import asyncio
import datetime as dt
import re
from typing import Dict, List

from ib_async import (IB, ComboLeg, CommissionReport, Contract, Fill, Index,
                      LimitOrder, MarketOrder, Option, Order, OrderStatus,
                      PriceIncrement, StopOrder, Ticker, Trade, TradeLogEntry,
                      util)
from loguru import logger

import optrabot.config as optrabotcfg
import optrabot.symbolinfo as symbolinfo
from optrabot.broker.brokerconnector import BrokerConnector, SymbolData
from optrabot.broker.optionpricedata import (OptionStrikeData,
                                             OptionStrikePriceData)
from optrabot.broker.order import Execution, Leg, OptionRight
from optrabot.broker.order import Order as GenericOrder
from optrabot.broker.order import OrderAction
from optrabot.broker.order import OrderStatus as GenericOrderStatus
from optrabot.broker.order import OrderType
from optrabot.exceptions.orderexceptions import (PlaceOrderException,
                                                 PrepareOrderException)
from optrabot.managedtrade import ManagedTrade
from optrabot.models import Account
from optrabot.optionhelper import OptionHelper
from optrabot.tradetemplate.templatefactory import Template


class IBSymbolData(SymbolData):
	def __init__(self) -> None:
		super().__init__()
		self.contract: Contract = None
		self.option_trading_class: str = None
		self.ticker: Ticker = None
		self.options_qualified = False

class ForeignOrder(GenericOrder):
	"""
	Represents an order that has been placed by another user in the TWS.
	It is just used for managing conflicting orders.
	"""
	def __init__(self) -> None:
		super().__init__()

