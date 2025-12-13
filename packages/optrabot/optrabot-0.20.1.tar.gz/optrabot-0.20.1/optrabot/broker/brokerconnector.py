import datetime as dt
from abc import ABC, abstractmethod
from bisect import bisect_left
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, final

from eventkit import Event
from loguru import logger

import optrabot.symbolinfo as symbolInfo
from optrabot.broker.optionpricedata import (OptionStrikeData,
                                             OptionStrikePriceData)
from optrabot.broker.order import Execution, OptionRight
from optrabot.broker.order import Order as GenericOrder
from optrabot.broker.order import OrderStatus
from optrabot.config import Config
from optrabot.exceptions import PlaceOrderException
from optrabot.managedtrade import ManagedTrade
from optrabot.models import Account
from optrabot.optionhelper import OptionHelper
from optrabot.tradetemplate.templatefactory import Template


@dataclass
class SymbolData:
	"""
	Holds symbol specific data which are common for all broker connectors
	"""
	def __init__(self):
		self.symbol: str = None
		self.expirations: List[dt.date] = []
		self.lastPrice: float = 0
		self.lastAtmStrike: float = 0
		self.noPriceDataCount = 0
		self.trade_options: bool = True		# True if options trading is enabled for the symbol
		self.dte_expiration_map: Dict[int, dt.date] = {}		# Maps DTE to expiration date
		self.strikes: List[float] = []
		self.optionPriceData: Dict[dt.date, OptionStrikeData] = {}

