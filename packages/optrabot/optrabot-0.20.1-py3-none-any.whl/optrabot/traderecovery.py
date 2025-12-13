"""
OTB-253: Trade Recovery Module

This module handles recovery of trades after OptraBot restart.
Implements phased recovery:
1. Settlement of expired trades
2. Recovery of active trades
3. Position reconciliation (future implementation)
"""

import copy
from datetime import date, datetime
from typing import List

import pytz
from loguru import logger
from sqlalchemy.orm import Session

from optrabot import crud
from optrabot.broker.order import (Leg, OptionRight, Order, OrderAction,
                                   OrderStatus, OrderType, PriceEffect)
from optrabot.database import get_db_engine
from optrabot.managedtrade import ManagedTrade
from optrabot.models import Trade, Transaction
from optrabot.tradehelper import TradeHelper, group_transactions
from optrabot.tradestatus import TradeStatus
from optrabot.tradetemplate.templatefactory import Template


class TradeRecoveryService:
    """
    Handles recovery of trades and orders after OptraBot restart.
    """
    
    # Separator line width for log output
    SEPARATOR_WIDTH = 70
    
    def __init__(self):
        self.recovered_count = 0
        self.settled_count = 0
        self.failed_count = 0
    
    async def recover_for_broker(self, broker_id: str, account_ids: list):
        """
        Recover trades for a specific broker and its accounts.
        
        Args:
            broker_id: The broker identifier (e.g., 'IBTWS', 'TASTY')
            account_ids: List of account IDs belonging to this broker
        
        This method:
        1. Queries database for OPEN trades belonging to this broker's accounts
        2. For each trade:
           - Loads template by template_name
           - Reconstructs entry order from transactions
           - Creates ManagedTrade object
           - Registers with TradeManager
        3. Logs summary for this broker
        """
        logger.info("=" * self.SEPARATOR_WIDTH)
        logger.info(f"Starting Trade Recovery for broker {broker_id}")
        logger.info(f"Accounts: {', '.join(account_ids)}")
        logger.info("=" * self.SEPARATOR_WIDTH)
        
        # Recover active trades for this broker's accounts
        broker_recovered = 0
        broker_failed = 0
        
        with Session(get_db_engine()) as session:
            today = date.today()
            
            # Find OPEN trades for this broker's accounts
            open_trades = session.query(Trade).filter(
                Trade.status == TradeStatus.OPEN,
                Trade.account.in_(account_ids)
            ).all()
            
            if not open_trades:
                logger.info(f"No active trades found for broker {broker_id}")
            else:
                logger.debug(f"Found {len(open_trades)} open trade(s) for broker {broker_id}")
                
                for trade in open_trades:
                    # Check if trade has expired (failsafe)
                    expiration_date = self._get_trade_expiration(trade)
                    if expiration_date and expiration_date < today:
                        logger.warning(
                            f"Trade {trade.id} is OPEN but expired on {expiration_date} "
                            f"- skipping (should be handled by expired trades settlement)"
                        )
                        continue
                    
                    # Skip trades without template_name (old trades before OTB-253)
                    if not trade.template_name:
                        logger.warning(
                            f"Trade {trade.id} has no template_name - "
                            f"created before OTB-253, cannot recover"
                        )
                        broker_failed += 1
                        continue
                    
                    # Recover this trade
                    try:
                        await self._recover_single_trade(trade.id, trade.template_name)
                        broker_recovered += 1
                    except Exception as e:
                        logger.error(
                            f"Failed to recover trade {trade.id} for broker {broker_id}: {e}",
                            exc_info=True
                        )
                        broker_failed += 1
        
        logger.info("=" * self.SEPARATOR_WIDTH)
        logger.info(f"Trade Recovery Summary for broker {broker_id}:")
        logger.info(f"  Active trades recovered: {broker_recovered}")
        logger.info(f"  Failed recoveries: {broker_failed}")
        logger.info("=" * self.SEPARATOR_WIDTH)
        
        # Update global counters
        self.recovered_count += broker_recovered
        self.failed_count += broker_failed
    
    async def recover_all(self):
        """
        Main recovery orchestration (DEPRECATED - use recover_for_broker instead).
        Implements Phase 1 (expired trades) and Phase 2 (active trades).
        
        Note: This method is kept for backwards compatibility but should not be used
        in multi-broker scenarios. Use recover_for_broker() for each connected broker instead.
        """
        logger.info("=" * self.SEPARATOR_WIDTH)
        logger.info("Starting Trade Recovery")
        logger.info("=" * self.SEPARATOR_WIDTH)
        
        # Phase 1: Settle expired trades (no broker needed)
        await self.settle_expired_trades()
        
        # Phase 2: Recover active trades (requires templates from config)
        await self.recover_active_trades()
        
        # Phase 3-4: To be implemented
        # - Order recovery (TP/SL orders)
        # - Position reconciliation
        
        logger.info("=" * self.SEPARATOR_WIDTH)
        logger.info(f"Trade Recovery Summary:")
        logger.info(f"  Expired trades settled: {self.settled_count}")
        logger.info(f"  Active trades recovered: {self.recovered_count}")
        logger.info(f"  Failed recoveries: {self.failed_count}")
        logger.info("=" * self.SEPARATOR_WIDTH)
    
    async def settle_expired_trades(self):
        """
        Find all OPEN trades with expiration < today and perform EOD settlement.
        
        This handles trades that:
        - Were opened but OptraBot was stopped before their expiration
        - Missed the regular EOD settlement for any reason
        - Have already expired but are still marked as OPEN
        
        Uses the same settlement logic as the regular EOD settlement (OTB-254, OTB-259).
        """
        logger.info("Phase 1: Settling expired trades")
        
        # Get market close time from BrokerFactory
        from optrabot.broker.brokerfactory import BrokerFactory
        broker_factory = BrokerFactory()
        market_close_time = broker_factory._session_end
        
        # Step 1: Find expired trades (read-only, can use single session)
        expired_trades = []
        with Session(get_db_engine()) as session:
            today = date.today()
            now = datetime.now(pytz.timezone('US/Eastern'))
            
            # Find all OPEN trades
            open_trades = session.query(Trade).filter(
                Trade.status == TradeStatus.OPEN
            ).all()
            
            if not open_trades:
                logger.info("No open trades found in database")
                return
            
            logger.debug(f"Found {len(open_trades)} open trades, checking expiration dates...")
            
            for trade in open_trades:
                expiration_date = self._get_trade_expiration(trade)
                
                if expiration_date is None:
                    # Trade has no transactions or no expiration date
                    # Settle it anyway with expiration = today (realized PNL will be 0)
                    logger.warning(
                        f"Trade {trade.id} has no expiration date in transactions - "
                        f"settling with expiration = today"
                    )
                    expired_trades.append((trade.id, today))
                    continue
                
                # Check if trade is expired:
                # 1. Expiration date is before today -> expired
                # 2. Expiration date is today AND market is closed -> expired
                is_expired = False
                if expiration_date < today:
                    is_expired = True
                elif expiration_date == today:
                    # Trade expires today - check if market has closed
                    if market_close_time and now >= market_close_time:
                        is_expired = True
                        logger.debug(
                            f"Trade {trade.id} expires today and market is closed "
                            f"(close: {market_close_time}, now: {now})"
                        )
                    else:
                        logger.debug(
                            f"Trade {trade.id} expires today but market is still open "
                            f"(close: {market_close_time}, now: {now})"
                        )
                
                if is_expired:
                    # Store only the trade ID and expiration, not the ORM object
                    expired_trades.append((trade.id, expiration_date))
                    logger.debug(
                        f"Trade {trade.id} expired on {expiration_date} "
                        f"({(today - expiration_date).days} days ago)"
                    )
        
        if not expired_trades:
            logger.info("No expired trades found - all trades are current")
            return
        
        logger.info(f"Found {len(expired_trades)} expired trade(s) requiring settlement")
        
        # Step 2: Settle each expired trade (each in its own session)
        for trade_id, expiration_date in expired_trades:
            try:
                await self._settle_single_trade(trade_id, expiration_date)
                self.settled_count += 1
            except Exception as e:
                logger.error(
                    f"Failed to settle expired trade {trade_id}: {e}",
                    exc_info=True
                )
                self.failed_count += 1
    
    def _get_trade_expiration(self, trade: Trade) -> date:
        """
        Get the expiration date of a trade from its transactions.
        
        All option legs should have the same expiration (same expiration cycle).
        Returns the expiration date or None if no transactions exist.
        """
        if not trade.transactions:
            return None
        
        # Get expiration from first option transaction
        for transaction in trade.transactions:
            if transaction.expiration:
                return transaction.expiration
        
        return None
    
    async def _settle_single_trade(self, trade_id: int, expiration_date: date):
        """
        Settle a single expired trade.
        
        Optimized settlement logic:
        1. Load fresh trade from database with all current transactions
        2. Set trade status to EXPIRED
        3. Call TradeHelper.updateTrade() - creates closing transactions and calculates P&L
        4. Reload trade to get closing transactions
        5. Apply calculated P&L and update in database
        
        Each trade settlement manages sessions carefully to avoid SQLite locking.
        
        Args:
            trade_id: ID of trade to settle
            expiration_date: The expiration date of the trade
        """
        days_since_expiration = (date.today() - expiration_date).days
        
        logger.info(
            f"Settling expired trade {trade_id} "
            f"(Expiration: {expiration_date}, {days_since_expiration} days ago)"
        )
        
        # Load fresh trade from database with all current transactions
        with Session(get_db_engine()) as session:
            trade = crud.getTrade(session, trade_id)
            if not trade:
                raise Exception(f"Trade {trade_id} not found in database")
            
            logger.debug(
                f"Trade {trade_id}: Account={trade.account}, Symbol={trade.symbol}, "
                f"Status={trade.status}, Transactions={len(trade.transactions)}"
            )
            
            # Set status to EXPIRED before processing
            trade.status = TradeStatus.EXPIRED
            
            # Process trade: creates closing transactions (if needed) and calculates realizedPNL
            # OTB-262: Pass session to avoid "database is locked" error from concurrent sessions
            TradeHelper.updateTrade(trade, session)
            
            # Update the trade in database with calculated values
            crud.update_trade(session, trade)
            
            logger.info(
                f"✅ Trade {trade_id} settled successfully "
                f"(Realized P&L: ${trade.realizedPNL:.2f})"
            )    # ========================================================================
    # Phase 2: Active Trade Recovery
    # ========================================================================
    
    async def recover_active_trades(self):
        """
        Find all OPEN trades and recover them into TradeManager.
        
        This method:
        1. Queries database for OPEN trades (non-expired)
        2. For each trade:
           - Loads template by template_name
           - Reconstructs entry order from transactions
           - Creates ManagedTrade object
           - Registers with TradeManager
        3. Logs summary
        
        Trades without template_name (created before OTB-253) cannot be recovered.
        """
        logger.info("Phase 2: Recovering active trades")
        
        active_trades = []
        
        # Step 1: Find OPEN trades
        with Session(get_db_engine()) as session:
            today = date.today()
            
            open_trades = session.query(Trade).filter(
                Trade.status == TradeStatus.OPEN
            ).all()
            
            if not open_trades:
                logger.info("No active trades found for recovery")
                return
            
            logger.debug(f"Found {len(open_trades)} open trade(s) in database")
            
            for trade in open_trades:
                # Check if trade has expired (failsafe - should be caught in Phase 1)
                expiration_date = self._get_trade_expiration(trade)
                if expiration_date and expiration_date < today:
                    logger.warning(
                        f"Trade {trade.id} is OPEN but expired on {expiration_date} "
                        f"- should have been settled in Phase 1"
                    )
                    continue
                
                # Skip trades without template_name (old trades before OTB-253)
                if not trade.template_name:
                    logger.warning(
                        f"Trade {trade.id} has no template_name - "
                        f"created before OTB-253, cannot recover"
                    )
                    continue
                
                # Store only IDs and template_name (not ORM objects)
                active_trades.append((
                    trade.id, 
                    trade.template_name, 
                    trade.account, 
                    trade.symbol
                ))
        
        if not active_trades:
            logger.info("No active trades require recovery")
            return
        
        logger.info(f"Found {len(active_trades)} active trade(s) requiring recovery")
        
        # Step 2: Recover each trade
        for trade_id, template_name, account, symbol in active_trades:
            try:
                await self._recover_single_trade(trade_id, template_name)
                self.recovered_count += 1
            except Exception as e:
                logger.error(
                    f"Failed to recover active trade {trade_id} "
                    f"(Template: {template_name}): {e}",
                    exc_info=True
                )
                self.failed_count += 1
    
    async def _recover_single_trade(self, trade_id: int, template_name: str):
        """
        Recover a single active trade.
        
        Steps:
        1. Load template from config by name
        2. Load trade with all transactions from database
        3. Reconstruct entry order from transactions
        4. Prepare entry order (fill broker-specific data)
        5. Create ManagedTrade object
        6. Register with TradeManager
        
        Args:
            trade_id: ID of trade to recover
            template_name: Name of template used for this trade
            
        Raises:
            Exception: If template not found or trade has no transactions
        """
        from optrabot.broker.brokerfactory import BrokerFactory
        from optrabot.config import appConfig

        # Step 1: Load template
        template = appConfig.get_template_by_name(template_name)
        if template is None:
            logger.error(
                f"Cannot recover trade {trade_id}: "
                f"Template '{template_name}' not found in config"
            )
            raise Exception(f"Template '{template_name}' not found")
        
        # Step 2: Load trade with all transactions
        with Session(get_db_engine()) as session:
            trade = crud.getTrade(session, trade_id)
            if not trade:
                raise Exception(f"Trade {trade_id} not found in database")
            
            if not trade.transactions:
                raise Exception(f"Trade {trade_id} has no transactions - cannot recover")
            
            logger.info(
                f"Recovering trade {trade_id} "
                f"(Account: {trade.account}, Symbol: {trade.symbol}, "
                f"Template: {template.name})"
            )
            
            # Step 3: Reconstruct entry order from transactions
            try:
                entry_order = self._reconstruct_entry_order(trade, template)
            except Exception as e:
                logger.error(
                    f"Failed to reconstruct entry order for trade {trade_id}: {e}",
                    exc_info=True
                )
                raise Exception(f"Failed to reconstruct entry order: {e}")

            logger.debug(
                f"Reconstructed entry order for trade {trade_id}: "
                f"{len(entry_order.legs)} legs, entry price: ${entry_order.filled_price:.2f}"
            )
            
            # Step 4: Prepare entry order to fill broker-specific data
            # This is critical for closing orders to work correctly
            # need_valid_price_data=False because we don't need current market prices for recovery
            brokerConnector = BrokerFactory().getBrokerConnectorByAccount(trade.account)
            if brokerConnector is None:
                raise Exception(f"No broker connector found for account {trade.account}")
            
            try:
                await brokerConnector.prepareOrder(entry_order, need_valid_price_data=False)
                logger.debug(
                    f"Entry order prepared with broker-specific data for trade {trade_id}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to prepare entry order for trade {trade_id}: {e}",
                    exc_info=True
                )
                raise Exception(f"Failed to prepare entry order: {e}")
            
            # Step 5: Create ManagedTrade object
            managed_trade = self._create_managed_trade(trade, template, entry_order)
            
            # Step 6: Register with TradeManager
            self._register_with_trade_manager(managed_trade)
            
            logger.info(
                f"✅ Trade {trade_id} recovered successfully "
                f"(Template: {template.name}, Amount: {entry_order.quantity}, Entry: ${entry_order.filled_price:.2f})"
            )
    
    def _reconstruct_entry_order(self, trade: Trade, template: Template) -> Order:
        """
        Reconstruct the entry order from trade transactions.
        
        Uses the shared group_transactions() function from TradeHelper to identify
        entry transactions. This ensures consistent logic between trade recovery
        and API display.
        
        Args:
            trade: Trade object with transactions
            template: Template object from config (needed for quantity/amount)
            
        Returns:
            Order object with legs reconstructed from opening transactions
        """
        # Use shared transaction grouping logic
        grouping = group_transactions(trade.transactions)
        
        # Create legs from entry leg summaries
        legs = []
        for entry_leg in grouping.entry_legs:
            action = OrderAction.SELL if entry_leg.action == 'SELL' else OrderAction.BUY
            leg = Leg(
                action=action,
                symbol=trade.symbol,
                quantity=1,  # Always 1 - amount scales the order
                strike=entry_leg.strike,
                right=OptionRight.CALL if entry_leg.sectype == 'C' else OptionRight.PUT,
                expiration=entry_leg.expiration
            )
            legs.append(leg)
        
        # Use amount and premium from grouping
        amount = grouping.trade_amount
        total_premium = grouping.total_entry_premium
        
        # Determine price effect based on total premium
        price_effect = PriceEffect.CREDIT if total_premium > 0 else PriceEffect.DEBIT
        
        # Calculate price per unit (divide by amount to get price for 1 set of legs)
        price_per_unit = abs(total_premium) / amount if amount > 0 else abs(total_premium)
        
        order = Order(
            symbol=trade.symbol,
            legs=legs,
            action=OrderAction.BUY_TO_OPEN,  # Entry orders are always BUY_TO_OPEN (opening a position)
            quantity=amount,  # Use amount from transactions (e.g., 2 for 2x Iron Condor)
            type=OrderType.MARKET,  # For recovery, type doesn't matter
            price=price_per_unit  # Price for 1 unit (1 set of legs)
        )
        
        # Set price_effect, filled price, and average fill price
        order.price_effect = price_effect
        order.filled_price = price_per_unit  # Price per unit
        order.averageFillPrice = price_per_unit  # Same as filled_price for recovered trades
        order.status = OrderStatus.FILLED
        
        return order
    
    def _create_managed_trade(
        self, 
        trade: Trade, 
        template: Template, 
        entry_order: Order
    ) -> ManagedTrade:
        """
        Create a ManagedTrade object for recovery.
        
        This is similar to what TradeManager.openTrade() does after entry order is filled,
        but without placing orders - we're recovering an existing trade.
        
        Args:
            trade: Trade model from database
            template: Template object from config
            entry_order: Reconstructed entry order
            
        Returns:
            ManagedTrade object ready for monitoring
        """
        managed_trade = ManagedTrade(
            trade=trade,
            template=template,
            entryOrder=entry_order,
            account=trade.account
        )
        
        # Set status to OPEN (trade is active)
        managed_trade.status = TradeStatus.OPEN
        
        # Set entry price from filled order
        managed_trade.entry_price = entry_order.filled_price
        
        # Set current legs from entry order
        # Use deepcopy to avoid reference issues
        managed_trade.current_legs = copy.deepcopy(entry_order.legs)
        
        # Setup adjusters (Stop Loss, Delta)
        # These methods copy adjusters from template and set base price
        managed_trade.setup_stoploss_adjusters()
        managed_trade.setup_delta_adjusters()
        
        return managed_trade
    
    def _register_with_trade_manager(self, managed_trade: ManagedTrade):
        """
        Register recovered trade with TradeManager.
        
        This adds the trade to TradeManager._trades[] so it will be
        monitored and managed like any other active trade.
        
        Args:
            managed_trade: ManagedTrade object to register
        """
        from optrabot.trademanager import TradeManager
        
        tm = TradeManager()
        tm._trades.append(managed_trade)
        
        logger.debug(
            f"Registered recovered trade {managed_trade.trade.id} "
            f"with TradeManager (Template: {managed_trade.template.name})"
        )
