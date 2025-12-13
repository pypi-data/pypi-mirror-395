import asyncio
import datetime as dt
import json
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List, Optional

import httpx
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import status
from loguru import logger

import optrabot.config as optrabotcfg
import optrabot.symbolinfo as symbol_info
from optrabot.broker.brokerconnector import BrokerConnector
from optrabot.broker.c2multileg import LegExecutionStatus, MultilegOrderHandler
from optrabot.broker.optionpricedata import OptionStrikePriceData
from optrabot.broker.order import OptionRight
from optrabot.broker.order import Order as GenericOrder
from optrabot.broker.order import OrderAction
from optrabot.broker.order import OrderStatus
from optrabot.broker.order import OrderStatus as GenericOrderStatus
from optrabot.broker.order import OrderType
from optrabot.exceptions.orderexceptions import (PlaceOrderException,
                                                 PrepareOrderException)
from optrabot.managedtrade import ManagedTrade
from optrabot.models import Account
from optrabot.tradetemplate.templatefactory import Template


class C2OrderSide(str, Enum):
	"""
	Represents the side of an order
	"""
	BUY = '1'
	SELL = '2'

class C2OrderType(str, Enum):
	"""
	Represents the type of an order
	"""
	MARKET = '1'
	LIMIT = '2'
	STOP = '3'

@dataclass
class C2ExchangeSymbol:
	"""
	Class for Collective2 Exchange Symbol Data
	"""
	Symbol: str = None
	Currency: str = None
	SecurityExchange: str = None
	SecurityType: str = None
	MaturityMonthYear: str = None
	PutOrCall: int = None
	StrikePrice: int = None
	PriceMultiplier: int = 1

	def __init__(self, symbol: str, symbol_type: str, right: OptionRight, strike: float) -> None:
		self.Symbol = symbol
		self.SecurityType = symbol_type
		self.PutOrCall = 1 if right == OptionRight.CALL else 0
		self.StrikePrice = strike
		self.SecurityExchange = 'DEFAULT'
		self.Currency = 'USD'

	def to_dict(self) -> dict:
		"""
		Returns the JSON representation of the order
		"""
		return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass
class C2Order:
	"""
	Class for Collective2 Order
	"""
	StrategyId: str = None
	OrderType: C2OrderType = None
	Side: C2OrderSide = None
	OrderQuantity: int = 0
	Limit: str = None
	Stop: str = None
	TIF: str = None
	ExchangeSymbol: C2ExchangeSymbol = None
	ParentSignalId: int = None
	CancelReplaceSignalId: int = None			# Id of the Signal Id which is to be replaced (used for Adjust Order)

	def __init__(self, order_type: C2OrderType, side: C2OrderSide, quantity: int = 1, strategy_id: str = None) -> None:
		self.StrategyId = strategy_id
		self.OrderType = order_type
		self.Side = side
		self.OrderQuantity = quantity
		self.TIF= '0'

	def to_dict(self) -> dict:
		"""
		Returns the JSON representation of the order
		"""
		result = {}
		result['StrategyId'] = self.StrategyId
		result['OrderType'] = self.OrderType.value
		result['Side'] = self.Side.value
		result['OrderQuantity'] = self.OrderQuantity
		result['TIF'] = self.TIF
		if self.ParentSignalId is not None:
			result['ParentSignalId'] = self.ParentSignalId
		if self.Limit is not None:
			result['Limit'] = self.Limit
		if self.Stop is not None:
			result['Stop'] = self.Stop
		if self.ExchangeSymbol is not None:
			result['ExchangeSymbol'] = self.ExchangeSymbol.to_dict()
		if self.CancelReplaceSignalId is not None:
			result['CancelReplaceSignalId'] = self.CancelReplaceSignalId
		return result
	
