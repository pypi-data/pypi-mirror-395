"""
Multileg Order Handler for Collective2 Connector

This module handles the execution of multi-leg option orders (e.g., Iron Condors, Spreads)
through the Collective2 API, which only supports single-leg orders.

The handler splits multileg orders into individual leg orders and executes them
in the correct sequence to avoid margin issues:
- Credit trades: Long legs first, then short legs
- Debit trades: Short legs first, then long legs

Each leg is adjusted independently using the template's adjustment parameters.
"""

import asyncio
import datetime as dt
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, List, Tuple

import httpx
from fastapi import status
from loguru import logger

from optrabot.broker.order import Leg
from optrabot.broker.order import Order as GenericOrder
from optrabot.broker.order import OrderAction, OrderStatus, OrderType
from optrabot.managedtrade import ManagedTrade

if TYPE_CHECKING:
    from optrabot.broker.c2connector import C2Connector, C2Order


class LegExecutionStatus(str, Enum):
    """Status of a single leg execution"""
    PENDING = 'pending'
    SUBMITTED = 'submitted'
    ADJUSTING = 'adjusting'
    FILLED = 'filled'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    SUBMIT_TIMEOUT = 'submit_timeout'  # Submission timed out, order status uncertain


@dataclass
class LegOrder:
    """Represents a single leg order for C2 execution"""
    leg: Leg
    c2_order: 'C2Order' = None
    initial_price: float = 0.0          # Mid-Price of the leg
    current_price: float = 0.0          # Current price (after adjustments)
    adjustment_count: int = 0
    signal_id: int = None
    status: LegExecutionStatus = LegExecutionStatus.PENDING
    fill_price: float = None
    error_message: str = None
    
    @property
    def is_long_leg(self) -> bool:
        """Returns True if this is a long (buy) leg"""
        return self.leg.action in [OrderAction.BUY, OrderAction.BUY_TO_OPEN, OrderAction.BUY_TO_CLOSE]
    
    @property
    def is_short_leg(self) -> bool:
        """Returns True if this is a short (sell) leg"""
        return self.leg.action in [OrderAction.SELL, OrderAction.SELL_TO_OPEN, OrderAction.SELL_TO_CLOSE]


@dataclass
class MultilegExecutionResult:
    """Result of a multileg order execution"""
    success: bool
    filled_legs: List[LegOrder] = field(default_factory=list)
    failed_legs: List[LegOrder] = field(default_factory=list)
    total_fill_price: float = 0.0
    error_message: str = None
    rollback_performed: bool = False
    
    @property
    def partial_fill(self) -> bool:
        """Returns True if some but not all legs were filled"""
        return len(self.filled_legs) > 0 and len(self.failed_legs) > 0