class BrokerConnector(ABC):
	# Constants for Events
	EVENT_CONNECTED = 'connectedEvent'
	EVENT_CONNECT_FAILED = 'connectFailedEvent'
	EVENT_COMMISSION_REPORT = 'commissionReportEvent'
	EVENT_DISCONNECTED = 'disconnectedEvent'
	EVENT_ORDER_STATUS = 'orderStatusEvent'
	EVENT_ORDER_EXEC_DETAILS = 'orderExecutionDetailsEvent'
	EVENT_BID_ASK_SPREAD_WARNING = 'bidAskSpreadWarningEvent'

	def __init__(self) -> None:
		self._initialized = False
		self._createEvents()
		self.id = None		# ID of the connector
		self.broker = None	# ID of the broker
		self._tradingEnabled = False
		self._managedAccounts: List[Account] = []
		self._last_option_price_update_time: dt.datetime = None
		self._dtes : List[int] = []		# Configured DTEs for option data requests
		self._symbolData: Dict[str, SymbolData] = {}
		self._subscribed_ticker_data = False
		# Multileg order handling capabilities
		self._supports_multileg_orders = True	# True = Broker can process multileg orders natively
		self._internal_order_adjustment = False	# True = Connector handles order adjustments internally
		pass
	
	@abstractmethod
	async def cancel_order(self, order: GenericOrder):
		"""
		Cancels the given order
		"""
		pass

	@abstractmethod
	async def connect(self):
		""" 
		Establishes a connection to the broker
		"""
		logger.info('Connecting with broker {}', self.id)

	@abstractmethod
	async def disconnect(self):
		""" 
		Disconnects from the broker
		"""
		await self.unsubscribe_ticker_data()
		logger.info('Disconnecting from broker {}', self.id)

	@abstractmethod
	def isConnected(self) -> bool:
		""" 
		Returns True if the broker is connected
		"""
		pass

	@abstractmethod
	def getAccounts(self) -> List[Account]:
		""" 
		Returns the accounts managed by the broker connection
		"""
		pass

	def get_atm_strike(self, symbol:str) -> float:
		""" 
		Returns the ATM strike price for the given symbol based on the buffered option price data.
		If no data is available, it returns None.
		"""
		symbolData = self._symbolData[symbol]
		return symbolData.lastAtmStrike
	
	@abstractmethod
	async def prepareOrder(self, order: GenericOrder, need_valid_price_data: bool = True) -> None:
		"""
		Prepares the given order for execution.
		- Retrieve current market data for order legs

		Raises:
			PrepareOrderException: If the order preparation fails with a specific reason.
		"""

	def oco_as_complex_order(self) -> bool:
		""" 
		Returns True if the broker connection supports OCO orders in form of one complex order
		instead of two single orders
		"""
		return False

	def supports_multileg_orders(self) -> bool:
		"""
		Returns True if the broker can process multileg orders natively (e.g., spreads, iron condors).
		If False, the connector must split multileg orders into individual leg orders.
		"""
		return self._supports_multileg_orders

	def handles_adjustments_internally(self) -> bool:
		"""
		Returns True if the connector handles order price adjustments internally.
		When True, the TradeManager should not call adjustOrder() for this connector.
		This is typically used when the connector splits multileg orders into individual legs
		and needs to adjust each leg independently.
		"""
		return self._internal_order_adjustment

	@abstractmethod
	async def placeOrder(self, managed_trade: ManagedTrade, order: GenericOrder, parent_order: GenericOrder = None) -> None:
		""" 
		Places the given order for a managed account via the broker connection.
		
		Raises:
			PlaceOrderException: If the order placement fails with a specific reason.
		"""
		pass

	@abstractmethod
	async def place_complex_order(self, take_profit_order: GenericOrder, stop_loss_order: GenericOrder, template: Template) -> bool:
		""" 
		Places Take Profit and Stop Loss Order as single complex order
		"""
		pass

	@abstractmethod
	async def adjustOrder(self, managed_trade: ManagedTrade, order: GenericOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		pass

	@abstractmethod
	async def requestTickerData(self, symbols: List[str]) -> None:
		""" 
		Request ticker data for the given symbols and their options
		"""
		pass

	@abstractmethod
	def getFillPrice(self, order: GenericOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		pass

	def getLastPrice(self, symbol: str) -> float:
		""" 
		Returns the last price of the given symbol
		"""
		pass

	@abstractmethod
	def get_option_strike_data(self, symbol: str, expiration: date) -> OptionStrikeData:
		""" 
		Returns the option strike data for the given symbol and expiration. It is including
		prices and greeks.
		"""
		pass

	@abstractmethod
	def get_option_strike_price_data(self, symbol: str, expiration: date, strike: float) -> OptionStrikePriceData:
		""" 
		Returns the option strike price data for the given symbol, expiration, strike and right
		"""
		pass

	def get_last_option_price_update_time(self) -> dt.datetime:
		"""
		Returns the last update time of the option price data
		"""
		return self._last_option_price_update_time

	@abstractmethod
	def get_strike_by_delta(self, symbol: str, right: str, delta: int) -> float:
		""" 
		Returns the strike price based on the given delta based on the buffered option price data
		"""
		raise NotImplementedError()
	
	@abstractmethod
	def get_strike_by_price(self, symbol: str, right: str, price: float) -> float:
		""" 
		Returns the strike price based on the given premium price based on the buffered option price data
		"""
		raise NotImplementedError()

	def get_min_price_increment(self, price: float) -> float:
		""" 
		Returns the minimum price increment for the given option based on the given price.
		It's based on the information from Tastytrade Help Center article: https://support.tastytrade.com/support/s/solutions/articles/43000435374
		"""
		if price < 3:
			return 0.05
		else:
			return 0.1

	@abstractmethod
	async def eod_settlement_tasks(self) -> None:
		"""
		Perform End of Day settlement tasks
		"""
		pass

	@final
	def set_dtes(self, dtes: List[int]):
		"""
		Sets the configured DTEs for option data requests
		"""
		self._dtes = dtes

	def determine_expiration_date_by_dte(self, symbol: str, dte: int) -> date:
		""" 
		Determines the expiration date for the given symbol based on the given DTE
		"""
		symbolData = self._symbolData[symbol]
		try:
			return symbolData.dte_expiration_map[dte]
		except KeyError:
			return None

	def _determine_relevant_expirations(self, symbolData: SymbolData) -> List[dt.date]:
		"""
		Determines the relevant option expirations for the given symbol data based on the current date and the days to expiration (DTE)
		"""
		current_date = dt.date.today()
		relevant_expirations = []
		for dte in self._dtes:
			# Calculate the expiration date based on the DTE and check if there is an expiration with this DTE, otherwise use the next available expiration
			closest_expiration = None
			for expiration in symbolData.expirations:
				diff = (expiration - current_date).days
				if diff >= dte:
					closest_expiration = expiration
					symbolData.dte_expiration_map[dte] = closest_expiration		# Store mapping of DTE to expiration date
					break
			if closest_expiration and closest_expiration not in relevant_expirations:
				relevant_expirations.append(closest_expiration)
		return relevant_expirations
	
	def _determine_strikes_of_interest(self, symbolData: SymbolData, atmStrike: float) -> List[float]:
		"""
		Determines the strikes of interest based on the given ATM strike price
		"""
		# Die 40 Strikes um den ATM Strike herum abfragen
		number_of_strikes_above = 45
		number_of_strikes_below = 45
		pos = bisect_left(symbolData.strikes, atmStrike)
		lower_bound = max(0, pos - number_of_strikes_below)
		upper_bound = min(len(symbolData.strikes), pos + number_of_strikes_above)
		return symbolData.strikes[lower_bound:upper_bound]
	
	def uses_oco_orders(self) -> bool:
		""" 
		Returns True if the broker connection supports and uses OCO orders for managing take profit and stop loss
		"""
		return False

	def _createEvents(self):
		""" 
		Creates the events for the broker connection
		"""
		self.connectedEvent = Event(self.EVENT_CONNECTED)
		self.disconnectedEvent = Event(self.EVENT_DISCONNECTED)
		self.commissionReportEvent = Event(self.EVENT_COMMISSION_REPORT)
		self.connectFailedEvent = Event(self.EVENT_CONNECT_FAILED)
		self.orderStatusEvent = Event(self.EVENT_ORDER_STATUS)
		self.orderExecutionDetailsEvent = Event(self.EVENT_ORDER_EXEC_DETAILS)
		self.bid_ask_spread_warning_event = Event(self.EVENT_BID_ASK_SPREAD_WARNING)

	def _emit_bid_ask_spread_warning_event(self, symbol: str, strike: float, right: OptionRight, bid_price: float, ask_price: float, spread: float, max_allowed_spread: float) -> None:
		""" 
		Emits the bid-ask spread warning event
		"""
		self.bid_ask_spread_warning_event.emit(symbol, strike, right, bid_price, ask_price, spread, max_allowed_spread)

	def _emitConnectedEvent(self):
		""" 
		Emits the connected event
		"""
		self.connectedEvent.emit(self)

	def _emitDisconnectedEvent(self):
		""" 
		Emits the disconnected event
		"""
		self._managedAccounts = []
		self.disconnectedEvent.emit(self)

	def _emitConnectFailedEvent(self):
		""" 
		Emits the broker connect failed event
		"""
		self.connectFailedEvent.emit(self)

	def _emitCommissionReportEvent(self, order: GenericOrder, execution_id: str, commission: float = 0, fee: float = 0):
		"""
		Emits the commission report event if commission and fee information are delivered
		for a execution which previously has been reported with the according execution_id.
		"""
		self.commissionReportEvent.emit(order, execution_id, commission, fee)

	def _emitOrderExecutionDetailsEvent(self, order: GenericOrder, execution: Execution):
		""" 
		Emits the order execution details event
		"""
		self.orderExecutionDetailsEvent.emit(order, execution)

	def _emitOrderStatusEvent(self, order: GenericOrder, status: OrderStatus, filledAmount: int = 0):
		""" 
		Emits the order status event. Filled amount holds the amount that has been filled with this
		order status change, if the status event is a "Filled" event.
		"""
		self.orderStatusEvent.emit(order, status, filledAmount)

	async def _monitor_bid_ask_spread(self, option_strike_price_data: OptionStrikePriceData, generic_symbol: str, strike: float) -> None:
		""" 
		Monitors the bid-ask spread of the option price data for the given symbol and strike. It sends a warning notification if the spread is too high.
		"""
		call_ask_price = option_strike_price_data.callAsk if option_strike_price_data.callAsk is not None and not OptionHelper.isNan(option_strike_price_data.callAsk) and option_strike_price_data.callAsk >= 0 else 0
		call_bid_price = option_strike_price_data.callBid if option_strike_price_data.callBid is not None and not OptionHelper.isNan(option_strike_price_data.callBid) and option_strike_price_data.callBid >= 0 else 0
		put_ask_price = option_strike_price_data.putAsk if option_strike_price_data.putAsk is not None and not OptionHelper.isNan(option_strike_price_data.putAsk) and option_strike_price_data.putAsk >= 0 else 0
		put_bid_price = option_strike_price_data.putBid if option_strike_price_data.putBid is not None and not OptionHelper.isNan(option_strike_price_data.putBid) and option_strike_price_data.putBid >= 0 else 0

		# Check Call Spread
		if call_ask_price > 0.30 and call_bid_price > 0:
				spread = round(call_ask_price - call_bid_price, 2)
				max_allowed_spread = call_bid_price * 2
				if spread > max_allowed_spread:
					self._emit_bid_ask_spread_warning_event(symbol=generic_symbol, strike=strike, right=OptionRight.CALL, bid_price=call_bid_price, ask_price=call_ask_price, spread=spread, max_allowed_spread=max_allowed_spread)
		
		# Check Put Spread
		if put_ask_price > 0.30 and put_bid_price > 0:
				spread = round(put_ask_price - put_bid_price, 2)
				max_allowed_spread = put_bid_price * 2
				if spread > max_allowed_spread:
					self._emit_bid_ask_spread_warning_event(symbol=generic_symbol, strike=strike, right=OptionRight.PUT, bid_price=put_bid_price, ask_price=put_ask_price, spread=spread, max_allowed_spread=max_allowed_spread)

	def isInitialized(self) -> bool:
		""" 
		Returns True if the broker connector is initialized
		"""
		return self._initialized

	def isTradingEnabled(self) -> bool:
		""" 
		Returns True if trading is enabled
		"""
		return self._tradingEnabled
	
	async def set_trading_enabled(self, enabled: bool, reason: str = None):
		""" 
		Sets the trading enabled flag with an optional reason which is being logged
		"""
		from optrabot.broker.brokerfactory import BrokerFactory
		self._tradingEnabled = enabled
		if reason:
			logger.debug('Trading enabled: {} - Reason: {}', enabled, reason)
			if enabled == False and not BrokerFactory().is_shutting_down() and BrokerFactory().is_market_open():
				from optrabot.tradinghubclient import NotificationType, TradinghubClient
				notification_message = '‼️ Trading with broker ' + self.broker + ' has been disabled'
				if reason:
					notification_message += ' due to: ' + reason 
				notification_message += '!'
				await TradinghubClient().send_notification(NotificationType.WARN, notification_message) 
				logger.error('Trading has been disabled: {}', reason)
		else:
			logger.debug('Trading enabled: {}', enabled)

	@abstractmethod
	async def unsubscribe_ticker_data(self):
		"""
		Unsubscribes from all ticker data from the broker
		"""
		logger.debug(f'Unsubscribing from all ticker data for broker {self.id}')
		self._subscribed_ticker_data = False