class C2Connector(BrokerConnector):
	"""
	Connector for the Collective2 platform for submitting trades to C2 strategies
	"""
	def __init__(self) -> None:
		super().__init__()
		self.id = 'C2'
		self.broker = 'C2'
		self._base_url = 'https://api4-general.collective2.com'
		self._api_key = None
		self._broker_connector = None
		self._http_headers = None
		self._strategies = []
		self._orders: List[GenericOrder] = []
		self._connected = False
		self._backgroundScheduler = AsyncIOScheduler()
		self._backgroundScheduler.start()
		self._start_date: dt.datetime = None
		# C2 does not support native multileg orders - legs must be sent individually
		self._supports_multileg_orders = False
		# C2 connector handles price adjustments internally for multileg orders
		self._internal_order_adjustment = True
		# Multileg order handler (lazy initialized)
		self._multileg_handler: Optional['MultilegOrderHandler'] = None
		# Shutdown synchronization: track pending multileg operations
		self._pending_multileg_tasks: set = set()
		self._shutdown_lock = asyncio.Lock()
		self._initialize()

	def _initialize(self) -> None:
		"""
		Initialize the C2 connector
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		try:
			config.get('c2')
		except KeyError:
			logger.debug('No Collective2 configuration found')
			return

		try:
			self._api_key = config.get('c2.apikey')
		except KeyError:
			logger.error('No Collective2 API key configured!')
			return
		
		try:
			broker = config.get('c2.broker')
		except KeyError:
			broker = None
			logger.error('No broker configured for C2 Connector!')
			return
		from optrabot.broker.brokerfactory import BrokerFactory

		self._broker_connector = BrokerFactory().get_connector_by_id(broker)
		if self._broker_connector is None:
			logger.error(f'Broker connector with id {broker} not found for C2 Connector!')
			return
		
		try:
			self._strategies = str(config.get('c2.strategies')).split(',')
		except KeyError:
			logger.error('No strategies configured for C2 Connector!')
			return
		self._start_date = dt.datetime.now()
		self._http_headers = {'Authorization': 'Bearer ' +  self._api_key, 'Content-Type': 'application/json'}
		self._initialized = True
		self._backgroundScheduler.add_job(self._track_orders, 'interval', seconds=5, id='_track_signals', misfire_grace_time=None)

	def ___del__(self) -> None:
		"""
		Cleanup when the connector object gets deleted
		"""
		self._backgroundScheduler.remove_all_jobs()
		self._backgroundScheduler.shutdown()

	async def adjustOrder(self, managed_trade: ManagedTrade, order: GenericOrder, price: float) -> bool:  # noqa: N802
		""" 
		Adjusts the given order with the given new price.
		For multileg orders, this method is not used as the MultilegOrderHandler
		handles all price adjustments internally during execution.
		"""
		# Multileg orders are adjusted internally by the MultilegOrderHandler
		if len(order.legs) > 1 or order.brokerSpecific.get('is_multileg'):
			logger.debug('Multileg order adjustments are handled internally by MultilegOrderHandler')
			return True
		
		if order.status == GenericOrderStatus.FILLED:
			logger.info('Order {} is already filled. Adjustment not required.', order)
			return True
		if order.status == GenericOrderStatus.CANCELLED:
			logger.info('Order {} is already cancelled. Adjustment not possible.', order)
			return True
		
		# For credit trades, the price must be negative
		if not managed_trade.long_legs_removed and (managed_trade.template.is_credit_trade() and order.price > 0) or (not managed_trade.template.is_credit_trade() and order.price < 0):
			price = -price
		
		previous_order_signal_id = order.brokerSpecific['order_signal']
		c2order: C2Order = order.brokerSpecific['c2order']
		
		# Adjust the price of the order
		if order.type == OrderType.LIMIT:
			c2order.Limit = str(price)
		elif order.type == OrderType.STOP:
			c2order.Stop = str(price)
		c2order.CancelReplaceSignalId = previous_order_signal_id

		data = {
            'Order': c2order.to_dict()
        }
		logger.debug(f'Payload: {data}')
		response = httpx.put(self._base_url + '/Strategies/ReplaceStrategyOrder', headers=self._http_headers, json=data)
		if response.status_code != status.HTTP_200_OK:
			logger.error('Failed to adjust order: {}', response.text)
			return False
		
		logger.debug(response.json())
		json_data = json.loads(response.text)
		response_status = json_data.get('ResponseStatus')
		if response_status.get('ErrorCode') != str(status.HTTP_200_OK):
			logger.error('Failed to adjust order!')
			return False
		
		# Signal speichern
		result = json_data.get('Results')[0]
		order_signal = result.get('SignalId')
		order.brokerSpecific['order_signal'] = order_signal
		logger.info(f'Order adjusted successfully. Previous Signal ID: {previous_order_signal_id} New Signal ID: {order_signal}')
		return True

	async def cancel_order(self, order: GenericOrder) -> None:
		"""
		Cancels the given order by sending a cancel signal to C2.
		
		For single-leg orders: Cancels the signal directly.
		For multileg orders: Cancels all pending leg signals.
		"""
		await super().cancel_order(order)
		
		# Check if this is a multileg order
		if order.brokerSpecific.get('is_multileg') or order.brokerSpecific.get('leg_signal_ids'):
			await self._cancel_multileg_order(order)
			return
		
		# Single-leg order cancellation
		signal_id = order.brokerSpecific.get('order_signal')
		if signal_id is None:
			logger.warning('Cannot cancel order - no signal ID found')
			return
		
		await self._cancel_signal(signal_id, order)
		order.status = GenericOrderStatus.CANCELLED
		self._emitOrderStatusEvent(order, OrderStatus.CANCELLED)
	
	async def _cancel_signal(self, signal_id: int, order: GenericOrder = None) -> bool:
		"""
		Cancels a C2 signal by sending a cancel request.
		
		Args:
			signal_id: The C2 signal ID to cancel
			order: Optional order for context in logging
			
		Returns:
			True if cancellation was successful
		"""
		data = {
			'SignalId': signal_id
		}
		
		try:
			logger.debug(f'Sending cancel request for signal {signal_id} to C2 API')
			response = httpx.post(
				self._base_url + '/Strategies/CancelStrategySignal',
				headers=self._http_headers,
				json=data
			)
			
			logger.debug(f'Cancel response: status={response.status_code}, body={response.text}')
			
			if response.status_code != status.HTTP_200_OK:
				logger.warning(f'Failed to cancel signal {signal_id}: HTTP {response.status_code} - {response.text}')
				return False
			
			json_data = json.loads(response.text)
			response_status = json_data.get('ResponseStatus')
			
			if response_status.get('ErrorCode') != str(status.HTTP_200_OK):
				error_msg = response_status.get('Message', 'Unknown error')
				logger.warning(f'Failed to cancel signal {signal_id}: {error_msg}')
				return False
			
			logger.info(f'Signal {signal_id} cancelled successfully')
			return True
			
		except Exception as e:
			logger.warning(f'Exception cancelling signal {signal_id}: {e}')
			return False
	
	async def _cancel_multileg_order(self, order: GenericOrder) -> None:
		"""
		Cancels a multileg order by cancelling all pending leg signals.
		This can be called during execution (via active_leg_orders) or after execution (via leg_signal_ids).
		Only cancels signals that are not yet filled.
		"""
		# If the order is already filled, don't try to cancel anything
		if order.status == GenericOrderStatus.FILLED:
			logger.debug('Multileg order already filled, nothing to cancel')
			return
		
		cancelled_count = 0
		cancelled_signal_ids = set()  # Track already cancelled signals to avoid duplicates
		
		# Check for active leg orders (during execution)
		active_leg_orders = order.brokerSpecific.get('active_leg_orders', [])
		for leg_order in active_leg_orders:
			if leg_order.signal_id and leg_order.signal_id not in cancelled_signal_ids:
				if leg_order.status not in [LegExecutionStatus.CANCELLED, LegExecutionStatus.FILLED]:
					logger.debug(f'Cancelling active leg signal {leg_order.signal_id} for {leg_order.leg.strike} {leg_order.leg.right}')
					if await self._cancel_signal(leg_order.signal_id, order):
						leg_order.status = LegExecutionStatus.CANCELLED
						cancelled_count += 1
					cancelled_signal_ids.add(leg_order.signal_id)
		
		# Check multileg_result if available (after partial execution) - only unfilled legs
		multileg_result = order.brokerSpecific.get('multileg_result')
		if multileg_result and hasattr(multileg_result, 'filled_legs'):
			# Note: filled_legs are already filled, don't cancel them
			# Only cancel pending legs from the result
			if hasattr(multileg_result, 'pending_legs'):
				for leg_order in multileg_result.pending_legs:
					if leg_order.signal_id and leg_order.signal_id not in cancelled_signal_ids:
						if leg_order.status not in [LegExecutionStatus.CANCELLED, LegExecutionStatus.FILLED]:
							if await self._cancel_signal(leg_order.signal_id, order):
								leg_order.status = LegExecutionStatus.CANCELLED
								cancelled_count += 1
							cancelled_signal_ids.add(leg_order.signal_id)
		
		order.status = GenericOrderStatus.CANCELLED
		self._emitOrderStatusEvent(order, OrderStatus.CANCELLED)
		logger.info(f'Multileg order cancelled ({cancelled_count} signals cancelled)')
	
	async def connect(self) -> None:
		"""
		Establish a connection to the C2 platform with the API key
		"""
		await super().connect()
		data = { 'Name': 'OptraBot'}
		connect_ok = False
		try:
			response = httpx.post(self._base_url + '/General/Hello', json=data, headers=self._http_headers)
		except Exception as excp:
			logger.error('Failed to connect to C2: {}', excp)
	
		if response.status_code != status.HTTP_200_OK:
			logger.error('Failed to connect to C2: {}', response.text)
			self._log_rate_limit_info(response)
		else:
			json_data = json.loads(response.text)
			#if json_data.get('message') != 'CONNECTION_ACCEPTED':
			results = json_data.get('Results')
			if results[0] == 'Hello, OptraBot!':
				connect_ok = True
				await self.set_trading_enabled(True, 'Broker connected')
			else:
				logger.error('Failed to connect to C2: Unexpected Results {}', results)
		
		if not connect_ok:
			self._emitConnectFailedEvent()
			self._connected = False
		else:
			self._connected = True
			self._emitConnectedEvent()

	def determine_expiration_date_by_dte(self, symbol: str, dte: int) -> date:
		"""
		Determines the expiration date based on the given DTE via the associated broker connector
		"""
		return self._broker_connector.determine_expiration_date_by_dte(symbol, dte)

	async def disconnect(self) -> None:
		# Wait for pending multileg operations to complete before disconnecting
		await self._await_pending_multileg_operations()
		await super().disconnect()
		self._connected = False
		await self.set_trading_enabled(False, 'Broker disconnected')

	async def _await_pending_multileg_operations(self, timeout: float = 10.0) -> None:
		"""
		Waits for all pending multileg operations to complete before shutdown.
		This ensures that leg cancellations and cleanup are completed properly.
		
		Args:
			timeout: Maximum time to wait for operations to complete (default 10 seconds)
		"""
		if not self._pending_multileg_tasks:
			return
		
		logger.debug(f'Waiting for {len(self._pending_multileg_tasks)} pending multileg operation(s) to complete...')
		
		try:
			# Wait for all pending tasks with a timeout
			if self._pending_multileg_tasks:
				done, pending = await asyncio.wait(
					self._pending_multileg_tasks,
					timeout=timeout,
					return_when=asyncio.ALL_COMPLETED
				)
				
				if pending:
					logger.warning(f'{len(pending)} multileg operation(s) did not complete within {timeout}s timeout')
					# Cancel remaining tasks
					for task in pending:
						task.cancel()
				else:
					logger.debug('All pending multileg operations completed')
		except Exception as e:
			logger.warning(f'Error waiting for pending multileg operations: {e}')

	async def eod_settlement_tasks(self) -> None:
		"""
		Perform End of Day settlement tasks
		"""
		pass

	def getAccounts(self) -> List[Account]:  # noqa: N802
		"""
		Returns the strategys managed by the user. The strategy ids is used as account ids
		"""
		if len(self._managedAccounts) == 0 and self.isConnected():
			for strategy_id in self._strategies:
				account = Account(id =strategy_id, name = strategy_id, broker = self.broker, pdt = False)
				self._managedAccounts.append(account)
		return self._managedAccounts

	def get_atm_strike(self, symbol:str) -> float:
		""" 
		Returns the ATM strike price for the given symbol based on the buffered option price data.
		If no data is available, it returns None.
		"""
		return self._broker_connector.get_atm_strike(symbol)

	def getFillPrice(self, order: GenericOrder) -> float:  # noqa: N802
		""" 
		Returns the fill price of the given order if it is filled
		"""
		return abs(order.averageFillPrice)
	
	def getLastPrice(self, symbol: str) -> float:  # noqa: N802
		""" 
		Returns the last price of the given symbol
		"""
		return self._broker_connector.getLastPrice(symbol)
	
	def get_last_option_price_update_time(self) -> dt.datetime:
		"""
		Returns the last update time of the option price data
		"""
		return self._broker_connector.get_last_option_price_update_time()

	def get_option_strike_data(self, symbol: str, expiration: dt.date) -> dict:
		"""
		Returns the option strike data for the given symbol and expiration date.
		"""
		return self._broker_connector.get_option_strike_data(symbol, expiration)

	def get_option_strike_price_data(self, symbol: str, expiration: dt.date, strike: float) -> OptionStrikePriceData:
		""" 
		Returns the option strike price data based on the real broker connector
		"""
		return self._broker_connector.get_option_strike_price_data(symbol, expiration, strike)

	def get_strike_by_delta(self, symbol: str, right: str, delta: int) -> float:
		""" 
		Returns the strike price based on the given delta using the real broker connector
		"""
		return self._broker_connector.get_strike_by_delta(symbol, right, delta)
	
	def get_strike_by_price(self, symbol: str, right: str, price: float) -> float:
		""" 
		Returns the strike price based on the given premium price based on the buffered option price data
		"""
		return self._broker_connector.get_strike_by_price(symbol, right, price)

	def isConnected(self) -> bool:  # noqa: N802
		return self._connected

	async def place_complex_order(self, take_profit_order: GenericOrder, stop_loss_order: GenericOrder, template: Template) -> bool:
		"""
		TWS doesn't support complex orders
		"""
		raise NotImplementedError()
	
	async def placeOrder(self, managed_trade: ManagedTrade, order: GenericOrder, parent_order: GenericOrder = None) -> None:  # noqa: N802
		""" 
		Places the given order for a managed account via the broker connection.
		For multileg orders (e.g., Iron Condors), the order is delegated to the MultilegOrderHandler
		which handles the sequential execution of individual legs.
		
		Raises:
			PlaceOrderException: If the order placement fails with a specific reason.
		"""
		# Check if this is a multileg order
		if len(order.legs) > 1:
			await self._place_multileg_order(managed_trade, order)
			return
		
		c2order: C2Order = order.brokerSpecific.get('c2order')
		if c2order is None:
			raise PlaceOrderException('Order not prepared', order)
		
		_ = order.legs[0]  # Leg reference available for future use
		c2order.OrderQuantity = order.quantity
		c2order.StrategyId = managed_trade.template.account
		if order.type == OrderType.LIMIT:
			c2order.Limit = str(order.price)
		elif order.type == OrderType.STOP:
			c2order.Stop = str(order.price)

		# Parent Signal Id if there is a parent order
		if parent_order is not None and order.type != OrderType.MARKET:   # Not use parent order for market orders now
			c2order.ParentSignalId = parent_order.brokerSpecific['order_signal']

		data = {
            'Order': c2order.to_dict()
        }
		logger.debug(f'Payload: {data}')
		response = httpx.post(self._base_url + '/Strategies/NewStrategyOrder', headers=self._http_headers, json=data)
		if response.status_code != status.HTTP_200_OK:
			raise PlaceOrderException(f'{response.text}', order)
		
		logger.debug(response.json())
		json_data = json.loads(response.text)
		response_status = json_data.get('ResponseStatus')
		if response_status.get('ErrorCode') != str(status.HTTP_200_OK):
			raise PlaceOrderException(f'Communication Error Code: {response_status.get("ErrorCode")} Message: {response_status.get("Message")}', order)
		
		# Signal speichern
		result = json_data.get('Results')[0]
		order_signal = result.get('SignalId')
		logger.info('Order placed successfully. Signal ID: {}', order_signal)
		order.brokerSpecific['c2order'] = c2order
		order.brokerSpecific['order_signal'] = order_signal
		self._orders.append(order)
	
	async def _place_multileg_order(self, managed_trade: ManagedTrade, order: GenericOrder) -> None:
		"""
		Places a multileg order (e.g., Iron Condor) by delegating to the MultilegOrderHandler.
		The handler executes legs sequentially in margin-aware order (long legs first for credit trades).
		
		Raises:
			PlaceOrderException: If the multileg order execution fails.
		"""
		# Initialize handler if not yet done
		if self._multileg_handler is None:
			self._multileg_handler = MultilegOrderHandler(self)
		
		logger.info(f'Placing multileg order with {len(order.legs)} legs via MultilegOrderHandler')
		
		# Set order status to OPEN immediately so it can be cancelled during shutdown
		order.status = OrderStatus.OPEN
		self._orders.append(order)
		self._emitOrderStatusEvent(order, OrderStatus.OPEN)
		
		# Create a trackable task for shutdown synchronization
		current_task = asyncio.current_task()
		if current_task:
			self._pending_multileg_tasks.add(current_task)
		
		# Execute multileg order
		try:
			result = await self._multileg_handler.execute_multileg_order(
				managed_trade=managed_trade,
				order=order
			)
		except asyncio.CancelledError:
			logger.warning('Multileg order execution cancelled during shutdown')
			raise PlaceOrderException('Order execution cancelled due to shutdown', order) from None
		finally:
			# Remove task from pending set when done
			if current_task and current_task in self._pending_multileg_tasks:
				self._pending_multileg_tasks.discard(current_task)
		
		if not result.success:
			error_msg = f'Multileg order execution failed: {result.error_message}'
			if result.partial_fill:
				error_msg += f' (Partial fill: {len(result.filled_legs)}/{len(order.legs)} legs filled, rollback performed)'
			raise PlaceOrderException(error_msg, order)
		
		# Store execution info in order
		order.brokerSpecific['multileg_result'] = result
		order.brokerSpecific['leg_signal_ids'] = [leg.signal_id for leg in result.filled_legs]
		
		# The total fill price was already calculated by MultilegOrderHandler
		# using _calculate_total_fill_price() which correctly handles long/short legs
		# order.averageFillPrice was also set by the handler
		
		# Mark order as filled and emit status event
		order.status = GenericOrderStatus.FILLED
		self._emitOrderStatusEvent(order, OrderStatus.FILLED, filledAmount=order.quantity)
		
		logger.info(f'Multileg order executed successfully. Total price: ${order.averageFillPrice:.2f}')
		# Note: Order was already added to _orders at start of execution
	
	async def prepareOrder(self, order: GenericOrder, need_valid_price_data: bool = True) -> None:  # noqa: N802
		"""
		Prepares the given order for execution.
		- Retrieve current market data for order legs

		Raises:
			PrepareOrderException: If the order preparation fails with a specific reason.
		"""
		# Handle multileg orders
		if len(order.legs) > 1:
			await self._prepare_multileg_order(order, need_valid_price_data)
			return
		
		symbol_information = symbol_info.symbol_infos[order.symbol]
		leg = order.legs[0]
		if need_valid_price_data:
			strike_price_data = self._broker_connector.get_option_strike_price_data(order.symbol, leg.expiration, leg.strike)
			if not strike_price_data.is_outdated():
				leg.askPrice = strike_price_data.putAsk if leg.right == OptionRight.PUT else strike_price_data.callAsk
				leg.bidPrice = strike_price_data.putBid if leg.right == OptionRight.PUT else strike_price_data.callBid
			else:
				raise PrepareOrderException(f'Price data for strike {leg.strike} is outdated', order)
		
		c2order = C2Order(self._map_order_type(order.type), side=self._map_order_side(leg.action))

		c2order.ExchangeSymbol = C2ExchangeSymbol(symbol_information.trading_class, 'OPT', leg.right, leg.strike)
		c2order.ExchangeSymbol.MaturityMonthYear = leg.expiration.strftime('%Y%m%d')
		order.brokerSpecific['c2order'] = c2order
		order.determine_price_effect()
	
	async def _prepare_multileg_order(self, order: GenericOrder, need_valid_price_data: bool = True) -> None:
		"""
		Prepares a multileg order (e.g., Iron Condor) for execution.
		Retrieves market data for all legs and prepares C2 orders for each leg.
		
		Raises:
			PrepareOrderException: If the order preparation fails.
		"""
		symbol_information = symbol_info.symbol_infos[order.symbol]
		
		for leg in order.legs:
			if need_valid_price_data:
				strike_price_data = self._broker_connector.get_option_strike_price_data(
					order.symbol, leg.expiration, leg.strike
				)
				if not strike_price_data.is_outdated():
					leg.askPrice = strike_price_data.putAsk if leg.right == OptionRight.PUT else strike_price_data.callAsk
					leg.bidPrice = strike_price_data.putBid if leg.right == OptionRight.PUT else strike_price_data.callBid
				else:
					raise PrepareOrderException(f'Price data for strike {leg.strike} is outdated', order)
			
			# Create C2 order for each leg
			c2order = C2Order(self._map_order_type(order.type), side=self._map_order_side(leg.action))
			c2order.ExchangeSymbol = C2ExchangeSymbol(symbol_information.trading_class, 'OPT', leg.right, leg.strike)
			c2order.ExchangeSymbol.MaturityMonthYear = leg.expiration.strftime('%Y%m%d')
			# Store C2 order in leg's extra data
			if not hasattr(leg, 'brokerSpecific'):
				leg.brokerSpecific = {}
			leg.brokerSpecific['c2order'] = c2order
		
		# Mark order as multileg for handler
		order.brokerSpecific['is_multileg'] = True
		order.determine_price_effect()

	async def requestTickerData(self, symbols: List[str]) -> None:  # noqa: N802
		""" 
		Request ticker data for the given symbols and their options
		"""
		pass

	async def unsubscribe_ticker_data(self) -> None:
		return await super().unsubscribe_ticker_data()

	def _log_rate_limit_info(self, response: httpx.Response) -> None:
		"""
		Logs the rate limit information from the response
		"""
		rate_limit = response.headers.get('X-Limit-Limit')
		rate_limit_type = response.headers.get('X-Limit-Type')
		rate_limit_remaining = response.headers.get('X-Limit-Remaining')
		rate_limit_reset = response.headers.get('X-Limit-Reset')
		logger.debug(f'Rate Limit: {rate_limit}/{rate_limit_type} Remaining: {rate_limit_remaining} Reset: {rate_limit_reset}')

	async def _track_orders(self) -> None:
		"""
		Tracks active Orders status at Collective2
		"""
		try:
			if not self.isConnected():
				return
			
			open_orders = any(order.status == OrderStatus.OPEN for order in self._orders)
			if not open_orders:
				return

			self._backgroundScheduler.reschedule_job('_track_signals', trigger=IntervalTrigger(seconds=60)) # Postpone the next run
			account_index = 0
			start_date = self._start_date.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
			for account in self._managedAccounts:
				account_index += 1
				if account_index > 1:
					await asyncio.sleep(5)  # wait 5 second between account requests to avoid rate limiting
				logger.debug(f'Checking orders for strategy {account.id}')
				query = {
							'StrategyId' : account.id,
							'StartDate' : start_date
						}
				try:
					response = httpx.get(self._base_url + '/Strategies/GetStrategyHistoricalOrders', headers=self._http_headers, params=query)
				except Exception as excp:
					logger.error('C2 HTTP request GetStrategyHistoricalOrders failed: {}', excp)
					continue

				if response.status_code != status.HTTP_200_OK:
					logger.error('Failed to get order status: {}', response.text)
					self._log_rate_limit_info(response)
					continue
			
				json_data = json.loads(response.text)
				results = json_data.get('Results')
				if len(results) == 0:
					continue
				else:
					logger.debug(f'Received {len(results)} orders for strategy {account.id}')
			
				for order in self._orders:
					if order.status == OrderStatus.OPEN:
						# Skip multileg orders - they are tracked via their individual leg signals
						if order.brokerSpecific.get('is_multileg'):
							continue
						order_signal = order.brokerSpecific.get('order_signal')
						if not order_signal:
							continue
						for result in results:
							if result.get('SignalId') == order_signal:
								order_status = result.get('OrderStatus')
								if order_status == '2': # Order filled
									filled_quantity = result.get('FilledQuantity')
									order.averageFillPrice = result.get('AvgFillPrice')
									self._emitOrderStatusEvent(order, OrderStatus.FILLED, filledAmount=filled_quantity)
								if order_status == '4':
									self._emitOrderStatusEvent(order, OrderStatus.CANCELLED)
		except asyncio.exceptions.CancelledError:
			logger.warning('Track Orders Task was cancelled!')
	
		# Schedule the next run in 5 seconds
		self._backgroundScheduler.reschedule_job('_track_signals', trigger=IntervalTrigger(seconds=5))

	def _map_order_side(self, action: OrderAction) -> C2OrderSide:
		"""
		Maps the action from a generic order to the C2 order side
		"""
		match action:
			case OrderAction.BUY:
				return C2OrderSide.BUY
			case OrderAction.BUY_TO_CLOSE:
				return C2OrderSide.BUY
			case OrderAction.SELL:
				return C2OrderSide.SELL
			case OrderAction.SELL_TO_CLOSE:
				return C2OrderSide.SELL
			case _:
				logger.error('Unsupported order action {}', action)
				return None

	def _map_order_type(self, order_type: OrderType) -> C2OrderType:
		"""
		Maps the order type from the generic order to the C2 order type
		"""
		match order_type:
			case OrderType.MARKET:
				return C2OrderType.MARKET
			case OrderType.LIMIT:
				return C2OrderType.LIMIT
			case OrderType.STOP:
				return C2OrderType.STOP
			case _:
				logger.error('Unsupported order type {}', order_type)
				return None

	def _get_osi_month(self, month: int, right: OptionRight) -> str:
		"""
		Returns the month code according to OSI based on the month and the option right.
		Reference: https://www.collective2.com/options
		"""
		match month:
			case 1:
				return 'A' if right == OptionRight.CALL else 'M'
			case 2:
				return 'B' if right == OptionRight.CALL else 'N'
			case 3:
				return 'C' if right == OptionRight.CALL else 'O'
			case 4:
				return 'D' if right == OptionRight.CALL else 'P'
			case 5:
				return 'E' if right	== OptionRight.CALL else 'Q'
			case 6:
				return 'F' if right == OptionRight.CALL else 'R'
			case 7:
				return 'G' if right == OptionRight.CALL else 'S'
			case 8:
				return 'H' if right == OptionRight.CALL else 'T'
			case 9:
				return 'I' if right == OptionRight.CALL else 'U'
			case 10:
				return 'J' if right == OptionRight.CALL else 'V'
			case 11:
				return 'K' if right == OptionRight.CALL else 'W'
			case 12:
				return 'L' if right == OptionRight.CALL else 'X'
			case _:
				logger.error('Unsupported month {}', month)
				return None