class MultilegOrderHandler:
    """
    Handles execution of multi-leg orders through C2 API.
    
    The handler:
    1. Splits the multileg order into individual leg orders
    2. Executes legs in the correct sequence (long first for credit, short first for debit)
    3. Adjusts prices for each leg independently until filled or max adjustments reached
    4. Performs rollback if any leg fails (closes already filled legs)
    5. Aggregates results and emits combined order status events
    """
    
    # Default configuration values
    DEFAULT_LEG_EXECUTION_TIMEOUT = 120  # seconds
    DEFAULT_MIN_DELAY_BETWEEN_REQUESTS = 0.5  # seconds (for rate limiting)
    DEFAULT_ADJUSTMENT_INTERVAL = 5  # seconds between price adjustments
    
    def __init__(self, c2_connector: 'C2Connector') -> None:
        self._connector = c2_connector
        self._leg_execution_timeout = self.DEFAULT_LEG_EXECUTION_TIMEOUT
        self._min_delay_between_requests = self.DEFAULT_MIN_DELAY_BETWEEN_REQUESTS
        self._adjustment_interval = self.DEFAULT_ADJUSTMENT_INTERVAL
        self._load_config()
    
    def _load_config(self) -> None:
        """Load multileg configuration from app config"""
        import optrabot.config as optrabotcfg
        config = optrabotcfg.appConfig
        
        try:
            multileg_config = config.get('c2.multileg')
            if multileg_config:
                self._leg_execution_timeout = multileg_config.get('leg_execution_timeout', self.DEFAULT_LEG_EXECUTION_TIMEOUT)
                self._min_delay_between_requests = multileg_config.get('min_delay_between_requests', self.DEFAULT_MIN_DELAY_BETWEEN_REQUESTS)
                self._adjustment_interval = multileg_config.get('adjustment_interval', self.DEFAULT_ADJUSTMENT_INTERVAL)
                logger.debug(f'Multileg config loaded: timeout={self._leg_execution_timeout}s, '
                           f'min_delay={self._min_delay_between_requests}s, adjustment_interval={self._adjustment_interval}s')
        except KeyError:
            logger.debug('No multileg configuration found, using defaults')
    
    async def execute_multileg_order(
        self, 
        managed_trade: ManagedTrade,
        order: GenericOrder
    ) -> MultilegExecutionResult:
        """
        Execute a multileg order by splitting it into individual leg orders.
        
        Args:
            managed_trade: The managed trade containing template configuration
            order: The multileg order to execute
            
        Returns:
            MultilegExecutionResult with success status and execution details
        """
        logger.info(f'Starting multileg order execution for {len(order.legs)} legs')
        
        # Create LegOrder objects for each leg
        leg_orders = self._create_leg_orders(order, managed_trade)
        
        # Store leg_orders in order.brokerSpecific so cancel_order can access them during execution
        order.brokerSpecific['active_leg_orders'] = leg_orders
        
        # Determine execution order based on price effect (credit vs debit)
        is_credit_trade = managed_trade.template.is_credit_trade()
        long_legs, short_legs = self._split_legs_by_side(leg_orders)
        
        if is_credit_trade:
            # Credit trade: Long legs first (buy protection), then short legs (sell premium)
            first_group = long_legs
            second_group = short_legs
            logger.info('Credit trade detected - executing long legs first, then short legs')
        else:
            # Debit trade: Short legs first (close short positions), then long legs
            first_group = short_legs
            second_group = long_legs
            logger.info('Debit trade detected - executing short legs first, then long legs')
        
        result = MultilegExecutionResult(success=False)
        
        try:
            # Execute first group of legs
            if first_group:
                group_success = await self._execute_leg_group(
                    first_group, managed_trade, order, 'first'
                )
                if not group_success:
                    result.error_message = 'Failed to execute first leg group'
                    result.failed_legs = [leg for leg in first_group if leg.status == LegExecutionStatus.FAILED]
                    # Rollback any filled legs from first group
                    filled_first = [leg for leg in first_group if leg.status == LegExecutionStatus.FILLED]
                    if filled_first:
                        await self._rollback_filled_legs(filled_first, managed_trade, order)
                        result.rollback_performed = True
                    return result
            
            # Execute second group of legs
            if second_group:
                group_success = await self._execute_leg_group(
                    second_group, managed_trade, order, 'second'
                )
                if not group_success:
                    result.error_message = 'Failed to execute second leg group'
                    result.failed_legs = [leg for leg in second_group if leg.status == LegExecutionStatus.FAILED]
                    # Rollback all filled legs (both groups)
                    all_filled = [leg for leg in leg_orders if leg.status == LegExecutionStatus.FILLED]
                    if all_filled:
                        await self._rollback_filled_legs(all_filled, managed_trade, order)
                        result.rollback_performed = True
                    return result
            
            # All legs executed successfully
            result.success = True
            result.filled_legs = leg_orders
            result.total_fill_price = self._calculate_total_fill_price(leg_orders, is_credit_trade)
            
            # Update the original order with aggregated fill information
            order.averageFillPrice = round(result.total_fill_price, 2)
            order.status = OrderStatus.FILLED
            
            logger.info(f'Multileg order executed successfully. Total fill price: ${result.total_fill_price:.2f}')
        
        except asyncio.CancelledError:
            logger.warning('Multileg order execution cancelled (shutdown in progress)')
            result.error_message = 'Execution cancelled due to shutdown'
            
            # Cancel any pending leg signals that were submitted but not filled
            pending_legs = [leg for leg in leg_orders if leg.status in [LegExecutionStatus.SUBMITTED, LegExecutionStatus.ADJUSTING]]
            if pending_legs:
                logger.info(f'Cancelling {len(pending_legs)} pending leg signals due to shutdown')
                for leg_order in pending_legs:
                    if leg_order.signal_id:
                        try:
                            await self._cancel_leg_signal(leg_order)
                            leg_order.status = LegExecutionStatus.CANCELLED
                        except Exception as e:
                            logger.warning(f'Failed to cancel leg signal {leg_order.signal_id}: {e}')
            
            # On cancellation, attempt rollback of any filled legs
            all_filled = [leg for leg in leg_orders if leg.status == LegExecutionStatus.FILLED]
            if all_filled:
                logger.info(f'Rolling back {len(all_filled)} filled legs due to cancellation')
                try:
                    await self._rollback_filled_legs(all_filled, managed_trade, order)
                    result.rollback_performed = True
                except asyncio.CancelledError:
                    logger.warning('Rollback also cancelled - manual cleanup may be required')
            raise  # Re-raise to propagate cancellation
            
        except Exception as e:
            logger.error(f'Unexpected error during multileg execution: {e}')
            result.error_message = str(e)
            # Attempt rollback
            all_filled = [leg for leg in leg_orders if leg.status == LegExecutionStatus.FILLED]
            if all_filled:
                await self._rollback_filled_legs(all_filled, managed_trade, order)
                result.rollback_performed = True
        
        return result
    
    def _create_leg_orders(self, order: GenericOrder, managed_trade: ManagedTrade) -> List[LegOrder]:
        """Create LegOrder objects from the order's legs with initial prices"""
        leg_orders = []
        
        for leg in order.legs:
            # Calculate mid price for the leg
            mid_price = self._calculate_leg_mid_price(leg)
            
            leg_order = LegOrder(
                leg=leg,
                initial_price=mid_price,
                current_price=mid_price
            )
            leg_orders.append(leg_order)
            logger.debug(f'Created leg order: {leg.action} {leg.strike} {leg.right} @ ${mid_price:.2f}')
        
        return leg_orders
    
    def _calculate_leg_mid_price(self, leg: Leg) -> float:
        """Calculate the mid price for a leg based on bid/ask"""
        if leg.midPrice is not None and leg.midPrice > 0:
            return leg.midPrice
        
        bid = leg.bidPrice if leg.bidPrice is not None and leg.bidPrice >= 0 else 0
        ask = leg.askPrice if leg.askPrice is not None and leg.askPrice >= 0 else 0
        
        if bid > 0 and ask > 0:
            return (bid + ask) / 2
        elif ask > 0:
            return ask
        elif bid > 0:
            return bid
        else:
            logger.warning(f'No valid price data for leg {leg.strike} {leg.right}, using 0')
            return 0
    
    def _split_legs_by_side(self, leg_orders: List[LegOrder]) -> Tuple[List[LegOrder], List[LegOrder]]:
        """Split legs into long and short groups"""
        long_legs = [lo for lo in leg_orders if lo.is_long_leg]
        short_legs = [lo for lo in leg_orders if lo.is_short_leg]
        return long_legs, short_legs
    
    async def _execute_leg_group(
        self,
        leg_orders: List[LegOrder],
        managed_trade: ManagedTrade,
        parent_order: GenericOrder,
        group_name: str
    ) -> bool:
        """
        Execute a group of legs (all long or all short).
        Legs are submitted with a small delay to respect rate limits,
        then all are monitored and adjusted in parallel.
        
        Returns True if all legs in the group were filled successfully.
        """
        from optrabot.broker.brokerfactory import BrokerFactory
        
        logger.info(f'Executing {group_name} leg group with {len(leg_orders)} legs')
        
        # Check if shutdown is in progress before starting
        if BrokerFactory().is_shutting_down() or not self._connector.isTradingEnabled():
            logger.warning(f'{group_name} leg group execution aborted - shutdown in progress')
            raise asyncio.CancelledError('Shutdown in progress')
        
        # Prepare and submit all legs with rate limit delay
        for leg_order in leg_orders:
            # Check shutdown status before each leg submission
            if BrokerFactory().is_shutting_down() or not self._connector.isTradingEnabled():
                logger.warning(f'{group_name} leg group execution aborted during submission - shutdown in progress')
                raise asyncio.CancelledError('Shutdown in progress')
            
            await self._prepare_leg_order(leg_order, parent_order, managed_trade)
            await self._submit_leg_order(leg_order, managed_trade)
            await asyncio.sleep(self._min_delay_between_requests)
        
        # Monitor and adjust all legs until filled or timeout
        adjustment_step = managed_trade.template.adjustmentStep
        max_adjustments = managed_trade.template.maxEntryAdjustments
        
        start_time = dt.datetime.now()
        timeout = dt.timedelta(seconds=self._leg_execution_timeout)
        
        while True:
            # Check for shutdown in progress
            if BrokerFactory().is_shutting_down() or not self._connector.isTradingEnabled():
                logger.warning(f'{group_name} leg group execution aborted during monitoring - shutdown in progress')
                raise asyncio.CancelledError('Shutdown in progress')
            
            # Check for timeout
            if dt.datetime.now() - start_time > timeout:
                logger.warning(f'Leg group execution timeout after {self._leg_execution_timeout}s')
                for leg_order in leg_orders:
                    if leg_order.status not in [LegExecutionStatus.FILLED, LegExecutionStatus.FAILED]:
                        leg_order.status = LegExecutionStatus.FAILED
                        leg_order.error_message = 'Execution timeout'
                return False
            
            # Check status of all legs
            all_filled = True
            any_failed = False
            
            for leg_order in leg_orders:
                if leg_order.status == LegExecutionStatus.FAILED:
                    any_failed = True
                    continue
                
                # Check if leg was cancelled externally
                if leg_order.status == LegExecutionStatus.CANCELLED:
                    logger.warning(f'Leg {leg_order.leg.strike} {leg_order.leg.right} was cancelled externally')
                    any_failed = True
                    continue
                
                if leg_order.status == LegExecutionStatus.FILLED:
                    continue
                
                all_filled = False
                
                # Handle SUBMIT_TIMEOUT: Check if order exists at C2 despite timeout
                if leg_order.status == LegExecutionStatus.SUBMIT_TIMEOUT:
                    order_found, signal_id, is_filled, fill_price = await self._find_order_at_c2(
                        leg_order, managed_trade
                    )
                    if order_found:
                        leg_order.signal_id = signal_id
                        if is_filled:
                            leg_order.status = LegExecutionStatus.FILLED
                            leg_order.fill_price = fill_price
                            logger.info(f'Leg {leg_order.leg.strike} {leg_order.leg.right} found at C2 and filled @ ${fill_price:.2f}')
                        else:
                            leg_order.status = LegExecutionStatus.SUBMITTED
                            logger.info(f'Leg {leg_order.leg.strike} {leg_order.leg.right} found at C2 with signal ID {signal_id}')
                        continue
                    else:
                        # Order not found at C2 after timeout - treat as failed
                        leg_order.status = LegExecutionStatus.FAILED
                        leg_order.error_message = 'Order not found at C2 after timeout'
                        logger.error(f'Leg {leg_order.leg.strike} {leg_order.leg.right} not found at C2 after timeout')
                        any_failed = True
                        continue
                
                # Check if leg was filled via C2 API
                filled, fill_price = await self._check_leg_fill_status(leg_order, managed_trade)
                if filled:
                    leg_order.status = LegExecutionStatus.FILLED
                    leg_order.fill_price = fill_price
                    logger.info(f'Leg {leg_order.leg.strike} {leg_order.leg.right} filled @ ${fill_price:.2f}')
                    continue
                
                # Check if leg was cancelled (detected during status check)
                if leg_order.status == LegExecutionStatus.CANCELLED:
                    logger.warning(f'Leg {leg_order.leg.strike} {leg_order.leg.right} was cancelled')
                    any_failed = True
                    continue
                
                # Check if we should adjust the price
                if max_adjustments is not None and leg_order.adjustment_count >= max_adjustments:
                    leg_order.status = LegExecutionStatus.FAILED
                    leg_order.error_message = f'Max adjustments ({max_adjustments}) reached'
                    any_failed = True
                    continue
                
                # Adjust the leg price
                adjustment_success = await self._adjust_leg_price(leg_order, adjustment_step, managed_trade)
                
                # If adjustment failed and leg is now cancelled, mark as failed
                if not adjustment_success and leg_order.status == LegExecutionStatus.CANCELLED:
                    any_failed = True
            
            if all_filled:
                logger.info(f'{group_name} leg group fully executed')
                return True
            
            if any_failed:
                logger.warning(f'{group_name} leg group has failed legs')
                return False
            
            # Wait before next adjustment cycle
            try:
                await asyncio.sleep(self._adjustment_interval)
            except asyncio.CancelledError:
                logger.warning(f'{group_name} leg group execution interrupted by shutdown')
                raise
        
        return False
    
    async def _find_order_at_c2(
        self,
        leg_order: LegOrder,
        managed_trade: ManagedTrade
    ) -> Tuple[bool, int | None, bool, float]:
        """
        Search for an order at C2 by matching leg characteristics.
        Used when submission timed out but order may have been received.
        
        Returns:
            Tuple of (order_found, signal_id, is_filled, fill_price)
        """
        import pytz
        
        leg = leg_order.leg
        start_date = self._connector._start_date.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        query = {
            'StrategyId': managed_trade.template.account,
            'StartDate': start_date
        }
        
        try:
            response = httpx.get(
                self._connector._base_url + '/Strategies/GetStrategyHistoricalOrders',
                headers=self._connector._http_headers,
                params=query,
                timeout=15.0
            )
            
            if response.status_code != status.HTTP_200_OK:
                logger.debug(f'Failed to search for order at C2: {response.text}')
                return False, None, False, 0.0
            
            json_data = json.loads(response.text)
            results = json_data.get('Results', [])
            
            # Search for matching order by symbol characteristics
            for result in results:
                exchange_symbol = result.get('ExchangeSymbol', {})
                
                # Match by strike, put/call, and expiration
                strike_matches = exchange_symbol.get('StrikePrice') == leg.strike
                # PutOrCall: 0 = Put, 1 = Call
                from optrabot.broker.order import OptionRight
                expected_put_or_call = 0 if leg.right == OptionRight.PUT else 1
                right_matches = exchange_symbol.get('PutOrCall') == expected_put_or_call
                
                # Check expiration (format: YYYYMMDD)
                expected_expiration = leg.expiration.strftime('%Y%m%d')
                expiration_matches = exchange_symbol.get('MaturityMonthYear') == expected_expiration
                
                if strike_matches and right_matches and expiration_matches:
                    signal_id = result.get('SignalId')
                    order_status = result.get('OrderStatus')
                    is_filled = order_status == '2'  # 2 = Filled
                    fill_price = result.get('AvgFillPrice', 0.0) if is_filled else 0.0
                    
                    logger.debug(f'Found matching order at C2: SignalId={signal_id}, Status={order_status}, '
                               f'Strike={leg.strike}, Right={leg.right}')
                    return True, signal_id, is_filled, fill_price
            
            return False, None, False, 0.0
            
        except Exception as e:
            logger.debug(f'Exception searching for order at C2: {e}')
            return False, None, False, 0.0

    async def _prepare_leg_order(
        self, 
        leg_order: LegOrder, 
        parent_order: GenericOrder,
        managed_trade: ManagedTrade
    ) -> None:
        """Prepare a C2Order for the leg"""
        import optrabot.symbolinfo as symbol_info_module
        from optrabot.broker.c2connector import C2ExchangeSymbol, C2Order
        
        leg = leg_order.leg
        symbol_info = symbol_info_module.symbol_infos[parent_order.symbol]
        
        c2_order = C2Order(
            order_type=self._connector._map_order_type(parent_order.type),
            side=self._connector._map_order_side(leg.action)
        )
        c2_order.StrategyId = managed_trade.template.account
        c2_order.OrderQuantity = parent_order.quantity
        c2_order.ExchangeSymbol = C2ExchangeSymbol(
            symbol_info.trading_class, 
            'OPT', 
            leg.right, 
            leg.strike
        )
        c2_order.ExchangeSymbol.MaturityMonthYear = leg.expiration.strftime('%Y%m%d')
        
        # Set initial price
        if parent_order.type == OrderType.LIMIT:
            c2_order.Limit = str(leg_order.current_price)
        
        leg_order.c2_order = c2_order
        logger.debug(f'Prepared C2Order for leg {leg.strike} {leg.right} @ ${leg_order.current_price:.2f}')
    
    async def _submit_leg_order(self, leg_order: LegOrder, managed_trade: ManagedTrade) -> None:
        """
        Submit a single leg order to C2.
        
        On timeout exceptions, the order status is set to SUBMIT_TIMEOUT instead of FAILED
        because the order may have been received by C2 despite the timeout. The monitoring
        loop will then check if the order exists at C2 and update the status accordingly.
        """
        c2_order = leg_order.c2_order
        
        data = {'Order': c2_order.to_dict()}
        logger.debug(f'Submitting leg order: {data}')
        
        try:
            response = httpx.post(
                self._connector._base_url + '/Strategies/NewStrategyOrder',
                headers=self._connector._http_headers,
                json=data,
                timeout=30.0  # Explicit timeout
            )
            
            if response.status_code != status.HTTP_200_OK:
                leg_order.status = LegExecutionStatus.FAILED
                leg_order.error_message = f'HTTP Error: {response.text}'
                logger.error(f'Failed to submit leg order: {response.text}')
                return
            
            json_data = json.loads(response.text)
            response_status = json_data.get('ResponseStatus')
            
            if response_status.get('ErrorCode') != str(status.HTTP_200_OK):
                leg_order.status = LegExecutionStatus.FAILED
                leg_order.error_message = f"API Error: {response_status.get('Message')}"
                logger.error(f'Failed to submit leg order: {response_status.get("Message")}')
                return
            
            result = json_data.get('Results')[0]
            leg_order.signal_id = result.get('SignalId')
            leg_order.status = LegExecutionStatus.SUBMITTED
            
            logger.info(f'Leg order submitted. Signal ID: {leg_order.signal_id}')
            
        except (httpx.TimeoutException, httpx.ReadTimeout) as e:
            # Timeout means we don't know if the order was received by C2
            # Set status to SUBMIT_TIMEOUT so monitoring loop can check
            leg_order.status = LegExecutionStatus.SUBMIT_TIMEOUT
            leg_order.error_message = f'Timeout: {e}'
            logger.warning(f'Timeout submitting leg order for {leg_order.leg.strike} {leg_order.leg.right} - '
                          f'will check if order exists at C2')
            
        except Exception as e:
            leg_order.status = LegExecutionStatus.FAILED
            leg_order.error_message = str(e)
            logger.error(f'Exception submitting leg order: {e}')
    
    async def _check_leg_fill_status(
        self, 
        leg_order: LegOrder, 
        managed_trade: ManagedTrade
    ) -> Tuple[bool, float]:
        """
        Check if a leg order has been filled via C2 API.
        Returns (is_filled, fill_price)
        """
        if leg_order.signal_id is None:
            return False, 0.0
        
        # Query C2 for order status
        # Note: This uses the same API as _track_orders but for a specific signal
        import pytz
        
        start_date = self._connector._start_date.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        query = {
            'StrategyId': managed_trade.template.account,
            'StartDate': start_date
        }
        
        try:
            response = httpx.get(
                self._connector._base_url + '/Strategies/GetStrategyHistoricalOrders',
                headers=self._connector._http_headers,
                params=query
            )
            
            if response.status_code != status.HTTP_200_OK:
                logger.debug(f'Failed to check leg status: {response.text}')
                return False, 0.0
            
            json_data = json.loads(response.text)
            results = json_data.get('Results', [])
            
            for result in results:
                if result.get('SignalId') == leg_order.signal_id:
                    order_status = result.get('OrderStatus')
                    if order_status == '2':  # Filled
                        fill_price = result.get('AvgFillPrice', 0)
                        return True, float(fill_price)
                    elif order_status == '4':  # Cancelled
                        leg_order.status = LegExecutionStatus.CANCELLED
                        return False, 0.0
            
            return False, 0.0
            
        except Exception as e:
            logger.debug(f'Exception checking leg status: {e}')
            return False, 0.0
    
    def _get_current_market_mid_price(
        self,
        leg: Leg,
        symbol: str
    ) -> float | None:
        """
        Get the current mid price from live market data for a leg.
        
        Returns:
            The current mid price, or None if market data is unavailable/outdated
        """
        try:
            strike_data = self._connector._broker_connector.get_option_strike_price_data(
                symbol, leg.expiration, leg.strike
            )
            
            if strike_data is None or strike_data.is_outdated():
                logger.debug(f'No current market data available for {leg.strike} {leg.right}')
                return None
            
            # Get bid/ask for the correct option type (put or call)
            from optrabot.broker.order import OptionRight
            if leg.right == OptionRight.PUT:
                bid = strike_data.putBid
                ask = strike_data.putAsk
            else:
                bid = strike_data.callBid
                ask = strike_data.callAsk
            
            if bid is not None and ask is not None and bid > 0 and ask > 0:
                return (bid + ask) / 2
            elif ask is not None and ask > 0:
                return ask
            elif bid is not None and bid > 0:
                return bid
            
            return None
        except Exception as e:
            logger.debug(f'Error fetching market data for {leg.strike} {leg.right}: {e}')
            return None

    async def _adjust_leg_price(
        self, 
        leg_order: LegOrder, 
        adjustment_step: float,
        managed_trade: ManagedTrade
    ) -> bool:
        """
        Adjust the leg price toward the market to improve fill probability.
        
        The method ensures that the new limit price is never worse than the current
        market mid price, preventing the order from lagging behind fast-moving markets.
        
        For long legs (buy): new price = max(current_price + step, market_mid_price)
        For short legs (sell): new price = min(current_price - step, market_mid_price)
        
        Returns:
            True if adjustment was successful, False if it failed (order may no longer exist)
        """
        leg = leg_order.leg
        symbol = managed_trade.entryOrder.symbol
        
        # Get current market mid price
        market_mid_price = self._get_current_market_mid_price(leg, symbol)
        
        # Determine adjustment direction based on leg side
        # Long legs (buy): Adjust UP toward ask price - must be at least at market mid
        # Short legs (sell): Adjust DOWN toward bid price - must be at least at market mid
        if leg_order.is_long_leg:
            step_adjusted_price = leg_order.current_price + adjustment_step
            direction = 'up'
            
            # For buy orders, use the higher of step-adjusted price or market mid
            # This ensures we don't lag behind a rising market
            if market_mid_price is not None and market_mid_price > step_adjusted_price:
                new_price = market_mid_price
                logger.debug(f'Leg {leg.strike} {leg.right}: Market moved up, using mid price ${market_mid_price:.2f} '
                           f'instead of step-adjusted ${step_adjusted_price:.2f}')
            else:
                new_price = step_adjusted_price
        else:
            step_adjusted_price = leg_order.current_price - adjustment_step
            direction = 'down'
            
            # For sell orders, use the lower of step-adjusted price or market mid
            # This ensures we don't lag behind a falling market
            if market_mid_price is not None and market_mid_price < step_adjusted_price:
                new_price = market_mid_price
                logger.debug(f'Leg {leg.strike} {leg.right}: Market moved down, using mid price ${market_mid_price:.2f} '
                           f'instead of step-adjusted ${step_adjusted_price:.2f}')
            else:
                new_price = step_adjusted_price
        
        # Ensure price doesn't go negative
        if new_price < 0.01:
            new_price = 0.01
        
        # Skip adjustment if price hasn't changed
        if abs(new_price - leg_order.current_price) < 0.005:  # Less than half a cent
            logger.debug(f'Leg {leg.strike} {leg.right}: Price unchanged, skipping adjustment')
            return True
        
        logger.debug(f'Adjusting leg {leg.strike} {leg.right} {direction}: ${leg_order.current_price:.2f} -> ${new_price:.2f}'
                    f'{f" (market mid: ${market_mid_price:.2f})" if market_mid_price else ""}')
        
        # Update the C2 order via cancel-replace
        c2_order = leg_order.c2_order
        previous_signal_id = leg_order.signal_id
        
        c2_order.Limit = str(new_price)
        c2_order.CancelReplaceSignalId = previous_signal_id
        
        data = {'Order': c2_order.to_dict()}
        
        try:
            response = httpx.put(
                self._connector._base_url + '/Strategies/ReplaceStrategyOrder',
                headers=self._connector._http_headers,
                json=data
            )
            
            if response.status_code != status.HTTP_200_OK:
                logger.warning(f'Failed to adjust leg order: {response.text}')
                # Check if order no longer exists - could be cancelled OR filled
                if 'Unable to cancel' in response.text or 'xrpeplace' in response.text.lower():
                    # The order cannot be modified - it's either filled or cancelled
                    # Wait a moment for C2 to update status, then check multiple times
                    for retry in range(3):
                        await asyncio.sleep(self._min_delay_between_requests)  # Respect rate limits
                        filled, fill_price = await self._check_leg_fill_status(leg_order, managed_trade)
                        if filled:
                            logger.info(f'Leg {leg.strike} {leg.right} was filled @ ${fill_price:.2f} (detected during adjustment)')
                            leg_order.status = LegExecutionStatus.FILLED
                            leg_order.fill_price = fill_price
                            return True  # Return True because the leg is successfully filled
                        if retry < 2:
                            logger.debug(f'Retry {retry + 1}/3: Leg {leg.strike} {leg.right} not yet showing as filled, waiting...')
                    
                    # After retries, if still not filled, it was cancelled
                    logger.warning(f'Leg {leg.strike} {leg.right} appears to be cancelled externally')
                    leg_order.status = LegExecutionStatus.CANCELLED
                    leg_order.error_message = 'Order cancelled externally'
                return False
            
            json_data = json.loads(response.text)
            response_status = json_data.get('ResponseStatus')
            
            if response_status.get('ErrorCode') != str(status.HTTP_200_OK):
                error_message = response_status.get('Message', '')
                logger.warning(f'Failed to adjust leg order: {error_message}')
                # Check for specific error indicating order no longer exists
                errors = response_status.get('Errors', [])
                for error in errors:
                    if 'Unable to cancel' in error.get('Message', '') or 'xrpeplace' in error.get('Message', '').lower():
                        # The order cannot be modified - it's either filled or cancelled
                        # Wait a moment for C2 to update status, then check multiple times
                        for retry in range(3):
                            await asyncio.sleep(self._min_delay_between_requests)  # Respect rate limits
                            filled, fill_price = await self._check_leg_fill_status(leg_order, managed_trade)
                            if filled:
                                logger.info(f'Leg {leg.strike} {leg.right} was filled @ ${fill_price:.2f} (detected during adjustment)')
                                leg_order.status = LegExecutionStatus.FILLED
                                leg_order.fill_price = fill_price
                                return True  # Return True because the leg is successfully filled
                            if retry < 2:
                                logger.debug(f'Retry {retry + 1}/3: Leg {leg.strike} {leg.right} not yet showing as filled, waiting...')
                        
                        # After retries, if still not filled, it was cancelled
                        logger.warning(f'Leg {leg.strike} {leg.right} appears to be cancelled externally')
                        leg_order.status = LegExecutionStatus.CANCELLED
                        leg_order.error_message = 'Order cancelled externally'
                        return False
                return False
            
            result = json_data.get('Results')[0]
            leg_order.signal_id = result.get('SignalId')
            leg_order.current_price = new_price
            leg_order.adjustment_count += 1
            leg_order.status = LegExecutionStatus.ADJUSTING
            
            logger.info(f'Leg {leg.strike} {leg.right} adjusted to ${new_price:.2f} '
                       f'(adjustment #{leg_order.adjustment_count})')
            return True
            
        except Exception as e:
            logger.warning(f'Exception adjusting leg order: {e}')
            return False
    
    async def _rollback_filled_legs(
        self,
        filled_legs: List[LegOrder],
        managed_trade: ManagedTrade,
        original_order: GenericOrder
    ) -> None:
        """
        Rollback filled legs by creating closing orders.
        This is called when the multileg execution fails partially.
        """
        logger.warning(f'Rolling back {len(filled_legs)} filled legs')
        
        for leg_order in filled_legs:
            try:
                # Create opposite order to close the position
                closing_action = self._get_closing_action(leg_order.leg.action)
                
                import optrabot.symbolinfo as symbol_info_module
                from optrabot.broker.c2connector import (C2ExchangeSymbol,
                                                         C2Order)
                
                leg = leg_order.leg
                symbol_info = symbol_info_module.symbol_infos[original_order.symbol]
                
                c2_order = C2Order(
                    order_type=self._connector._map_order_type(OrderType.MARKET),  # Use market for rollback
                    side=self._connector._map_order_side(closing_action)
                )
                c2_order.StrategyId = managed_trade.template.account
                c2_order.OrderQuantity = original_order.quantity
                c2_order.ExchangeSymbol = C2ExchangeSymbol(
                    symbol_info.trading_class,
                    'OPT',
                    leg.right,
                    leg.strike
                )
                c2_order.ExchangeSymbol.MaturityMonthYear = leg.expiration.strftime('%Y%m%d')
                
                data = {'Order': c2_order.to_dict()}
                logger.info(f'Submitting rollback order for leg {leg.strike} {leg.right}')
                
                response = httpx.post(
                    self._connector._base_url + '/Strategies/NewStrategyOrder',
                    headers=self._connector._http_headers,
                    json=data
                )
                
                if response.status_code == status.HTTP_200_OK:
                    logger.info(f'Rollback order submitted for leg {leg.strike} {leg.right}')
                else:
                    logger.error(f'Failed to submit rollback order: {response.text}')
                
                await asyncio.sleep(self._min_delay_between_requests)
                
            except Exception as e:
                logger.error(f'Exception during rollback of leg {leg_order.leg.strike}: {e}')
    
    def _get_closing_action(self, opening_action: OrderAction) -> OrderAction:
        """Get the closing action for an opening action"""
        match opening_action:
            case OrderAction.BUY | OrderAction.BUY_TO_OPEN:
                return OrderAction.SELL_TO_CLOSE
            case OrderAction.SELL | OrderAction.SELL_TO_OPEN:
                return OrderAction.BUY_TO_CLOSE
            case OrderAction.BUY_TO_CLOSE:
                return OrderAction.SELL_TO_OPEN
            case OrderAction.SELL_TO_CLOSE:
                return OrderAction.BUY_TO_OPEN
            case _:
                return OrderAction.SELL_TO_CLOSE
    
    def _calculate_total_fill_price(self, leg_orders: List[LegOrder], is_credit_trade: bool) -> float:
        """
        Calculate the total fill price from all legs.
        For credit trades: sum of sold premiums - sum of bought premiums
        For debit trades: sum of bought premiums - sum of sold premiums
        """
        total = 0.0
        
        for leg_order in leg_orders:
            if leg_order.fill_price is None:
                continue
            
            if leg_order.is_long_leg:
                total -= leg_order.fill_price  # Paid premium (debit)
            else:
                total += leg_order.fill_price  # Received premium (credit)
        
        # For credit trades, result should be positive (credit received)
        # For debit trades, result should be negative (debit paid)
        return total
    
    async def _cancel_leg_signal(self, leg_order: LegOrder) -> bool:
        """
        Cancels a pending leg signal at C2.
        
        Args:
            leg_order: The leg order with a signal_id to cancel
            
        Returns:
            True if cancellation was successful
        """
        if leg_order.signal_id is None:
            logger.warning('Cannot cancel leg - no signal ID')
            return False
        
        data = {
            'SignalId': leg_order.signal_id
        }
        
        try:
            logger.debug(f'Sending cancel request for signal {leg_order.signal_id} to C2 API')
            response = httpx.post(
                self._connector._base_url + '/Strategies/CancelStrategySignal',
                headers=self._connector._http_headers,
                json=data
            )
            
            logger.debug(f'Cancel response: status={response.status_code}, body={response.text}')
            
            if response.status_code != status.HTTP_200_OK:
                logger.warning(f'Failed to cancel leg signal {leg_order.signal_id}: HTTP {response.status_code} - {response.text}')
                return False
            
            json_data = json.loads(response.text)
            response_status = json_data.get('ResponseStatus')
            
            if response_status.get('ErrorCode') != str(status.HTTP_200_OK):
                error_msg = response_status.get('Message', 'Unknown error')
                logger.warning(f'Failed to cancel leg signal {leg_order.signal_id}: {error_msg}')
                return False
            
            logger.info(f'Leg signal {leg_order.signal_id} for {leg_order.leg.strike} {leg_order.leg.right} cancelled')
            return True
            
        except Exception as e:
            logger.warning(f'Exception cancelling leg signal {leg_order.signal_id}: {e}')
            return False