class IBTWSTConnector(BrokerConnector):
	def __init__(self) -> None:
		super().__init__()
		self._host = ''
		self._port = None
		self._clientid = None
		self._initialize()
		self.id = 'IBTWS'
		self.broker = 'IBKR'
		self._lock = asyncio.Lock()
		self._ib = IB()
		self._ib.errorEvent += self.onErrorEvent
		self._ib.disconnectedEvent += self.onDisconnected
		self._ib.execDetailsEvent += self.onExecDetailsEvent
		self._ib.orderStatusEvent += self.onOrderStatusEvent
		self._ib.commissionReportEvent += self.onCommissionReportEvent
		self._ib.pendingTickersEvent += self.onPendingTickers
		self._compiled_option_pattern = re.compile(pattern = r'^(?P<optionsymbol>[A-Z]+)\ +(?P<expiration>[0-9]+)(?P<type>[CP])(?P<strike>[0-9]+)')
		self._symbolReverseLookup: Dict[str, str] = {}		# maps IB symbol to generic symbol
		self._orders: List[GenericOrder] = []
		self._duplicate_order_ids: List[int] = []			# Liste mit Order-IDs, die als dopplete Order IDs von TWS gemeldet wurden
		self._conflictingOrderMap: Dict[GenericOrder,GenericOrder] = {}   # Maps the conflicting order to the causing order
		self._rule_details:  Dict[str, List[PriceIncrement]] = {}   # Map of Rule ID to Price Increment rules
		self._lock_rule = asyncio.Lock()
		self._strikes_wo_option: List[str] = []		# List of strikes without option data
		self._ticker_data_ok: bool = False			# Indicates if Ticker data is received.

	def ___del__(self) -> None:
		"""
		Disconnect from TWS when object is deleted
		"""
		if self._ib.isConnected():
			self._ib.disconnect()

		# Unregister event handlers
		self._ib.errorEvent -= self.onErrorEvent
		self._ib.disconnectedEvent -= self.onDisconnected
		self._ib.execDetailsEvent -= self.onExecDetailsEvent
		self._ib.orderStatusEvent -= self.onOrderStatusEvent
		self._ib.commissionReportEvent -= self.onCommissionReportEvent
		self._ib.pendingTickersEvent -= self.onPendingTickers

	def _initialize(self) -> None:
		"""
		Initialize the TWS connector from the configuration
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		if config is None:
			return
		try:
			config.get('tws')
		except KeyError:
			logger.debug('No TWS connection configured')
			return

		self._host = config.get('tws.host')
		if self._host == '':
			self._host = 'localhost'
		
		try:
			self._port = int(config.get('tws.port'))
		except KeyError:
			self._port = 7496
		try:
			self._clientid = int(config.get('tws.clientid'))
		except KeyError:
			self._clientid = 21
		self._initialized = True

	async def cancel_order(self, order: GenericOrder) -> None:
		""" 
		Cancels the given order
		"""
		await super().cancel_order(order)
		ib_trade: Trade = order.brokerSpecific['trade']
		if ib_trade.orderStatus.status != OrderStatus.Cancelled:
			self._ib.cancelOrder(ib_trade.order)

	async def connect(self) -> None:
		await super().connect()
		
		asyncio.create_task(self._connect_tws_task())

	async def disconnect(self) -> None:
		await super().disconnect()
		try:
			self._ib.disconnect()
		except Exception as excp:
			logger.debug('Error during disconnect from IB TWS: {}', excp)

	async def eod_settlement_tasks(self) -> None:
		"""
		Perform End of Day settlement tasks.
		- Clear list of unavailable options
		"""
		self._strikes_wo_option.clear()

	def getAccounts(self) -> List[Account]:
		"""
		Returns the accounts managed by the TWS connection
		"""
		if len(self._managedAccounts) == 0 and self.isConnected():
			for managedAccount in self._ib.managedAccounts():
				account = Account(id = managedAccount, name = managedAccount, broker = self.broker, pdt = False)
				self._managedAccounts.append(account)
		return self._managedAccounts

	def isConnected(self) -> bool:
		return self._ib.isConnected()
	
	async def prepareOrder(self, order: GenericOrder, need_valid_price_data: bool = True) -> None:
		"""
		Prepares the given order for execution.
		- Retrieve current market data for order legs

		Args:
			order: The order to prepare
			need_valid_price_data: If True, validates price data availability and freshness.
								   If False, creates contracts without price validation (e.g., for trade recovery)

		Raises:
			PrepareOrderException: If the order preparation fails with a specific reason.
		"""  # noqa: E101
		logger.debug('Wait for lock Prepare Order')
		async with self._lock:
			logger.debug('Got Prepare Order lock')
			symbolInformation = symbolinfo.symbol_infos[order.symbol]
			symbolData = self._symbolData[order.symbol]
			comboLegs: list[ComboLeg] = []
			comboContracts: list[Contract] = []
			for leg in order.legs:
				leg_contract = None
				
				if need_valid_price_data:
					# Normal order flow: use price data with validation
					try:
						option_price_data = symbolData.optionPriceData[leg.expiration]
					except KeyError:
						raise PrepareOrderException(f'No price data for expiration {leg.expiration} available', order)

					try:
						option_strike_price_data = option_price_data.strikeData[leg.strike]
					except KeyError as keyErr:
						raise PrepareOrderException(f'No price data for strike {leg.strike} available', order)
					
					leg_contract = option_strike_price_data.brokerSpecific['call_contract'] if leg.right == OptionRight.CALL else option_strike_price_data.brokerSpecific['put_contract']
					
					if not OptionHelper.checkContractIsQualified(leg_contract):
						raise PrepareOrderException(f'Contract {leg_contract} is not qualified', order)
					
					# Preisdaten für das Order Leg übernehmen
					if not option_strike_price_data.is_outdated():
						leg.askPrice = option_strike_price_data.putAsk if leg.right == OptionRight.PUT else option_strike_price_data.callAsk
						leg.bidPrice = option_strike_price_data.putBid if leg.right == OptionRight.PUT else option_strike_price_data.callBid
					else:
						raise PrepareOrderException(f'Price data for strike {leg.strike} is outdated', order)
				else:
					# Trade recovery flow: create contract without price data validation
					# This is used when recovering trades after restart before market data is available
					expiration_str = leg.expiration.strftime('%Y%m%d')
					leg_contract = Option(
						symbolData.contract.symbol,
						expiration_str,
						leg.strike,
						self._mappedRight(leg.right),
						symbolInformation.exchange,
						tradingClass=symbolData.option_trading_class
					)
					
					# Qualify the contract to get the conId needed for ComboLeg
					try:
						qualified_contracts = await asyncio.wait_for(
							self._ib.qualifyContractsAsync(leg_contract),
							timeout=10
						)
						if qualified_contracts and len(qualified_contracts) > 0:
							leg_contract = qualified_contracts[0]
						else:
							raise PrepareOrderException(f'Failed to qualify contract for strike {leg.strike}', order)
					except asyncio.TimeoutError:
						raise PrepareOrderException(f'Timeout qualifying contract for strike {leg.strike}', order)
					
				comboContracts.append(leg_contract)
				leg.brokerSpecific['contract'] = leg_contract
				comboLeg = ComboLeg(conId=leg_contract.conId, ratio=1, action=self._mapped_leg_action(order.action,leg.action), exchange=symbolInformation.exchange)
				comboLegs.append(comboLeg)
			order.brokerSpecific['comboLegs'] = comboLegs
			
			# Only determine price effect when we have valid price data
			# During recovery, price_effect is already set from transactions
			if need_valid_price_data:
				order.determine_price_effect()

	async def placeOrder(self, managed_trade: ManagedTrade, order: GenericOrder, parent_order: GenericOrder = None) -> None:
		""" 
		Places the given order for a managed account via the broker connection.
		
		Raises:
			PlaceOrderException: If the order placement fails with a specific reason.
		"""
		logger.debug('Wait for Place order lock')
		async with self._lock:
			logger.debug('Got Place order lock')
			symbolInformation = symbolinfo.symbol_infos[order.symbol]
			symbolData = self._symbolData[order.symbol]		
	
			comboLegs = order.brokerSpecific['comboLegs']
			if not comboLegs:
				logger.error("Internal Error: Broker specific attribute comboContracts not filled!")
				return
			
			logger.debug('Checking for open Trades if Combo Legs are colliding')
			#contractsWithOpenOrders = await self._getAllOpenOrderContracts(template.account, symbolData.contract.symbol)

			conflictingOrders = await self._findConflictingOrders(order, managed_trade.template.account)
			if len(conflictingOrders) > 0:
				cancelledOCAs = []
				logger.debug(f'Found {len(conflictingOrders)} conflicting orders for symbol {order.symbol}...adding them to the conflicting order map')
				for conflictingIBTrade in conflictingOrders:
					conflictingOrder = self._findOrderByIBTrade(conflictingIBTrade)
					if conflictingOrder == None:
						raise PlaceOrderException(f'Foreign order from another user at the strike prices', order=order)

					self._conflictingOrderMap[conflictingOrder] = order # Conflicting Order mit der verursachenden Order verknüpfen und merken
					
					# Cancel the conflicting order
					if conflictingIBTrade.order.ocaGroup and conflictingIBTrade.order.ocaGroup in cancelledOCAs:
						# Order braucht nicht storniert werden, da bereits eine andere aus der gleichen OCA Gruppe storniert wurde
						pass
					else:
						self._ib.cancelOrder(conflictingIBTrade.order)
						if conflictingIBTrade.order.ocaGroup:
							cancelledOCAs.append(conflictingIBTrade.order.ocaGroup)

				# Urspüngliche Broker Order - Broker Specific [trade] ; Aktuelle Broker Order ; [Conflicting Trades]

				# Ich stormiere die Conflicting Trades
				# - Beim OrderStatusEvent darf die Stonierung für diese Orders nicht weitergreicht werden, weil sie in der Conflicting Trade Map
				#   enthalten sind

				# Es wird die aktuelle Order platziert
				# - Beim OrderStatusEvent "Filled" muss zusätzlich geprüft werden ob es in der Conflicting Trade Map einen Eintrag gibt
				#   wenn ja, dann müssen die referenzierten Conflicting Trades wieder in den Markt gelegt werden

			# Die Orders der behindernden Trades müssen hier storniert werden und deren Daten zwischengespeichert werden
			# Auch der Bezug zu dieser Order, denn wenn diese ausgeführt worden ist müssen die stornierten Orders wieder neu in den Markt gelegt werden.
			#for trade in conflictingTrades:
			#	trade.order.transmit = False
			#	trade.orderStatus.status = OrderStatus.Inactive
			#	self._ib.placeOrder(trade.contract, trade.order)

			#if len(conflictingTrades) > 0:
			#	logger.error(f'Order with opposite action already open for contract. Order not placed!')
			#	return False

			comboContract = None
			if len(order.legs) > 1:
				comboContract = Contract(symbol=symbolData.contract.symbol, secType='BAG', exchange=symbolInformation.exchange, currency=symbolData.contract.currency, comboLegs=comboLegs)
			else:
				comboContract = order.legs[0].brokerSpecific['contract']

			ib_order_price = self._determine_ib_order_price(order)

			if order.type == OrderType.LIMIT:
				#order.price -= 0.50
				ibOrder = LimitOrder(self._mappedOrderAction(order.action), order.quantity, ib_order_price)
				ibOrder.account = managed_trade.template.account
				ibOrder.outsideRth = True
			elif order.type == OrderType.STOP:
				ibOrder = StopOrder(self._mappedOrderAction(order.action), order.quantity, ib_order_price)
				ibOrder.account = managed_trade.template.account
				ibOrder.outsideRth = True
			elif order.type == OrderType.MARKET:
				ibOrder = MarketOrder(self._mappedOrderAction(order.action), order.quantity)
				ibOrder.account = managed_trade.template.account
				ibOrder.outsideRth = True
				ibOrder.auxPrice = 0
				ibOrder.lmtPrice = 0
			else:
				logger.error(f'Order type {order.type} currently not supported by IBKR Connector!')
			ibOrder.orderRef = order.orderReference
			if order.ocaGroup:  # https://interactivebrokers.github.io/tws-api/oca.html
				ibOrder.ocaGroup = order.ocaGroup
				ibOrder.ocaType = 1
			
			ibOrder.tif = 'DAY'  # Set Time in Force to DAY to avoid GTC orders
			trade = self._ib.placeOrder(comboContract, ibOrder)
			order.brokerSpecific['comboContract'] = comboContract
			order.brokerSpecific['order'] = ibOrder
			order.brokerSpecific['trade'] = trade
			self._orders.append(order)
			logger.debug(f'Account: {managed_trade.template.account} Order {ibOrder.orderId} placed for Trade: {trade} Number of contracts: {order.quantity}')

	async def place_complex_order(self, take_profit_order: GenericOrder, stop_loss_order: GenericOrder, template: Template) -> bool:
		"""
		TWS doesn't support complex orders
		"""
		raise NotImplementedError()
	
	async def adjustOrder(self, managed_trade: ManagedTrade, order: GenericOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		if order.status == GenericOrderStatus.FILLED:
			logger.info('Order {} is already filled. Adjustment not required.', order)
			return True
		if order.status == GenericOrderStatus.CANCELLED:
			logger.info('Order {} is already cancelled. Adjustment not possible.', order)
			return True

		order.price = price
		ib_order_price = self._determine_ib_order_price(order)

		trade: Trade = order.brokerSpecific['trade']
		try:
			comboContract = order.brokerSpecific['comboContract']
			ibOrder: Order = order.brokerSpecific['order']
			if order.type == OrderType.LIMIT:
				ibOrder.lmtPrice = ib_order_price
			elif order.type == OrderType.STOP:
				ibOrder.auxPrice = ib_order_price
			trade = self._ib.placeOrder(comboContract, ibOrder)
			order.brokerSpecific['trade'] = trade
			return True
		except Exception as excp:
			logger.error('Exception beim Anpassen der Order')
		return False

	async def requestTickerData(self, symbols: List[str]) -> None:
		""" 
		Request ticker data for the given symbols and their options
		"""
		retries = 0
		qualifiedContracts = False
		contracts = []
		for symbol in symbols:
			requestOptionsData = False
			match symbol:
				case 'SPX':
					symbolData = IBSymbolData()
					symbolData.symbol = symbol
					symbolInformation = symbolinfo.symbol_infos[symbolData.symbol]
					symbolData.contract = Index('SPX', 'CBOE')
					symbolData.option_trading_class = symbolInformation.trading_class
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.contract.symbol] = symbol
					contracts.append(symbolData.contract)
				case 'VIX':
					symbolData = IBSymbolData()
					symbolData.symbol = symbol
					symbolData.contract = Index('VIX', 'CBOE')
					symbolData.trade_options = False  # No options for VIX
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.contract.symbol] = symbol
					contracts.append(symbolData.contract)
				case _:
					logger.error(f'Symbol {symbol} currently not supported by IBKR Connector!')
					continue

		while retries < 3:
			try:
				qualifiedContracts = await asyncio.wait_for(self._ib.qualifyContractsAsync(*contracts), timeout=10)
				for contract in qualifiedContracts:
					if self._symbolData[contract.symbol].trade_options:
						symbolInformation = symbolinfo.symbol_infos[contract.symbol]
						chains = await self._ib.reqSecDefOptParamsAsync(contract.symbol, '', contract.secType, contract.conId)
						if len(chains) > 0:
							chain = next(c for c in chains if c.tradingClass == symbolInformation.trading_class and c.exchange == contract.exchange)
							if chain == None:
								logger.error(f'No Option Chain for trading class {symbolInformation.trading_class} found. Unable to request option data')

							current_date = dt.date.today()
							expiration = current_date.strftime('%Y%m%d')
							symbolData = self._symbolData[contract.symbol]

							# Keep Option Chain expirations for later DTE calculations
							for expiration in chain.expirations:
								exp_date = dt.datetime.strptime(expiration, '%Y%m%d').date()
								if not exp_date in symbolData.expirations:
									symbolData.expirations.append(exp_date)

							symbolData.strikes = chain.strikes
							#if int(chain.expirations[0]) > int(expiration):
							if current_date > symbolData.expirations[0]:
								logger.warning(f'There are no {contract.symbol} options expiring today!')
					
					self._ib.reqMktData(contract, '', False, False)
				contracts_qualified = True
				break
			except asyncio.TimeoutError:
				retries += 1
				logger.warning(f'Timeout while qualifying contracts. Retrying ({retries}) in 5 seconds ...')
				await asyncio.sleep(5)
			except Exception as excp:
				logger.error(f'Error qualifying contract {symbolData.contract}: {excp}')
			
		if qualifiedContracts == False:
			logger.error(f'Error qualifying contracts when requesting ticker data!!')
		else:
			self._subscribed_ticker_data = True # Remember that we have subscribed to ticker data

	async def _connect_tws_task(self) -> None:
		try:
			await self._ib.connectAsync(self._host, self._port, clientId=self._clientid)
			
			self._emitConnectedEvent()
			
		except Exception as excp:
			self._emitConnectFailedEvent()
			#logger.error("Error connecting TWS: {}", excp)
			#attempt += 1
			#logger.error('Connect failed. Retrying {}. attempt in {} seconds', attempt, delaySecs)
			#await asyncio.sleep(delaySecs)
			#asyncio.create_task(self._connect_ib_task(attempt, delaySecs))

	async def onDisconnected(self):
		#logger.warning('Disconnected from TWS, attempting to reconnect in 30 seconds ...')
		await self._set_ticker_data_status(False, 'Broker disconnected')
		self._emitDisconnectedEvent()

	async def onErrorEvent(self, reqId: int, errorCode: int, errorString: str, contract: Contract):
		if errorCode in {101, 104, 200, 202, 399, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2157, 2158, 10349}:
			# 101: Maximale Anzahl an Tickern wurde erreicht
			# 104: Cannot modify a filled order
			# 200: No security definition has been found for the request, contract
			# 202: Order wurde storniert z.B. TP order bei OCO, wenn SL Order ausgeführt wurde
			# 399: Warnung das die Order nur während der regulären Handelszeiten ausgeführt wird
			# 10349: Die Gültigkeitsdauer der Order wurde gemäß Order-Voreinstellungen auf DAY gesetzt
			# 2103, 2104, 2105, 2106, 2108, 2158: Marktdatenverbindung ignorieren
			# 2107: Die Verbindung zum HMDS-Datenzentrum is inaktv, sollte jedoch auf Anfrage verfügbar seind
			# 2109: Warnhinweis zu einem Orderereignis außerhalb der regulären Handelszeiten
			# 2157: Verbindung zum Sec-def-Datenzentrum unterbrochen
			return
		elif errorCode == 201:
			# 201: Order rejected - reason:Stop price revision is disallowed after order has triggered
			# 201: Order rejected - reason:We are unable to accept your order. Your Available Funds are in sufficient
			# 201: Order abgewiesen - Grund:Order has been cancelled already, too late to replace
			if errorString.find('Margin') > -1:
				logger.error('Order rejected: Insufficient margin!')
				# Send Notification
				from optrabot.tradinghubclient import NotificationType, TradinghubClient
				notification_message = f'‼️ Broker {self.broker}: Order rejected because of insufficient margin!'
				await TradinghubClient().send_notification(NotificationType.INFO, notification_message)
				return

		elif errorCode == 10147:
			# Die zu stornierende Order wurde nicht gefunden
			if reqId in self._duplicate_order_ids:
				logger.info(f'Order {reqId}' + ' is a duplicate order ID. Ignoring error event.')
				return

		elif errorCode == 10148:
			# Order that should be cancelled cannot be cancelled
			# Passiert beim Cancel einer TP oder SL Order, wenn sie per OCO Group verbunden sind und eine der Orders bereits
			# storniert wurde

			# Prüfen ob die betreffende Order in den conflicting Orders enthalten ist
			for entry in self._conflictingOrderMap.keys():
				order: GenericOrder = entry
				if order.brokerSpecific['trade'].order.orderId == reqId:
					logger.debug(f'Order {reqId} is conflicting with another order. Ignoring error event.')
					return
		
		elif errorCode == 10168:
			# Für die angeforderten Markdaten besteht kein Abonnement
			logger.error(f'No valid market data subscription for symbol {contract.symbol}')
			await self._set_ticker_data_status(False, 'No valid market data subscription')
			return

		elif errorCode == 1100:
			# Connection between TWS and IB lost.
			logger.warning('Connection between TWS and Interactive Brokers lost -> Trading disabled!')
			await self._set_ticker_data_status(False, 'Connection lost')
			return
		elif errorCode == 1102:
			# Connection between TWS and IB restored
			logger.success('Connection between TWS and Interactive Brokers has been reestablished! -> Trading enabled!')
			await self._set_ticker_data_status(True, 'Connection restored')
			return
		elif errorCode == 321:
			# Invalid contract id - happens after overnight disconnection
			# This will be handled by the reconnection flow which triggers requestTickerData()
			logger.warning('Invalid contract id detected - will be refreshed on next reconnection')
			return
		elif errorCode == 2148:
			# Margin Warning
			logger.warning('IB reports potential margin violation!')
			return

		errorData = {'action': 'errorEvent','reqId':reqId, 'errorCode':errorCode, 'errorString':errorString, 'contract': contract}
		logger.error('IB raised following error: {}', errorData)
	
	async def onExecDetailsEvent(self, trade: Trade, fill: Fill):
		""" This eventhandler is called on trade execution.
		The event is raised for each single fill of an order leg
		"""
		logger.debug('Exec Detail for trade {}', trade)
		logger.debug('Fill: {}', fill)
		relevantOrder = None
		for order in self._orders:
			brokerSpecificTrade: Trade = order.brokerSpecific['trade']
			if brokerSpecificTrade.order.orderId == trade.order.orderId:
				relevantOrder = order
				break
		if relevantOrder == None:
			logger.debug(f'No managed order matched the execution details event')
			return
		if fill.contract.secType == 'BAG':
			# Do not store inform stion on combo executions
			return
		if fill.execution.side == 'BOT':
			action = OrderAction.BUY
		else:
			action = OrderAction.SELL
		expirationDate = dt.datetime.strptime(fill.contract.lastTradeDateOrContractMonth, '%Y%m%d')
		execution = Execution(id=fill.execution.execId, 
							action=action,
							sec_type=fill.contract.right,
							strike=fill.contract.strike,
							amount=fill.execution.shares,
							price=fill.execution.avgPrice,
							expiration=expirationDate,
							timestamp=fill.execution.time)
		self._emitOrderExecutionDetailsEvent(relevantOrder, execution)

	async def onCommissionReportEvent(self, trade: Trade, fill: Fill, report: CommissionReport):
		"""
		Handles the Commission Report Event
		"""
		relevantOrder = None
		logger.debug('Commission Report order id {} and fill {}', trade.order.orderId, fill)
		logger.debug('Commission Report: {}', report)
		for order in self._orders:
			brokerSpecificTrade: Trade = order.brokerSpecific['trade']
			if brokerSpecificTrade.order.orderId == trade.order.orderId:
				relevantOrder = order
				break
		if relevantOrder == None:
			logger.debug(f'No managed order matched the commission report event')
			return

		self._emitCommissionReportEvent(relevantOrder, fill.execution.execId, report.commission, 0)

	async def onOrderStatusEvent(self, trade: Trade):
		"""
		Handles the Order Status Event
		"""
		logger.debug(f'onOrderStatusEvent() Order: {trade.order.orderId} Status: {trade.orderStatus.status}')
		relevantOrder: GenericOrder = None
		for order in self._orders:
			brokerSpecificTrade: Trade = order.brokerSpecific['trade']
			if brokerSpecificTrade.order.orderId == trade.order.orderId:
				relevantOrder = order
				break
		if relevantOrder == None:
			logger.debug(f'No managed order matched the status event')
			return
		
		# Prüfen ob die order in der Conflicting Order Map enthalten ist
		if relevantOrder in self._conflictingOrderMap.keys():
			causingOrder = self._conflictingOrderMap[relevantOrder]
			causingOrderOrderId = causingOrder.brokerSpecific['trade'].order.orderId
			logger.debug(f'Order {trade.order.orderId} is conflicting with order {causingOrderOrderId}. Ignoring status event.')
			return

		if trade.orderStatus.status == OrderStatus.Cancelled or trade.orderStatus.status == OrderStatus.Inactive or trade.orderStatus.status == OrderStatus.ApiCancelled:
			log_entry: TradeLogEntry = None
			for log_entry in trade.log:
				if log_entry.status != 'Cancelled':
					continue
				logger.debug(f'Order Log: {log_entry}')
			if log_entry == None:
				logger.error(f'No log entry found for cancelled order!')
			elif log_entry.errorCode == 103:
				# Error 103, reqId 10292: Doppelt vorhandene Order-ID
				logger.warning('Adjustment of entry order has been rejected, because Duplicate Order-ID.')
				duplicate_order_id = trade.order.orderId
				self._duplicate_order_ids.append(duplicate_order_id)
				logger.debug(f'Added Order ID {duplicate_order_id} to duplicate order IDs')
				# In diesem Fall muss die Order sicherheitshalber neu platziert werden
				try:
					self._ib.cancelOrder(trade.order)
				except Exception as excp:
					logger.debug(f'Error cancelling order: {excp}')
				new_order_id = self._ib.client.getReqId()
				trade.order.orderId = new_order_id
				# Add the replacement order ID to duplicate list to prevent it from being treated as cancelled
				self._duplicate_order_ids.append(new_order_id)
				logger.debug(f'Replacing order with new Order Id {trade.order.orderId}')
				relevantOrder.brokerSpecific['trade'] = self._ib.placeOrder(trade.contract, trade.order)
				logger.info(f'Order {duplicate_order_id} has been replaced with new Order Id {trade.order.orderId}')
				return
			elif log_entry.errorCode == 104:
				# Error 104: Cannot modify a filled order
				logger.warning(f'Order {trade.order.orderId} has been filled already. Ignoring the Cancelled status event.')
				return
			elif log_entry.errorCode == 10349:
				# Error 10349: Gültigkeitsdauer der Order wurde gemäß Order-Voreinstellungen auf DAY gesetzt
				logger.warning(f'Order {trade.order.orderId} validity changed per default settings. Ignoring the Cancelled status event.')
				return
			
			# Ingnore the Cancelled status event for duplicate order IDs
			if trade.order.orderId in self._duplicate_order_ids:
				logger.debug(f'Order {trade.order.orderId} is a duplicate order ID. Ignoring the Cancelled status event.')
				return
			else:
				logger.debug(f'Order with ID {trade.order.orderId} is not in the list of duplicate order IDs')

			# Wenn die stornierte Order eine verursachende Order für Conflicting Ordrer(s) ist, dann müssen die stornierten Orders wieder in den Markt gelegt werden
			await self._placeConflictingOrdersAgain(relevantOrder)
		
		filledAmount = 0
		if trade.orderStatus.status == OrderStatus.Filled:
			# Wenn die gefüllte Order eine verursachende Order für conflicting Order(s) ist und sie vollständig ausgeüfhrt wurde,
			# dann müssen die stornierten Orders wieder in den Markt gelegt werden
			await self._placeConflictingOrdersAgain(relevantOrder)

			filledAmount = relevantOrder.quantity - trade.remaining()
			relevantOrder.averageFillPrice = trade.orderStatus.avgFillPrice
			
			# Remove filled order from duplicate order IDs list (if it's a replacement order)
			if trade.order.orderId in self._duplicate_order_ids:
				self._duplicate_order_ids.remove(trade.order.orderId)
				logger.debug(f'Removed filled order {trade.order.orderId} from duplicate order IDs list')

		self._emitOrderStatusEvent(relevantOrder, self._genericOrderStatus(trade.orderStatus.status), filledAmount)

	def getFillPrice(self, order: GenericOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		trade: Trade = order.brokerSpecific['trade']
		return abs(trade.orderStatus.avgFillPrice)
	
	def getLastPrice(self, symbol: str) -> float:
		""" 
		Returns the last price of the given symbol
		"""
		symbolData = self._symbolData[symbol]
		return symbolData.lastPrice

	def get_option_strike_data(self, symbol: str, expiration: dt.date) -> OptionStrikeData:
		""" 
		Returns the option strike data for the given symbol and expiration. It is including
		prices and greeks.
		"""
		symbolData = self._symbolData[symbol]
		try:
			return symbolData.optionPriceData[expiration]
		except KeyError:
			raise ValueError(f'No option strike data for symbol {symbol} and expiration {expiration} found!')

	def get_option_strike_price_data(self, symbol: str, expiration: dt.date, strike: float) -> OptionStrikePriceData:
		""" 
		Returns the option strike price data for the given symbol, expiration date, strike price and right
		"""
		symbolData = self._symbolData[symbol]
		try:
			optionStrikeData = symbolData.optionPriceData[expiration]
			if strike in optionStrikeData.strikeData.keys():
				return optionStrikeData.strikeData[strike]
			else:
				return None
		except KeyError as keyErr:
			return None

	def get_strike_by_delta(self, symbol: str, right: str, delta: int) -> float:
		""" 
		Returns the strike price based on the given delta based on the buffered option price data
		"""
		symbolData = self._symbolData[symbol]
		current_date = dt.date.today()
		option_price_data: OptionStrikeData= symbolData.optionPriceData[current_date]
		previous_delta = 0
		previous_strike = 0
		reverse = True if right == OptionRight.PUT else False
		sorted_strikes = dict(sorted(option_price_data.strikeData.items(), reverse=reverse))
		for strike, price_data in sorted_strikes.items():
			if right == OptionRight.PUT:
				if price_data.putDelta == None:
					continue
				adjusted_delta = price_data.putDelta * -100
			else:
				if price_data.callDelta == None:
					continue
				adjusted_delta = price_data.callDelta * 100
			if adjusted_delta <= delta:
				if OptionHelper.closest_number(delta, previous_delta, adjusted_delta) == adjusted_delta:
					return strike
				else:
					return previous_strike
			previous_delta = adjusted_delta
			previous_strike = strike

		raise ValueError(f'No strike price found for delta {delta} in symbol {symbol}!')
	
	def get_strike_by_price(self, symbol: str, right: str, price: float) -> float:
		""" 
		Returns the strike price based on the given premium price based on the buffered option price data
		"""
		symbolData = self._symbolData[symbol]
		current_date = dt.date.today()
		option_price_data: OptionStrikeData= symbolData.optionPriceData[current_date]
		previous_price = 0
		previous_strike = 0
		reverse = True if right == OptionRight.PUT else False
		sorted_strikes = dict(sorted(option_price_data.strikeData.items(), reverse=reverse))
		for strike, price_data in sorted_strikes.items():
			if right == OptionRight.PUT:
				current_strike_price = price_data.getPutMidPrice()
				if current_strike_price == None:
					continue
			elif right == OptionRight.CALL:
				current_strike_price = price_data.getCallMidPrice()
				if current_strike_price == None:
					continue
			if current_strike_price > 0 and current_strike_price <= price:
				if OptionHelper.closest_number(price, previous_price, current_strike_price) == current_strike_price:
					return strike
				else:
					return previous_strike
			previous_price = current_strike_price
			previous_strike = strike
		raise ValueError(f'No strike price found for price {price} in symbol {symbol}!')

	async def onPendingTickers(self, tickers: List[Ticker]):
		"""
		Handles the pending tickers event
		"""
		if not self._subscribed_ticker_data:
			return
		
		for ticker in tickers:
			if ticker.contract.symbol in self._symbolData.keys():
				logger.trace(f'Ticker for symbol {ticker.contract.symbol} received.')
				ticker.lastExchange
				logger.trace(f'Ticker Last {ticker.last}: {ticker}')
				symbolData = self._symbolData[ticker.contract.symbol]
				symbolData.ticker = ticker
				if ticker.contract.secType != 'OPT':
					# Capture last price of Underlying
					if ticker.last and util.isNan(ticker.last) == False:
						symbolData.lastPrice = ticker.last
					else:
						symbolData.lastPrice = ticker.close

				# Prüfen ob Preisdaten vorhanden sind
				if util.isNan(symbolData.lastPrice) and ticker.contract.secType != 'OPT':
					# Wenn mehrmals keine gültigen Preisdaten empfangen wurden, dann wird der Handel deaktiviert
					symbolData.noPriceDataCount += 1
					if symbolData.noPriceDataCount > 5:
						logger.error(f'Receiving no valid price data for symbol {symbolData.symbol}. Trading disabled!')
						await self._set_ticker_data_status(False)
						break
					continue
				elif symbolData.options_qualified:
					symbolData.noPriceDataCount = 0
					if not self._ticker_data_ok:
						await self._set_ticker_data_status(True)

				# Für VIX werden keine weiteren Daten gelesen
				if ticker.contract.symbol == 'VIX':
					break

				if ticker.contract.secType != 'OPT':
					# Keine Optionen -> Fehlende Optionen abfragen
					try:
						atmStrike = OptionHelper.roundToStrikePrice(symbolData.lastPrice)
						if symbolData.lastAtmStrike != atmStrike:  # Check for missing Option Data only if ATM Strike has changed
							
							symbolData.lastAtmStrike = atmStrike
							await self._requestMissingOptionData(symbolData, atmStrike)
					except KeyError as keyErr:
						logger.error(f'No generic symbol found for IB TWS symbol {ticker.contract.symbol}')
				else:
					# Option verarbeiten
					try:
						optionType, expiration, strike = self._getOptionInfos(ticker.contract)
					except Exception as exc:
						logger.error(f'Error getting option infos: {exc}')
					genericSymbol = self._symbolReverseLookup[ticker.contract.symbol]
					symbol_information = symbolinfo.symbol_infos[genericSymbol]
					optionStrikePriceData = self.get_option_strike_price_data(genericSymbol, expiration, strike)
					if optionStrikePriceData:
						if optionType == OptionRight.CALL:
							optionStrikePriceData.callAsk = ticker.ask
							optionStrikePriceData.callBid = ticker.bid
							if ticker.modelGreeks:
								optionStrikePriceData.callDelta = ticker.modelGreeks.delta
						else:
							optionStrikePriceData.putAsk = ticker.ask
							optionStrikePriceData.putBid = ticker.bid
							if ticker.modelGreeks:
								optionStrikePriceData.putDelta = ticker.modelGreeks.delta
						optionStrikePriceData.lastUpdated = dt.datetime.now(symbol_information.timezone)
						self._last_option_price_update_time = optionStrikePriceData.lastUpdated
						await self._monitor_bid_ask_spread(optionStrikePriceData, genericSymbol, strike)
					else:
						logger.debug(f'No option data available for strike {strike} in symbol {genericSymbol} yet. Ignoring Ticker data.')
					
	def uses_oco_orders(self) -> bool:
		""" 
		The TWS Connector uses OCO orders for take profit and stop loss orders
		"""
		return True

	async def unsubscribe_ticker_data(self):
		""" 
		Unsubscribes all ticker data subscriptions
		"""
		await super().unsubscribe_ticker_data()
		for symbolData in self._symbolData.values():
			try:
				for day_option_price_data in symbolData.optionPriceData.values():
					for value in day_option_price_data.strikeData.values():
						option_price_data: OptionStrikePriceData = value
						try:
							call_contract = option_price_data.brokerSpecific['call_contract']
							if call_contract:
								self._ib.cancelMktData(call_contract)
								option_price_data.brokerSpecific['call_contract'] = None
						except KeyError as keyErr:
							pass
						try:
							put_contract = option_price_data.brokerSpecific['put_contract']
							if put_contract:
								self._ib.cancelMktData(put_contract)
								option_price_data.brokerSpecific['put_contract'] = None
						except KeyError as keyErr:
							pass
				symbolData.optionPriceData.clear()
				symbolData.lastAtmStrike = 0
				symbolData.lastPrice = 0
			except KeyError as keyErr:
				pass
	
	def _createReplacementOrder(self, ibOrder: Order) -> Order:
		"""
		Creates a new replacement order for the given order
		"""
		if isinstance(ibOrder, LimitOrder):
			replacementOrder = LimitOrder(ibOrder.action, ibOrder.totalQuantity, ibOrder.lmtPrice)
		elif isinstance(ibOrder, StopOrder):
			replacementOrder = StopOrder(ibOrder.action, ibOrder.totalQuantity, ibOrder.auxPrice)
		else:
			logger.error(f'Order type {type(ibOrder)} currently not supported by IBKR Connector!')
			return None
		replacementOrder.account = ibOrder.account
		replacementOrder.outsideRth = ibOrder.outsideRth
		replacementOrder.tif = ibOrder.tif
		replacementOrder.orderRef = ibOrder.orderRef
		replacementOrder.ocaGroup = ibOrder.ocaGroup
		replacementOrder.ocaType = ibOrder.ocaType
		replacementOrder.transmit = True
		return replacementOrder

	def _determine_ib_order_price(self, order: GenericOrder) -> float:
		"""
		Determines the correct IBKR order price based on the given generic order
		"""
		assert order.price_effect is not None

		# If it is a single leg order, and it is a buy to open or sell to close order, the price is positive
		if len(order.legs) == 1 and (order.action == OrderAction.BUY_TO_OPEN or order.action == OrderAction.SELL_TO_CLOSE):
			return abs(order.price)

		# Calculate price based on the order legs
		calculated_price = order.calculate_price()
		# If it is a closing order, the calculated price must be inverted, because the leg actions are inverted as well (_mapped_leg_action)
		if order.action == OrderAction.SELL_TO_CLOSE or order.action == OrderAction.BUY_TO_CLOSE:
			calculated_price = -calculated_price

		# Invert the order price if signs are different from calculated price
		ib_order_price = order.price
		if (calculated_price < 0 and order.price > 0) or (calculated_price > 0 and order.price < 0):
			ib_order_price = -order.price
		return ib_order_price

	def _findOrderByIBTrade(self, trade: Trade) -> GenericOrder:
		"""
		Find the generic order that belongs to the given IBKR trade
		"""
		for order in self._orders:
			if order.brokerSpecific['trade'] == trade:
				return order
		return None

	async def _findConflictingOrders(self, order: GenericOrder, account: str) -> List[Trade]:
		"""
		Find all open trades for the given account and symbol that are conflicting with the given order
		"""
		comboLegs = order.brokerSpecific['comboLegs']
		oppositeAction = 'BUY' if self._mappedOrderAction(order.action) == 'SELL' else 'SELL'
		conflictingTrades: List[Trade] = []
		openTrades: List[Trade] = await self._ib.reqAllOpenOrdersAsync()
		
		for openTrade in openTrades:
			if openTrade.order.transmit == False or openTrade.contract.symbol != order.symbol or openTrade.order.account != account or openTrade.order.action != oppositeAction:
				continue

			# ausgeführte und stonierte Trades/Orders spielen keine Rolle (sollten eigentlich nicht mehr in der Liste sein)
			if openTrade.orderStatus.status == OrderStatus.Cancelled or openTrade.orderStatus.status == OrderStatus.Filled:
				continue

			# Offene Order mit entgegengesetzter Aktion gefunden -> Sind enhalten sie Kontrakte die mit der neuen Order kollidieren
			if openTrade.contract.secType == 'BAG':
				for leg in openTrade.contract.comboLegs:
					for comboLeg in comboLegs:
						if leg.conId == comboLeg.conId:
							if openTrade not in conflictingTrades:
								conflictingTrades.append(openTrade)
			else:
				for comboLeg in comboLegs:
					if openTrade.contract.conId == comboLeg.conId:
						if openTrade not in conflictingTrades:
							conflictingTrades.append(openTrade)
		return conflictingTrades

	def _genericOrderStatus(self, status: OrderStatus) -> GenericOrderStatus:
		"""
		Maps the IBKR specific order status to the general order status
		"""
		match status:
			case OrderStatus.PendingSubmit:
				return GenericOrderStatus.OPEN
			case OrderStatus.PreSubmitted:
				return GenericOrderStatus.OPEN
			case OrderStatus.Submitted:
				return GenericOrderStatus.OPEN
			case OrderStatus.ApiCancelled:
				return GenericOrderStatus.CANCELLED
			case OrderStatus.Cancelled:
				return GenericOrderStatus.CANCELLED
			case OrderStatus.Filled:
				return GenericOrderStatus.FILLED
			case OrderStatus.Inactive:
				return GenericOrderStatus.CANCELLED
			case OrderStatus.PendingCancel:
				return GenericOrderStatus.OPEN
			case OrderStatus.Cancelled:
				return GenericOrderStatus.CANCELLED

	def _getOptionInfos(self, option: Option) -> tuple:
		"""
		Extracts the generic symbol and expiration date, strike price from the IBKR option contract
		"""
		error = False
		match = self._compiled_option_pattern.match(option.localSymbol)
		try:
			if match:
				for symbol, symbol_info in symbolinfo.symbol_infos.items():
					if symbol_info.symbol == option.symbol:
						genericSymbol = symbol_info.symbol
						break
				expiration = dt.datetime.strptime(match.group('expiration'), '%y%m%d').date()
				optionType = OptionRight.CALL if match.group('type') == 'C' else OptionRight.PUT
			else:
				raise IndexError
		except IndexError as indexErr:
			logger.error(f'Invalid option symbol {option.localSymbol}')
			error = True
		except ValueError as valueErr:
			logger.error(f'Invalid option symbol {option.localSymbol}')
			error = True
		if genericSymbol == None or error == True:
			raise ValueError(f'Invalid option symbol {option.localSymbol}')
		return optionType, expiration, option.strike

	def _mappedOrderAction(self, action: OrderAction) -> str:
		"""
		Maps the general order action to the IBKR specific order action
		"""
		match action:
			case OrderAction.BUY:
				return 'BUY'
			case OrderAction.BUY_TO_OPEN:
				return 'BUY'
			case OrderAction.BUY_TO_CLOSE:
				return 'BUY'
			case OrderAction.SELL:
				return 'SELL'
			case OrderAction.SELL_TO_OPEN:
				return 'SELL'
			case OrderAction.SELL_TO_CLOSE:
				return 'SELL'
			case _:
				logger.error(f'Order action {action} not supported by IBKR Connector!')
				return None
			
	def _mapped_leg_action(self, order_action: OrderAction, leg_action: OrderAction) -> str:
		"""
		Maps the leg action of a generic order to the correct IB specific leg action depending on the order action
		"""
		match order_action:
			case OrderAction.BUY_TO_OPEN:
				if leg_action == OrderAction.BUY:
					return 'BUY'
				elif leg_action == OrderAction.SELL:
					return 'SELL'
				else:
					raise ValueError(f'Unknown leg action: {leg_action}')
			case OrderAction.SELL_TO_OPEN:
				if leg_action == OrderAction.BUY:
					return 'BUY'
				elif leg_action == OrderAction.SELL:
					return 'SELL'
				else:
					raise ValueError(f'Unknown leg action: {leg_action}')
			case OrderAction.BUY_TO_CLOSE:
				# Action of the leg needs to be inverted
				if leg_action == OrderAction.BUY:
					return 'SELL'
				elif leg_action == OrderAction.SELL:
					return 'BUY'
				else:
					raise ValueError(f'Unknown leg action: {leg_action}')
			case OrderAction.SELL_TO_CLOSE:
				# Action of the leg needs to be inverted
				if leg_action == OrderAction.BUY:
					return 'SELL'
				elif leg_action == OrderAction.SELL:
					return 'BUY'
				else:
					raise ValueError(f'Unknown leg action: {leg_action}')
			case _:
				logger.error(f'Order action {order_action} not supported by IBKR Connector!')
				return None
	
	def _mappedRight(self, right: OptionRight) -> str:
		"""
		Maps the general option right to the IBKR specific option right
		"""
		match right:
			case OptionRight.CALL:
				return 'C'
			case OptionRight.PUT:
				return 'P'
			case _:
				raise ValueError(f'Option right {right} not supported by IBKR Connector!')
				return None
			
	async def _placeConflictingOrdersAgain(self, order: GenericOrder):
		"""
		Relevante temporär stornierte Conflicting Orders wieder in den Markt legen, wenn
		die übergebene Order eine verursachende Order ist
		"""
		resolvedConflictingOrders: List[GenericOrder] = []
		for key, value in self._conflictingOrderMap.items():
			if value == order:
				logger.debug(f'Causing order of a conflicting order has been filled. Re-placing conflicting order again.')
				if type(key) == ForeignOrder:
					logger.debug(f'Conflicting order is a foreign order. Re-placing it.')
				conflictingOrder: GenericOrder = key
				ibOrder:Order = conflictingOrder.brokerSpecific['order']
				replacementOrder = self._createReplacementOrder(ibOrder)
				replacementTrade = self._ib.placeOrder(conflictingOrder.brokerSpecific['comboContract'], replacementOrder)
				logger.debug(f'Conflicting order {ibOrder.orderId} has been re-placed with order id {replacementTrade.order.orderId}')
				conflictingOrder.brokerSpecific['order'] = replacementOrder
				conflictingOrder.brokerSpecific['trade'] = replacementTrade
				resolvedConflictingOrders.append(conflictingOrder)
		
		# Jetzt wiedereingestellte conflicting orders aus der Map entfernen
		for entry in resolvedConflictingOrders:
			self._conflictingOrderMap.pop(entry)

	async def _getAllOpenOrderContracts(self, account, symbol) -> List:
		"""
		Determine the ContractIds of all open Orders for the given account and symbol
		"""
		openTrades: List[Trade] = await self._ib.reqAllOpenOrdersAsync()
		openOrderContracts = list()
		for openTrade in openTrades:
			if openTrade.contract.symbol != symbol or openTrade.order.account != account:
				continue
			if openTrade.contract.secType == 'BAG':
				for leg in openTrade.contract.comboLegs:
					openOrderContracts.append(leg.conId)
			else:
				openOrderContracts.append(openTrade.contract.conId)
		return openOrderContracts
	
	def _calculateMidPrice(self, legs: List[Leg], tickers: List[Ticker], contracts: List[Contract]) -> float:
		"""
		Calculates the mid price for the given tickers
		"""
		midPrice = None
		for leg in legs:
			for ticker in tickers:
				if ticker.contract.strike == leg.strike and ticker.contract.right == self._mappedRight(leg.right):
					leg
					legMidPrice = (ticker.ask + ticker.bid) / 2
					if util.isNan(legMidPrice) or (ticker.ask == -1.00 and ticker.bid == -1.00):
						if leg.action == OrderAction.BUY:
							legMidPrice = 0.05
						else:
							return None
					if leg.action == OrderAction.SELL:
						midPrice = -legMidPrice
					else:
						midPrice += legMidPrice
					break

		return OptionHelper.roundToTickSize(midPrice)
	
	async def _requestMissingOptionData(self, symbolData: IBSymbolData, atmStrike: float):
		"""
		Request option data for the given symbol and expiration date
		"""
		relevant_expirations = self._determine_relevant_expirations(symbolData)
		symbolInformation = symbolinfo.symbol_infos[symbolData.symbol]
		strikes_of_interest = self._determine_strikes_of_interest(symbolData, atmStrike)	
		options_to_be_requested = []
		for relevant_expiration in relevant_expirations:
			# Bestehende gespeicherte Optionen abfragen
			try:
				expiration_date_str = relevant_expiration.strftime('%Y%m%d')
				optionStrikeData = symbolData.optionPriceData[relevant_expiration]
			except KeyError as keyErr:
				# Wenn noch keine Optionsdaten für das Verfallsdatum vorhanden sind
				# dann bei der TWS anfragen ob es Optionen gibt
				chains = await self._ib.reqSecDefOptParamsAsync(symbolData.contract.symbol, '', symbolData.contract.secType, symbolData.contract.conId)
				try:
					chain = next(c for c in chains if c.tradingClass == symbolData.option_trading_class and c.exchange == symbolData.contract.exchange)
					if int(chain.expirations[0]) > int(expiration_date_str):
						return
				
					optionStrikeData = OptionStrikeData()
					symbolData.optionPriceData[relevant_expiration] = optionStrikeData
			
				except Exception as excp:
					logger.error(f'Unexpected error: {excp}')
					return

			for strike_price in strikes_of_interest:
				strike_identifier = f"{expiration_date_str}#{strike_price}"
				if strike_identifier in self._strikes_wo_option:
					continue

				try:
					optionStrikeData.strikeData[strike_price]
				except KeyError as keyErr:
					option_strike_price_data = OptionStrikePriceData()
					call_option_to_be_requested = Option(symbolData.symbol , expiration_date_str, strike_price, self._mappedRight(OptionRight.CALL), symbolInformation.exchange , tradingClass=symbolData.option_trading_class)
					list_of_details = await self._ib.reqContractDetailsAsync(call_option_to_be_requested)
					if len(list_of_details) == 0:
						logger.info(f'No Options available at strike {strike_price}')
						self._strikes_wo_option.append(expiration_date_str + '#' + str(strike_price))
						continue

					optionStrikeData.strikeData[strike_price] = option_strike_price_data

					put_option_to_be_requested = Option(symbolData.symbol , expiration_date_str, strike_price, self._mappedRight(OptionRight.PUT), symbolInformation.exchange , tradingClass=symbolData.option_trading_class)

					option_strike_price_data.brokerSpecific['call_contract'] = call_option_to_be_requested
					options_to_be_requested.append(call_option_to_be_requested)
				
					option_strike_price_data.brokerSpecific['put_contract'] = put_option_to_be_requested
					options_to_be_requested.append(put_option_to_be_requested)
		
		if len(options_to_be_requested) > 0:
			retries = 0
			symbolData.options_qualified = False
			qualifiedContracts = []
			while retries < 3:
				try:
					qualifiedContracts = await asyncio.wait_for(self._ib.qualifyContractsAsync(*options_to_be_requested), timeout=30)
					symbolData.options_qualified = True
					break
				except asyncio.TimeoutError:
					retries += 1
					logger.warning(f'Timeout while qualifying contracts. Retrying ({retries}) in 5 seconds ...')
					await asyncio.sleep(5)

			if not symbolData.options_qualified:
				logger.error(f'Error qualifying contracts when requesting option data!!')
				await self._set_ticker_data_status(False)
				from optrabot.tradinghubclient import NotificationType, TradinghubClient
				notification_message = f'‼️ Broker {self.broker}: Unable to retrieve options data. Trading will be disabled!'
				await TradinghubClient().send_notification(NotificationType.ERROR, notification_message)
				return

			for qualified_contract in qualifiedContracts:
				self._ib.reqMktData(qualified_contract, '', False, False)

	async def _set_ticker_data_status(self, okay: bool, reason: str = None) -> None:
		"""
		Sets the ticker data status
		"""
		self._ticker_data_ok = okay
		if okay:
			await self.set_trading_enabled(True, reason or 'Valid ticker data received')
		else:
			await self.set_trading_enabled(False, reason or 'No valid ticker data available')