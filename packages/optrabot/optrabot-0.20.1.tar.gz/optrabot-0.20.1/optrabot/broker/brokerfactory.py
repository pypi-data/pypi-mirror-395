import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

import pandas_market_calendars as mcal
import pytz
from eventkit import Event
from loguru import logger
from sqlalchemy.orm import Session

import optrabot.config as optrabotcfg
from optrabot import crud, schemas
from optrabot.broker.brokerconnector import BrokerConnector
from optrabot.broker.c2connector import C2Connector
from optrabot.broker.ibtwsconnector import IBTWSTConnector
from optrabot.broker.order import Execution, OptionRight, Order, OrderStatus
from optrabot.broker.tastytradeconnector import TastytradeConnector
from optrabot.database import get_db_engine
from optrabot.models import Account
from optrabot.util.singletonmeta import SingletonMeta


class BrokerFactory(metaclass=SingletonMeta):
	def __init__(self):
		self._connectors: Dict[str, BrokerConnector] = {}
		self.orderStatusEvent = Event('orderStatusEvent')
		self.commissionReportEvent = Event('commissionReportEvent')
		self.orderExecutionDetailsEvent = Event('orderExecutionDetailsEvent')
		self._symbols = ['SPX', 'VIX']
		self._shutingdown = False
		self._session_pre : datetime = None
		self._session_start : datetime = None
		self._session_end : datetime = None
		self._session_price_end : datetime = None
		self._expired_trades_settled = False  # OTB-253: Flag to settle expired trades only once
		self._expired_trades_lock = asyncio.Lock()  # Lock for expired trades settlement
		self._brokers_recovered = set()  # Track which brokers have completed recovery
		self._last_bid_ask_spread_warning_time: datetime = None  # Rate limit for bid/ask spread warnings
		self.update_trading_session_data()

	async def createBrokerConnectors(self):
		""" Creates broker connections from the given configuration
		"""
		twsConnector = IBTWSTConnector()
		if twsConnector.isInitialized():
			self._connectors[twsConnector.id] = twsConnector
		tastyConnector = TastytradeConnector()
		if tastyConnector.isInitialized():
			self._connectors[tastyConnector.id] = tastyConnector
		c2Connector = C2Connector()
		if c2Connector.isInitialized():
			self._connectors[c2Connector.id] = c2Connector
		
		logger.debug(f'Configured brokers: {len(self._connectors)} ({", ".join(self._connectors.keys())})')
		
		for value in self._connectors.values():
			connector : BrokerConnector = value
			connector.connectedEvent += self._onBrokerConnected
			connector.commissionReportEvent += self._onCommissionReport
			connector.disconnectedEvent += self._onBrokerDisconnected
			connector.connectFailedEvent += self._onBrokerConnectFailed
			connector.orderStatusEvent += self._onOrderStatus
			connector.orderExecutionDetailsEvent += self._onOrderExecutionDetailsEvent
			connector.bid_ask_spread_warning_event += self._on_bid_ask_spread_warning_event
			await connector.connect()

	def check_accounts_after_all_brokers_connected(self):
		"""
		Checks if the accounts configured in the trade template are available in the broker connections.
		If not all connectors are connected yet, this method does nothing.
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig

		all_accounts = []
		for connector in self._connectors.values():
			if not connector.isConnected():
				return
			else:
				all_accounts += connector.getAccounts()

		tradeTemplates = config.getTemplates()	
		for template in tradeTemplates:
			if template.account:
				accountFound = False
				for account in all_accounts:
					if account.id == template.account:
						accountFound = True
						break
				if not accountFound:
					logger.error(f'Account {template.account} configured in Trade Template {template.name} is not available in any connected Broker!')

	async def check_price_data(self):
		"""
		Checks if the connected brokers are still delivering price data during the trading session
		"""
		now = datetime.now(pytz.timezone('US/Eastern'))
		if self._session_start and self._session_end:
			if now >= self._session_start + timedelta(seconds=30) and now <= self._session_price_end:
				logger.debug('Checking price data are up-to-date for the connected brokers')
				for connector in self.get_broker_connectors().values():
					if connector.isConnected():
						last_update_time = connector.get_last_option_price_update_time()
						if last_update_time is None or (now - last_update_time).total_seconds() > 30:
							if last_update_time is None:
								last_update_time_str = 'Never'
							else:
								last_update_time_str = last_update_time.strftime('%Y-%m-%d %H:%M:%S %Z')
							from optrabot.tradinghubclient import NotificationType, TradinghubClient
							message = f'Price data for {connector.broker} is not up-to-date! Last update: {last_update_time_str}'
							await TradinghubClient().send_notification(NotificationType.WARN, f'⚠️ {message}')
							logger.warning(message)
						else:
							last_update_time_str = last_update_time.strftime('%Y-%m-%d %H:%M:%S %Z')
							logger.debug(f'Price data for {connector.broker} is up-to-date. Last update: {last_update_time_str}')

	async def new_day_start(self):
		"""
		Called when a new day starts
		"""
		for value in self._connectors.values():
			connector : BrokerConnector = value
			# Request ticker data for the new day
			if connector.isConnected():
				await self._request_ticker_data(connector, self._symbols)
			else:
				logger.warning(f'Broker {connector.broker} is not connected yet. Not requesting ticker data now.')

		self.update_trading_session_data()

	def get_broker_connectors(self) -> Dict[str, BrokerConnector]:
		"""
		Returns the broker connectors
		"""
		return self._connectors

	def getBrokerConnectorByAccount(self, account: str) -> BrokerConnector:
		""" Returns the broker connector for the given account
		"""
		for value in self._connectors.values():
			connector : BrokerConnector = value
			accounts = connector.getAccounts()
			for acc in accounts:
				if acc.id == account:
					return connector
		return None
	
	def get_connector_by_id(self, id: str) -> BrokerConnector:
		""" 
		Returns the broker connector for the given id
		"""
		return self._connectors.get(id)
	
	def get_trading_satus_info(self) -> tuple[str, bool]:
		""" 
		Returns a tuple with the status string and a boolean indicating if all brokers have trading enabled
		
		Returns:
			tuple[str, bool]: (status_string, all_trading_enabled)
		"""
		status = ''
		all_trading_enabled = True
		for value in self._connectors.values():
			connector : BrokerConnector = value
			connector_trading_enabled = connector.isTradingEnabled()
			status += f'{connector.broker}: {"Yes" if connector_trading_enabled else "No"} '
			if not connector_trading_enabled:
				all_trading_enabled = False
		return status, all_trading_enabled
	
	def is_market_open(self) -> bool:
		""" 
		Returns True if the market is open
		"""
		if self._session_start and self._session_end:
			now = datetime.now(pytz.timezone('America/New_York'))
			if now >= self._session_start and now <= self._session_end:
				return True
		return False
	
	def is_pre_market(self) -> bool:
		"""
		Returns True if the market is in pre-market session
		"""
		if self._session_pre and self._session_start:
			now = datetime.now(pytz.timezone('America/New_York'))
			if now >= self._session_pre and now < self._session_start:
				return True
		return False
	
	def is_trading_day(self) -> bool:
		"""
		Returns True if today is a trading day
		"""
		if self._session_start == None and self._session_end == None:
			return False
		return True

	def is_shutting_down(self) -> bool:
		""" 
		Returns True if the BrokerFactory is shutting down
		"""
		return self._shutingdown

	def update_trading_session_data(self):
		try:
			cme = mcal.get_calendar('CBOE_Index_Options')
			now = datetime.now(pytz.timezone('America/New_York'))
			today_schedule = cme.schedule(start_date=now.date(), end_date=now.date())

			if today_schedule.empty:
				self._session_start = None
				self._session_end = None
				self._session_price_end = None
				self._session_pre = None
				logger.info('No trading session today.')
			else:
				self._session_pre = today_schedule.iloc[0]['market_open'] - timedelta(hours=9)
				self._session_start = today_schedule.iloc[0]['market_open']
				self._session_end = today_schedule.iloc[0]['market_close']
				self._session_price_end = self._session_end - timedelta(minutes=self._session_end.minute) if self._session_end.minute > 0 else self._session_end
				formatted_session_start_time = self._session_start.strftime('%H:%M:%S %Z')
				formatted_session_end_time = self._session_end.strftime('%H:%M:%S %Z')
				logger.info(f'Today trading - Session start: {formatted_session_start_time} Session end: {formatted_session_end_time}')
		except Exception as e:
			logger.error(f'Error while determining trading session start and end: {e}')

	async def _onBrokerConnected(self, brokerConnector: BrokerConnector):
		""" 
		Called when a broker connection has been established
		the BrokerConnector object is passed as parameter
		"""
		logger.info('Broker {} connected successfully.', brokerConnector.id)
		
		try:
			accounts = brokerConnector.getAccounts()
			self._updateAccountsInDatabase(accounts)
		except Exception as e:
			logger.error(f'Failed to get accounts from broker {brokerConnector.id}: {e}')
			logger.warning(f'Trade Recovery skipped for broker {brokerConnector.id} due to account retrieval failure')
			return

		self.check_accounts_after_all_brokers_connected()

		# OTB-253: Request ticker data FIRST - symbol data is needed for trade recovery
		# prepareOrder() during recovery requires self._symbolData[symbol] to exist
		# For TASTY: Symbol data creation is fast, subscribe runs in background (non-blocking)
		# For IBTWS: Symbol data creation is fast, qualification/chains load in parallel
		try:
			await self._request_ticker_data(brokerConnector, self._symbols)
		except Exception as e:
			logger.error(f'Failed to request ticker data from broker {brokerConnector.id}: {e}')
			logger.warning(f'Broker {brokerConnector.id} reconnection incomplete - ticker data unavailable')
			# Don't return - allow trade recovery to proceed even without fresh ticker data
			# Existing symbol data may still be available from before disconnect

		# OTB-253: Per-broker trade recovery
		# Each broker runs its own recovery for its accounts independently
		# No waiting for other brokers - if one fails to connect, others still recover
		# Runs AFTER requestTickerData() so symbol data is available for prepareOrder()
		if len(accounts) > 0:
			# Step 1: Settle expired trades (only once, by first broker to connect)
			async with self._expired_trades_lock:
				if not self._expired_trades_settled:
					self._expired_trades_settled = True
					logger.info("Settling expired trades (triggered by first connected broker)")
					try:
						from optrabot.traderecovery import TradeRecoveryService
						recovery = TradeRecoveryService()
						await recovery.settle_expired_trades()
					except Exception as e:
						logger.error(f'Expired trades settlement failed: {e}')
						# Don't reset flag - we don't want to retry settling expired trades
						# They will be caught on next restart
			
			# Step 2: Recover active trades for this specific broker
			if brokerConnector.id not in self._brokers_recovered:
				self._brokers_recovered.add(brokerConnector.id)
				account_ids = [acc.id for acc in accounts]
				
				try:
					from optrabot.traderecovery import TradeRecoveryService
					recovery = TradeRecoveryService()
					await recovery.recover_for_broker(brokerConnector.id, account_ids)
				except Exception as e:
					logger.error(f'Trade Recovery failed for broker {brokerConnector.id}: {e}')
					# Remove from recovered set so it can be retried
					self._brokers_recovered.discard(brokerConnector.id)
					raise

	async def _request_ticker_data(self, connector: BrokerConnector, symbols: List[str]):
		"""
		Requests ticker data for the given symbols from the given connector and the given days to expirations (dtes).
		Implements retry logic for connection timeouts (e.g., after streamer reconnection).
		"""
		# Obtain DTEs from the configured trade templates
		dtes: List[int] = [0] # Always request 0DTE data
		config: optrabotcfg.Config = optrabotcfg.appConfig
		tradeTemplates = config.getTemplates()
		for template in tradeTemplates:
			if template.dte and template.dte > 0:
				dtes.append(template.dte)
		connector.set_dtes(dtes)

		# Retry logic for ticker data request (important after reconnection)
		max_retries = 3
		retry_delay = 2.0  # seconds
		
		for attempt in range(max_retries):
			try:
				await connector.requestTickerData(symbols)
				logger.debug(f"Ticker data request successful for broker {connector.id}")
				return
			except Exception as e:
				if attempt < max_retries - 1:
					logger.warning(f"Ticker data request failed for broker {connector.id} (attempt {attempt + 1}/{max_retries}): {e}")
					logger.debug(f"Retrying in {retry_delay} seconds...")
					await asyncio.sleep(retry_delay)
				else:
					logger.error(f"Ticker data request failed for broker {connector.id} after {max_retries} attempts: {e}")
					raise

	async def _on_bid_ask_spread_warning_event(self, symbol: str, strike: float, right: OptionRight, bid_price: float, ask_price: float, spread: float, max_allowed_spread: float) -> None:
		""" 
		Called when a bid-ask spread warning event has been received.
		Rate-limited to send at most one notification every 5 seconds to prevent flooding the hub.
		"""  
		if not self.is_market_open():
			return
		
		# Rate limit: Only send a notification every 5 seconds
		current_time = datetime.now()
		if self._last_bid_ask_spread_warning_time is not None:
			time_since_last_warning = (current_time - self._last_bid_ask_spread_warning_time).total_seconds()
			if time_since_last_warning < 5:
				return
		
		self._last_bid_ask_spread_warning_time = current_time
		
		from optrabot.tradinghubclient import NotificationType, TradinghubClient
		option_right_string = 'Call' if right == OptionRight.CALL else 'Put'
		notification_message = f'⚠️ High Bid-Ask Spread detected for {symbol} {option_right_string} Option Strike {strike}: Bid=${bid_price:.2f}, Ask=${ask_price:.2f}, Spread=${spread:.2f} (Max Allowed: ${max_allowed_spread:.2f})'
		await TradinghubClient().send_notification(NotificationType.WARN, notification_message)
		logger.warning(notification_message)

	def _onBrokerDisconnected(self, brokerConnector):
		""" 
		Called when a broker connection has been disconnected
		the BrokerConnector object is passed as parameter
		"""
		logger.warning('Broker {} disconnected, attempting to reconnect in 30 seconds ...', brokerConnector.id)
		
		asyncio.create_task(self._reconnect_broker_task(brokerConnector))

	def _onCommissionReport(self,  order: Order, execution_id: str, commission: float, fee: float):
		""" 
		Called when a commission report has been received
		"""
		self.commissionReportEvent.emit(order, execution_id, commission, fee)

	def _onOrderExecutionDetailsEvent(self, order: Order, execution: Execution):
		""" 
		Called when an order execution details event has been received
		"""
		self.orderExecutionDetailsEvent.emit(order, execution)

	def _onOrderStatus(self, order: Order, status: OrderStatus, filledAmount: int = 0):
		""" 
		Called when an order status has changed
		"""
		self.orderStatusEvent.emit(order, status, filledAmount)

	def _onBrokerConnectFailed(self, brokerConnector):
		""" 
		Called when a broker connection has failed to connect
		"""
		logger.error('Failed to connect to broker {}, attempting to reconnect in 30 seconds ...', brokerConnector.id)
		asyncio.create_task(self._reconnect_broker_task(brokerConnector))

	async def _reconnect_broker_task(self, brokerConnector: BrokerConnector):
		"""
		Asynchronous task to reconnect a broker after a disconnect
		"""
		await asyncio.sleep(30)
		await brokerConnector.connect()

	def _updateAccountsInDatabase(self, accounts: List[Account]):
		"""
		Updates the account information in the database if required
		"""
		with Session(get_db_engine()) as session:
			for account in accounts:
				logger.debug('Managed Account at {}: {}', account.broker, account.id)
				known_account = crud.get_account(session, account.id)
				if known_account == None:
					logger.debug('Account is new. Adding it to the Database')
					new_account = schemas.AccountCreate( id = account.id, name = account.name, broker = account.broker, pdt = account.pdt)
					crud.create_account(session, new_account)
					logger.debug('Account {} created in database.', account.id)
				else:
					if account.name != known_account.name or account.pdt != known_account.pdt:
						logger.debug('Account {} has changed. Updating it in the database.', account.id)
						known_account.name = account.name
						known_account.pdt = account.pdt
						crud.update_account(session, known_account)

	async def shutdownBrokerConnectors(self):
		""" Shuts down all broker connections
		"""
		self._shutingdown = True
		for value in self._connectors.values():
			connector : BrokerConnector = value
			connector.disconnectedEvent -= self._onBrokerDisconnected
			connector.connectFailedEvent -= self._onBrokerConnectFailed
			connector.connectedEvent -= self._onBrokerConnected
			connector.orderStatusEvent -= self._onOrderStatus
			if connector.isConnected():
				await connector.disconnect()
		
