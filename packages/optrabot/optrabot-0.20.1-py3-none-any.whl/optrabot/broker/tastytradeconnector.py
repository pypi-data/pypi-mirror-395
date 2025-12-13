import asyncio
import datetime as dt
import re
import ssl
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, List

import certifi
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from httpx import ConnectError
from loguru import logger
from pydantic import ValidationError
from tastytrade import Account, AlertStreamer, DXLinkStreamer, Session
from tastytrade.account import Transaction
from tastytrade.dxfeed import Candle, Greeks, Quote
from tastytrade.instruments import (NestedOptionChain, Option, OptionType,
                                    Strike)
from tastytrade.order import (NewComplexOrder, NewOrder, OrderAction,
                              OrderStatus, OrderTimeInForce, OrderType,
                              PlacedOrder)
from tastytrade.utils import TastytradeError
from websockets.exceptions import ConnectionClosedOK

import optrabot.config as optrabotcfg
import optrabot.symbolinfo as symbolInfo
from optrabot.broker.brokerconnector import BrokerConnector, SymbolData
from optrabot.broker.optionpricedata import (OptionStrikeData,
                                             OptionStrikePriceData)
from optrabot.broker.order import Execution
from optrabot.broker.order import Leg as GenericOrderLeg
from optrabot.broker.order import OptionRight
from optrabot.broker.order import Order as GenericOrder
from optrabot.broker.order import OrderAction as GenericOrderAction
from optrabot.broker.order import OrderStatus as GenericOrderStatus
from optrabot.broker.order import PriceEffect
from optrabot.exceptions.orderexceptions import (PlaceOrderException,
                                                 PrepareOrderException)
from optrabot.managedtrade import ManagedTrade
from optrabot.models import Account as ModelAccount
from optrabot.optionhelper import OptionHelper
from optrabot.tradetemplate.templatefactory import Template


@dataclass
class TastySymbolData(SymbolData):
	def __init__(self) -> None:
		super().__init__()
		self.tastySymbol: str = None
		self.chain: NestedOptionChain = None

class TastytradeConnector(BrokerConnector):
	task_listen_quotes: asyncio.Task = None

	def __init__(self) -> None:
		super().__init__()
		self._client_secret = ''
		self._refresh_token = ''
		self._sandbox = False
		self._initialize()
		self.id = 'TASTY'
		self.broker = 'TASTY'
		self._orders: List[GenericOrder] = []
		self._replacedOrders: List[PlacedOrder] = []
		self._processed_transaction_ids: List[int] = []
		self._is_disconnecting = False
		self._session: Session = None
		self._streamer: DXLinkStreamer = None
		self._alert_streamer: AlertStreamer = None
		self._quote_symbols = []
		self._candle_symbols = []
		self._greeks_symbols = []
		self._tasty_accounts: List[Account] = []
		self._symbolReverseLookup: Dict[str, str] = {}		# maps tastytrade symbol to generic symbol

		self.task_listen_quotes = None
		self.task_listen_accounts = None
		self.task_listen_greeks = None
		self.task_listen_candle = None

		self._backgroundScheduler = AsyncIOScheduler()

	def _initialize(self) -> None:
		"""
		Initialize the Tastytrade connector from the configuration
		"""
		if not optrabotcfg.appConfig:
			return
		
		config :optrabotcfg.Config = optrabotcfg.appConfig
		try:
			config.get('broker.tastytrade')
		except KeyError:
			logger.debug('No Tastytrade connection configured')
			return
		
		try:
			self._client_secret = config.get('broker.tastytrade.client_secret')
		except KeyError:
			logger.error('Tastytrade client_secret not configured')
			return
		
		try:
			self._refresh_token = config.get('broker.tastytrade.refresh_token')
		except KeyError:
			logger.error('Tastytrade refresh_token not configured')
			return
		
		try:
			self._sandbox = config.get('broker.tastytrade.sandbox')
		except KeyError:
			pass
		self._initialized = True

	async def cancel_order(self, order: GenericOrder) -> None:
		""" 
		Cancels the given order
		"""
		await super().cancel_order(order)
		tasty_order: PlacedOrder = order.brokerSpecific['order']
		account: Account = order.brokerSpecific['account']
		logger.debug(f'Cancelling order {tasty_order.id}')
		try:
			account.delete_order(self._session, str(tasty_order.id))
		except TastytradeError as tastyErr:
			logger.error(f'Error cancelling order {tasty_order.id}: {tastyErr}')
			raise

	async def connect(self) -> None:
		await super().connect()
		self._is_disconnecting = False
		try:
			#self._session = Session(self._username, self._password, is_test=self._sandbox)
			self._session = Session(provider_secret=self._client_secret, refresh_token=self._refresh_token, is_test=self._sandbox)
			await self.set_trading_enabled(True, 'Broker connected')
			
			# I Sandbox mode, there are SPX optins only
			if self._sandbox:
				spx_symbol_information = symbolInfo.symbol_infos['SPX']
				spx_symbol_information.trading_class = 'SPX'
				spx_symbol_information.option_symbol_suffix = ''

			# OTB-xxx: Verify session is ready by attempting to retrieve accounts
			# This prevents race conditions where connectedEvent is emitted before
			# the session is fully initialized and ready to handle API calls.
			# If successful, accounts are cached for subsequent getAccounts() calls.
			max_retries = 3
			session_ready = False
			for attempt in range(max_retries):
				try:
					self._tasty_accounts = Account.get(self._session)
					if len(self._tasty_accounts) > 0:
						logger.debug(f'Session verified - {len(self._tasty_accounts)} account(s) accessible')
						session_ready = True
						break
					else:
						logger.debug(f'Session not ready - no accounts found (attempt {attempt + 1}/{max_retries})')
				except Exception as e:
					logger.debug(f'Session verification failed (attempt {attempt + 1}/{max_retries}): {e}')

				if attempt < max_retries - 1:
					await asyncio.sleep(0.2)  # Brief delay between retries
			
			if not session_ready:
				logger.warning('Session created but verification failed after 3 attempts - proceeding with caution')
			
			self._backgroundScheduler.start()
			self._backgroundScheduler.add_job(self._perform_periodic_updates, 'interval', seconds=10, misfire_grace_time=None)

			self._emitConnectedEvent()
		except TastytradeError as tastyErr:
			logger.error('Failed to connect to Tastytrade: {}', tastyErr)
			self._emitConnectFailedEvent()
		except ConnectError:
			logger.debug('Failed to connect to Tastytrade - network connection error')
			self._emitConnectFailedEvent()

	async def _disconnect_internal(self) -> None:
		"""
		Perform the operations for disconnecting from Tastytrade
		"""
		# Note: _is_disconnecting should already be set to True before calling this method
		logger.debug('Starting _disconnect_internal')
		await self.set_trading_enabled(False, 'Broker disconnected')

		# FIRST: Close streamers gracefully to stop their internal _connect tasks
		# This prevents the RecursionError from nested task cancellation
		if self._streamer:
			try:
				logger.debug('Closing DXLink streamer')
				await asyncio.wait_for(self._streamer.close(), timeout=2.0)
				logger.debug('DXLink streamer closed')
			except asyncio.TimeoutError:
				logger.warning('Timeout closing DXLink streamer')
			except Exception as e:
				logger.debug(f'Error closing DXLink streamer: {e}')
		
		if self._alert_streamer:
			try:
				logger.debug('Closing Alert streamer')
				await asyncio.wait_for(self._alert_streamer.close(), timeout=2.0)
				logger.debug('Alert streamer closed')
			except asyncio.TimeoutError:
				logger.warning('Timeout closing Alert streamer')
			except Exception as e:
				logger.debug(f'Error closing Alert streamer: {e}')

		# SECOND: Now cancel our listener tasks (which should already be stopping)
		tasks_to_cancel = [
			task for task in [
				self.task_listen_quotes,
				self.task_listen_greeks,
				self.task_listen_candle,
				self.task_listen_accounts
			] if task and not task.done()
		]

		if tasks_to_cancel:
			logger.debug(f'Cancelling {len(tasks_to_cancel)} listener tasks')
			for task in tasks_to_cancel:
				task.cancel()
			
			# Give tasks a moment to process cancellation
			await asyncio.sleep(0.1)

		# THIRD: Clear streamer references
		logger.debug('Clearing streamer references')
		self._streamer = None
		self._alert_streamer = None
		logger.debug('Streamer references cleared')

		# FOURTH: Let event loop clean up cancelled tasks
		if tasks_to_cancel:
			logger.debug('Listener tasks cancelled - will be cleaned up by event loop')
		
		# Give event loop time to process cancellations
		await asyncio.sleep(0.1)

		# Clear task references
		self.task_listen_quotes = None
		self.task_listen_greeks = None
		self.task_listen_candle = None
		self.task_listen_accounts = None

		# Close session
		self._session = None
		
		# Clear cached account data
		self._tasty_accounts = []
		
		self._emitDisconnectedEvent()

	async def disconnect(self):
		"""
		Disconnect from Tastytrade broker.
		Sets _is_disconnecting flag BEFORE starting disconnect operations to prevent
		reconnect attempts from disconnect callbacks.
		"""
		await super().disconnect()
		# Set flag BEFORE calling _disconnect_internal to prevent reconnect attempts
		self._is_disconnecting = True
		await self._disconnect_internal()

	def getAccounts(self) -> List[ModelAccount]:
		"""
		Returns the Tastytrade accounts and starts the account update task for listening to updates on orders.
		Uses cached account data from connect() if available.
		"""
		if len(self._managedAccounts) == 0 and self.isConnected():
			# If accounts were not already loaded in connect(), load them now
			if len(self._tasty_accounts) == 0:
				self._tasty_accounts = Account.get(self._session)
			
			for tastyAccount in self._tasty_accounts:
				account = ModelAccount(id = tastyAccount.account_number, name = tastyAccount.nickname, broker = self.broker, pdt = not tastyAccount.day_trader_status)
				self._managedAccounts.append(account)

			# Store the task reference so we can cancel it during disconnect
			self.task_listen_accounts = asyncio.create_task(self._request_account_updates())
		return self._managedAccounts
	
	def isConnected(self) -> bool:
		return self._session is not None
		
	async def prepareOrder(self, order: GenericOrder, need_valid_price_data: bool = True) -> None:
		"""
		Prepares the given order for execution

		Args:
			order: The order to prepare
			need_valid_price_data: If True, validates price data availability and freshness.
								   If False, creates order legs without price validation (e.g., for trade recovery)

		Raises:
			PrepareOrderException: If the order preparation fails with a specific reason.
		"""
		symbolData = self._symbolData[order.symbol]
		comboLegs: list[GenericOrderLeg] = []
		for leg in order.legs:
			optionInstrument: Option = None
			
			if need_valid_price_data:
				# Normal order flow: use price data with validation
				try:
					optionPriceData = symbolData.optionPriceData[leg.expiration]
				except KeyError as keyErr:
					raise PrepareOrderException(f'No option price data for expiration date {leg.expiration} available!', order)

				try:
					priceData: OptionStrikePriceData = optionPriceData.strikeData[leg.strike]
					if not priceData.is_outdated():
						if leg.right == OptionRight.CALL:
							leg.askPrice = float(priceData.callAsk)
							if leg.askPrice == None:
								leg.askPrice = 0
							leg.bidPrice = float(priceData.callBid)
							if leg.bidPrice == None:
								leg.bidPrice = 0
							optionInstrument = Option.get(self._session, priceData.brokerSpecific['call_option'])
						elif leg.right == OptionRight.PUT:
							leg.askPrice = float(priceData.putAsk)
							if leg.askPrice == None:
								leg.askPrice = 0
							leg.bidPrice = float(priceData.putBid)
							if leg.bidPrice == None:
								leg.bidPrice = 0
							optionInstrument = Option.get(self._session, priceData.brokerSpecific['put_option'])
					else:
						raise PrepareOrderException(f'Price data for strike {leg.strike} is outdated or not available!', order)

				except KeyError as keyErr:
					# No data for strike available
					raise PrepareOrderException(f'No option price data for strike {leg.strike} available!', order)
				except Exception as excp:
					raise PrepareOrderException(f'Error preparing order: {excp}', order)
			else:
				# Trade recovery flow: create option instrument without price data validation
				try:
					# Use the cached option chain from symbolData
					if symbolData.chain is None:
						raise PrepareOrderException(
							f'No option chain available for {order.symbol} - symbol data may not be initialized', 
							order
						)
					
					# Find the specific option in the cached chain
					for expiration in symbolData.chain.expirations:
						if expiration.expiration_date == leg.expiration:
							for strike in expiration.strikes:
								if abs(float(strike.strike_price) - leg.strike) < 0.01:  # Float comparison tolerance
									if leg.right == OptionRight.CALL and strike.call is not None:
										optionInstrument = Option.get(self._session, strike.call)
										leg.askPrice = 0
										leg.bidPrice = 0
										break
									elif leg.right == OptionRight.PUT and strike.put is not None:
										optionInstrument = Option.get(self._session, strike.put)
										leg.askPrice = 0
										leg.bidPrice = 0
										break
							if optionInstrument:
								break
					
					if optionInstrument is None:
						raise PrepareOrderException(
							f'Could not find option instrument for {order.symbol} {leg.expiration} {leg.strike} {leg.right}', 
							order
						)
				except PrepareOrderException:
					raise
				except Exception as e:
					raise PrepareOrderException(f'Error creating option instrument for trade recovery: {e}', order)
			
			# Build the leg for the tasty trade order
			mapped_action = self._mappedOrderAction(order.action, leg.action)
			logger.debug(f'Mapping order.action={order.action} leg.action={leg.action} -> mapped_action={mapped_action}')
			comboLeg = optionInstrument.build_leg(quantity=Decimal(leg.quantity * order.quantity), action=mapped_action)
			comboLegs.append(comboLeg)
			leg.brokerSpecific['tasty_symbol'] = comboLeg.symbol  # Memorize the tastytrade symbol identifier for later transaction processing

		order.brokerSpecific['comboLegs'] = comboLegs
		order.determine_price_effect()
		return True
	
	def _transform_generic_order(self, generic_order: GenericOrder) -> NewOrder:
		"""
		Transforms the given generic order to a tastytrade order
		"""
		new_order_legs = generic_order.brokerSpecific['comboLegs']
		price = abs(generic_order.price)
		tasty_price = Decimal(price * -1 if generic_order.price_effect == PriceEffect.DEBIT else price)
		rounded_tasty_price: Decimal = round(tasty_price, 2)
		new_order = None
		if generic_order.type == OrderType.LIMIT:
			new_order = NewOrder(
				time_in_force=OrderTimeInForce.DAY,
				order_type=generic_order.type,	
				legs=new_order_legs,
				price=rounded_tasty_price
			)
		elif generic_order.type == OrderType.STOP:
			if len(generic_order.legs) == 1:
				new_order = NewOrder(
					time_in_force=OrderTimeInForce.DAY,
					order_type=generic_order.type,	
					legs=new_order_legs,
					stop_trigger=rounded_tasty_price
				)
			else:
				# Stop Orders with multiple legs must be Stop Limit Orders
				calculated_limit_price = OptionHelper.roundToTickSize(round(rounded_tasty_price * Decimal('1.25'), 2))  # Round to the nearest tick size
				tasty_limit_price: Decimal = Decimal(calculated_limit_price)
				
				new_order = NewOrder(
					time_in_force=OrderTimeInForce.DAY,
					order_type=OrderType.STOP_LIMIT,
					legs=new_order_legs,
					stop_trigger=Decimal(abs(rounded_tasty_price)),
					price=tasty_limit_price
				)
		return new_order
	
	async def placeOrder(self, managed_trade: ManagedTrade, order: GenericOrder, parent_order: GenericOrder = None) -> None:
		""" 
		Places the given order for a managed account via the broker connection.
		
		Raises:
			PlaceOrderException: If the order placement fails with a specific reason.
		"""
		account = Account.get(self._session, managed_trade.template.account)
		newOrder = self._transform_generic_order(order)
		try:
			response = account.place_order(self._session, newOrder, dry_run=False)
			#placedComplexOrders = account.get_live_complex_orders(session=self._session)
			#placedOrders = account.get_live_orders(session=self._session)
			#for order in placedOrders:
			#	logger.debug(f'Live order: {order.id} underlying: {order.underlying_symbol}')
			#	#account.delete_order(session=self._session, order_id=order.id)
			logger.debug(f'Response of place Order: {response}')
			if response.errors:
				for errorMessage in response.errors:
					raise PlaceOrderException(errorMessage, order=order)
			if response.warnings:
				for warningMessage in response.warnings:
					logger.warning(f'Warning placing order: {warningMessage}')
			
			order.brokerSpecific['order'] = response.order
			order.brokerSpecific['account'] = account
			self._orders.append(order)
			logger.debug(f'Order {response.order.id} placed successfully')
		except TastytradeError as tastyErr:
			raise PlaceOrderException(f'{tastyErr}', order=order)
		except ValidationError as valErr:
			logger.error(f'Validation error placing order: {valErr}')
			err = valErr.errors()[0]
			logger.error(err)
		except Exception as exc:
			raise PlaceOrderException(f'{exc}', order=order)

	async def place_complex_order(self, take_profit_order: GenericOrder, stop_loss_order: GenericOrder, template: Template) -> bool:
		"""
		Places the Take Profit and Stop Loss Order as complex order
		"""
		account = Account.get(self._session, template.account)
		new_order_tp = self._transform_generic_order(take_profit_order)
		new_order_sl = self._transform_generic_order(stop_loss_order)
		oco_order = NewComplexOrder( orders=[ new_order_tp, new_order_sl ] )
		try:
			dry_run = False
			response = account.place_complex_order(self._session, oco_order, dry_run=dry_run)
			logger.debug(f'Response of place_complex_order: {response}')
			if response.errors:
				for errorMessage in response.errors:
					logger.error(f'Error placing order: {errorMessage}')
					return False
			if response.warnings:
				for warningMessage in response.warnings:
					logger.warning(f'Warning placing order: {warningMessage}')
			
			try:
				take_profit_order.brokerSpecific['order'] = response.complex_order.orders[0]
				take_profit_order.brokerSpecific['account'] = account
				self._orders.append(take_profit_order)
			except IndexError as indexErr:
				logger.error(f'Error complex order. Take Profit order not found in complex order response!')
				return False

			try: 
				stop_loss_order.brokerSpecific['order'] = response.complex_order.orders[1]
				stop_loss_order.brokerSpecific['account'] = account
				self._orders.append(stop_loss_order)
			except IndexError as indexErr:
				logger.error(f'Error complex order. Stop Loss order not found in complex order response!')
				return False

			logger.debug(f'Complex Order {response.complex_order.id} placed successfully')
			return True
		except TastytradeError as tastyErr:
			logger.error(f'Error placing order: {tastyErr}')
		except ValidationError as valErr:
			logger.error(f'Validation error placing order: {valErr}')
			err = valErr.errors()[0]
			logger.error(err)
			#logger.error(repr(valErr.errors()[0]['type']))
		except Exception as exc:
			logger.error(f'Unexpected exception placing order: {exc}')
			
		return False		
		
	async def adjustOrder(self, managed_trade: ManagedTrade, order: GenericOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		if order.status == GenericOrderStatus.FILLED:
			logger.info('Order {} is already filled. Adjustment not required.', order)
			return True
		try:
			tasty_order: PlacedOrder = order.brokerSpecific['order']
		except KeyError as keyErr:
			logger.error(f'Order {order.broker_order_id} not prepared for adjustment. Cannot adjust order.')
			return False
		
		account: Account = order.brokerSpecific['account']
		logger.debug(f'Adjusting order {tasty_order.id} to price {price}')

		order.price = price
		replacement_order = self._transform_generic_order(order)

		#new_order_legs = order.brokerSpecific['comboLegs']
		#new_price = abs(price)
		#tasty_price = Decimal(new_price * -1 if order.price_effect == PriceEffect.DEBIT else new_price)

		# if order.type == OrderType.LIMIT:
		# 	replacement_order = NewOrder(
		# 		time_in_force=OrderTimeInForce.DAY,
		# 		order_type=order.type,	
		# 		legs=new_order_legs,
		# 		price=tasty_price
		# 	)
		# elif order.type == OrderType.STOP:
		# 	replacement_order = NewOrder(
		# 		time_in_force=OrderTimeInForce.DAY,
		# 		order_type=order.type,	
		# 		legs=new_order_legs,
		# 		stop_trigger=tasty_price
		# 	)
		# elif order.type == OrderType.MARKET:
		# 	replacement_order = NewOrder(
		# 		time_in_force=OrderTimeInForce.DAY,
		# 		order_type=order.type,	
		# 		legs=new_order_legs
		# 	)

		try:
			self._replacedOrders.append(tasty_order)  # Merken für das Cancel Event dieser Order
			response: PlacedOrder = account.replace_order(session=self._session, old_order_id=tasty_order.id, new_order=replacement_order)
			order.brokerSpecific['order'] = response
			#self._replacedOrders.append(response) # Auch die neue Order zu den zu ignorierenden Orders hinzufügen
			logger.debug(f'Replacment order {response.id} submitted successfully')
			return True
		
		except TastytradeError as tastyErr:
			logger.error(f'Error adjusting order: {tastyErr}')
			return False
		except ValidationError as valErr:
			logger.error(f'Validation error adjusting order: {valErr}')
			err = valErr.errors()[0]
			logger.error(err)
			return False 

	async def _perform_periodic_updates(self) -> None:
		"""
		Background job for fetching new transactions from Tastytrade for order executions.
		This is required for getting the commission and fee data.
		Additionally it checks if the access token needs to be refreshed.
		"""
		try:
			if not self.isConnected():
				return
			
			# Check if access token needs to be refreshed
			from tastytrade.utils import now_in_new_york
			if self._session.session_expiration < now_in_new_york() + timedelta(seconds=25):
				logger.debug('Access token is about to expire, refreshing...')
				self._session.refresh()

			for tasty_account in self._tasty_accounts:
				transactions =  tasty_account.get_history(self._session, start_date=dt.date.today())
				for transaction in transactions:
					if transaction.transaction_type != 'Trade' or transaction.id in self._processed_transaction_ids:
						continue
					self._processed_transaction_ids.append(transaction.id)
					await self._process_transaction(tasty_account, transaction)
		
		except Exception as e:
			logger.error(f'Error fetching new transactions: {e}')

	async def _process_transaction(self, account: Account, transaction: Transaction) -> None:
		"""
		Process a transaction from Tastytrade and report the fill and commission report events.
		"""
		logger.debug(f'Processing transaction {transaction.id}')

		# Find the corresponding generic order
		generic_order: GenericOrder = None
		tasty_order: PlacedOrder = None
		for order in self._orders:
			tasty_order = order.brokerSpecific['order']
			if tasty_order.id == transaction.order_id:
				generic_order = order
				break
		if generic_order is None:
			logger.debug(f'No matching generic order found for transaction {transaction.id} (order ID {transaction.order_id})')
			return

		# Emit a order execution details event for the transaction
		action = OrderAction.BUY if transaction.transaction_sub_type in ['Buy to Open', 'Buy to Close'] else OrderAction.SELL
		
		# Determine the matching leg of the order based on the tastytrade symbol
		matching_leg = None
		for leg in generic_order.legs:
			tasty_symbol = leg.brokerSpecific.get('tasty_symbol', None)
			if tasty_symbol == transaction.symbol:
				matching_leg = leg
				break
		if matching_leg is None:
			logger.error(f'Unexpected Error: No matching leg found in order {tasty_order.id} for transaction symbol {transaction.symbol}')
			return
		
		sec_type = 'C' if matching_leg.right == OptionRight.CALL else 'P'

		execution = Execution(
			id=str(transaction.id),
			action=action,
			sec_type=sec_type,
			strike=matching_leg.strike,
			amount=int(transaction.quantity),
			price=float(transaction.price),
			expiration=matching_leg.expiration,
			timestamp=transaction.executed_at
			)
		logger.debug(f'Emitting execution details for Tastytrade order {tasty_order.id}: {matching_leg.symbol} {matching_leg.right} {matching_leg.strike} qty={execution.amount} @ ${execution.price}')
		self._emitOrderExecutionDetailsEvent(generic_order, execution)

		# Calculate total fees and commission and emit commission report event
		commission: float = abs(float(transaction.commission))
		fee: float = float(abs(transaction.regulatory_fees) + abs(transaction.clearing_fees) + abs(transaction.proprietary_index_option_fees))
		self._emitCommissionReportEvent(order=generic_order, execution_id=str(transaction.id), commission=commission, fee=fee)

	async def _on_alert_streamer_disconnect(self, streamer: AlertStreamer):
		"""
		Callback method which is called when the Tastytra	de alert streamer disconnects.
		Reconnects only the alert streamer without affecting the DXLink streamer.
		"""
		try:
			logger.debug("Tastytrade Alert Streamer disconnected.")
			
			# Check if we're already disconnecting OR if the DXLink streamer is also disconnected
			# (indicating a full disconnect scenario, not just an Alert Streamer issue)
			if self._is_disconnecting:
				logger.debug("Already disconnecting, skipping Alert Streamer reconnect")
				return
			
			if self._streamer is None:
				logger.debug("DXLink streamer is also disconnected (None) - this is a full disconnect, not an Alert Streamer reconnect scenario")
				return
			
			if self._is_disconnecting == False:
				logger.warning("Alert Streamer disconnected unexpectedly. Reconnecting Alert Streamer...")
			
			# CRITICAL: Close the old alert streamer FIRST to stop the async for loop
			# This prevents the old task from receiving events after being cancelled
			old_streamer = self._alert_streamer
			old_streamer_id = id(old_streamer) if old_streamer else None
			self._alert_streamer = None  # Clear reference immediately to prevent race conditions
			logger.debug(f'Set _alert_streamer to None (old streamer was {old_streamer_id})')
			
			if old_streamer:
				try:
					logger.debug(f'Closing old alert streamer {old_streamer_id}')
					await asyncio.wait_for(old_streamer.close(), timeout=2.0)
					logger.debug(f'Old alert streamer {old_streamer_id} closed successfully')
				except asyncio.TimeoutError:
					logger.warning(f'Timeout while closing old alert streamer {old_streamer_id} - continuing anyway')
				except asyncio.CancelledError:
					logger.warning(f'Close operation cancelled for alert streamer {old_streamer_id} - continuing anyway')
				except Exception as exc:
					logger.warning(f'Error closing old alert streamer {old_streamer_id}: {exc} - continuing anyway')
			
			# Now cancel the account listening task (it should exit cleanly now)
			old_task_id = id(self.task_listen_accounts) if self.task_listen_accounts else None
			if self.task_listen_accounts and not self.task_listen_accounts.done():
				logger.debug(f'Cancelling account listening task {old_task_id}')
				self.task_listen_accounts.cancel()
				# Wait for the task using gather to avoid recursion issues
				try:
					await asyncio.wait_for(
						asyncio.gather(self.task_listen_accounts, return_exceptions=True),
						timeout=2.0
					)
					logger.debug(f'Account listening task {old_task_id} cancelled successfully')
				except asyncio.TimeoutError:
					logger.warning(f'Timeout waiting for account listening task {old_task_id} to cancel - continuing anyway')
				except asyncio.CancelledError:
					logger.debug(f'Account listening task {old_task_id} already cancelled')
				except Exception as exc:
					logger.warning(f'Error waiting for account listening task to cancel: {exc} - continuing anyway')
			else:
				logger.debug(f'Account listening task already done or None, no need to cancel')
			
			# Small delay to ensure everything is cleaned up
			logger.debug('Waiting 0.5s for cleanup before reconnecting')
			await asyncio.sleep(0.5)
			
			# Restart the account updates task which will create a new alert streamer
			try:
				# Check if event loop is still running before creating new task
				loop = asyncio.get_event_loop()
				if loop.is_running():
					self.task_listen_accounts = asyncio.create_task(self._request_account_updates())
					new_task_id = id(self.task_listen_accounts)
					logger.info(f"Alert Streamer reconnected successfully (new task {new_task_id})")
				else:
					logger.debug("Event loop not running, skipping Alert Streamer reconnect")
			except RuntimeError as runtime_err:
				logger.warning(f'Cannot reconnect Alert Streamer: {runtime_err}')
			except Exception as exc:
				logger.error(f'Error reconnecting Alert Streamer: {exc}')
		except Exception as e:
			logger.error(f"Critical error in _on_alert_streamer_disconnect: {e}", exc_info=True)

	async def _handle_alert_streamer_error(self, error: Exception):
		"""
		Handle fatal errors from the AlertStreamer (e.g., AUTH timeout).
		
		OTB-264: When the AlertStreamer encounters a fatal error that doesn't trigger
		the disconnect callback, we need to manually initiate a reconnect.
		
		This handles cases like:
		- "The timeout for waiting for AUTH has been reached"
		- Connection errors during streaming
		"""
		try:
			logger.warning(f'AlertStreamer fatal error: {error}. Attempting reconnect...')
			
			# Check if we should attempt reconnect
			if self._is_disconnecting:
				logger.debug('Already disconnecting, skipping AlertStreamer reconnect after error')
				return
			
			if self._streamer is None:
				logger.debug('DXLink streamer is None - this may be a full disconnect scenario')
				# Emit disconnected event to trigger full reconnection
				self._emitDisconnectedEvent()
				return
			
			# Clean up the old alert streamer
			old_streamer = self._alert_streamer
			self._alert_streamer = None
			
			if old_streamer:
				try:
					await asyncio.wait_for(old_streamer.close(), timeout=2.0)
				except Exception as close_err:
					logger.debug(f'Error closing old alert streamer after error: {close_err}')
			
			# Wait a bit before reconnecting to avoid rapid reconnect loops
			await asyncio.sleep(2.0)
			
			# Check again if we should reconnect (state may have changed during sleep)
			if self._is_disconnecting or self._streamer is None:
				logger.debug('State changed during wait, skipping AlertStreamer reconnect')
				return
			
			# Create a new task to handle account updates (which creates a new AlertStreamer)
			try:
				loop = asyncio.get_event_loop()
				if loop.is_running():
					self.task_listen_accounts = asyncio.create_task(self._request_account_updates())
					logger.info('AlertStreamer reconnect initiated after fatal error')
				else:
					logger.debug('Event loop not running, cannot reconnect AlertStreamer')
			except RuntimeError as runtime_err:
				logger.warning(f'Cannot reconnect AlertStreamer: {runtime_err}')
				
		except Exception as e:
			logger.error(f'Error handling AlertStreamer error: {e}', exc_info=True)

	async def _on_streamer_disconnect(self, streamer: DXLinkStreamer):
		"""
		Callback method which is called when the Tastytrade streamer disconnects.
		
		OTB-236: This callback may be invoked by the tastytrade library during shutdown
		when the event loop is already closing. We need to:
		1. Check if event loop is still running
		2. Avoid calling _disconnect_internal() which would try to close the streamer again (recursion!)
		3. Handle unexpected disconnects without causing infinite loops
		"""
		try:
			logger.debug(f'Tastytrade Streamer disconnect callback triggered (_is_disconnecting={self._is_disconnecting})')
			
			if self._backgroundScheduler.running:
				self._backgroundScheduler.remove_all_jobs()
				self._backgroundScheduler.shutdown(wait=False)

			# Check if we're already in the process of disconnecting
			if self._is_disconnecting:
				logger.debug('Already disconnecting, ignoring streamer disconnect callback')
				return
			
			# OTB-236: Check if event loop is still running to avoid RuntimeError during shutdown
			try:
				loop = asyncio.get_running_loop()  # noqa: F841
				# Note: is_closing() is not available in Python 3.11, only check if loop exists
				logger.debug('Event loop is running')
			except RuntimeError as e:
				logger.debug(f'Event loop not running, ignoring streamer disconnect callback (shutdown in progress): {e}')
				return
			
			# Handle unexpected disconnect (not during our controlled shutdown)
			logger.warning('Unexpected DXLink streamer disconnect detected. Initiating full reconnection...')
			logger.debug(f'Streamer: {id(self._streamer) if self._streamer else None}, Alert Streamer: {id(self._alert_streamer) if self._alert_streamer else None}')
			
			# OTB-236: Set flag BEFORE any operations to prevent recursive calls
			self._is_disconnecting = True
			
			# OTB-236: Don't call _disconnect_internal() here as it will try to close the streamer again!
			# Instead, manually clean up and trigger reconnection via the disconnected event
			
			# Disable trading immediately
			await self.set_trading_enabled(False, 'Streamer disconnected unexpectedly')
			
			# Cancel streaming tasks - use gather with return_exceptions to avoid recursion
			tasks_to_cancel = [
				task for task in [
					self.task_listen_quotes,
					self.task_listen_greeks,
					self.task_listen_candle,
					self.task_listen_accounts
				] if task and not task.done()
			]
			
			if tasks_to_cancel:
				# Cancel all tasks
				for task in tasks_to_cancel:
					task.cancel()
				
				# Wait for cancellation to complete
				try:
					await asyncio.wait_for(
						asyncio.gather(*tasks_to_cancel, return_exceptions=True),
						timeout=2.0
					)
					logger.debug(f'All {len(tasks_to_cancel)} streaming tasks cancelled')
				except asyncio.TimeoutError:
					logger.debug(f'Timeout waiting for streaming tasks to cancel')
				except Exception as e:
					logger.debug(f'Error waiting for streaming tasks to cancel: {e}')
			
			# Clear task references
			self.task_listen_quotes = None
			self.task_listen_greeks = None
			self.task_listen_candle = None
			self.task_listen_accounts = None
			
			# Clear streamer references (don't call close() - it's already closing!)
			self._streamer = None
			self._alert_streamer = None
			
			# Emit the disconnected event to trigger reconnection logic
			self._emitDisconnectedEvent()
		except Exception as e:
			logger.error(f'Unexpected error in _on_streamer_disconnect: {e}', exc_info=True)
	
	async def _subscribe_data(self) -> None:
		"""
		Subscribe to the required data
		"""
		logger.debug('Subscribing to streaming data')
		await self._streamer.subscribe(Quote, self._quote_symbols)
		await self._streamer.subscribe(Greeks, self._greeks_symbols)
		start_time = dt.datetime.now() - timedelta(days=1)
		await self._streamer.subscribe_candle(self._candle_symbols, interval='1m', start_time=start_time)

	async def requestTickerData(self, symbols: List[str]) -> None:
		""" 
		Request ticker data for the given symbols and their options
		"""
		# Check if this is the first call (initial setup) or a re-subscription (e.g., after EOD settlement)
		is_initial_setup = self._streamer is None
		if is_initial_setup:
			ssl_context = ssl.create_default_context(cafile=certifi.where())
			self._streamer = await DXLinkStreamer(self._session, ssl_context=ssl_context, disconnect_fn=self._on_streamer_disconnect)

			self._quote_symbols = []
			self._candle_symbols = []
			self._greeks_symbols = symbols

			# Initial setup: Create new symbolData objects
			for symbol in symbols:
				match symbol:
					case 'SPX':
						symbolData = TastySymbolData()
						symbolData.symbol = symbol
						symbolData.tastySymbol = 'SPX'
						self._quote_symbols.append('SPX')
						self._symbolData[symbol] = symbolData
						self._symbolReverseLookup[symbolData.tastySymbol] = symbol
					case 'VIX':
						symbolData = TastySymbolData()
						symbolData.symbol = symbol
						symbolData.tastySymbol = 'VIX'
						symbolData.trade_options = False  # No options for VIX
						self._candle_symbols.append('VIX')
						self._symbolData[symbol] = symbolData
						self._symbolReverseLookup[symbolData.tastySymbol] = symbol
					case _:
						logger.error(f'Symbol {symbol} currently not supported by Tastytrade Connector!')
						continue

			# Request option chains and expirations for symbols with options trading enable
			current_date = dt.date.today()
			for item in self._symbolData.values():
				symbol_data: TastySymbolData = item
				desired_chain = None
				if symbol_data.trade_options:
					# If options are enabled, request the option chain and expirations
					symbol_information = symbolInfo.symbol_infos[symbol_data.symbol]
					chains = NestedOptionChain.get(self._session, symbol_data.tastySymbol)
					for chain in chains:
						if chain.root_symbol == symbol_information.trading_class:
							desired_chain = chain
							break
					if not desired_chain:
						logger.error(f'No option chain found for symbol {symbol_data.symbol} with trading class {symbol_information.trading_class}!')
						continue
					symbol_data.chain = desired_chain

					got_strikes = False
					for expiration in desired_chain.expirations:
						if expiration.expiration_date < current_date:
							continue
						symbol_data.expirations.append(expiration.expiration_date)
						if not got_strikes:
							# Obtain strikes of the first expiration only
							for strike in expiration.strikes:
								symbol_data.strikes.append(float(strike.strike_price))
							got_strikes = True

					if current_date > symbol_data.expirations[0]:
						logger.warning(f'There are no {symbol_data.symbol} options expiring today!')

			# OTB-253: Symbol data is now ready for trade recovery to use
			# Start subscribe operations in background (don't await - they can take 2+ seconds)
			# This prevents blocking trade recovery which needs symbol data but not live streaming yet
			logger.debug('Symbol data loaded, starting streaming subscriptions in background')
			
			# Start subscribe and streaming tasks in background
			asyncio.create_task(self._start_streaming_async())
		else:
			# Re-subscription after EOD settlement: Keep existing symbolData, just re-subscribe
			logger.debug('Re-subscribing to ticker data after EOD settlement (keeping existing symbolData)')
			
			# Re-subscribe to base symbols (SPX, VIX) - these should still be in the lists
			await self._subscribe_data()
			
			# Mark ticker data as subscribed again
			self._subscribed_ticker_data = True
			logger.debug('Ticker data re-subscription completed')

	async def _start_streaming_async(self) -> None:
		"""
		OTB-253: Start streaming subscriptions and tasks asynchronously.
		This method runs in the background to avoid blocking trade recovery.
		"""
		try:
			# Subscribe to data (this can take 2+ seconds due to network calls)
			await self._subscribe_data()
			self._subscribed_ticker_data = True
			
			# OTB-xxx: Start streaming tasks but don't wait for them (they run indefinitely)
			# These tasks will be cancelled during disconnect via _disconnect_internal()
			if self.task_listen_quotes is None:
				self.task_listen_quotes = asyncio.create_task(self._update_quotes())
				self.task_listen_greeks = asyncio.create_task(self._update_greeks())
				self.task_listen_candle = asyncio.create_task(self._update_candle())
				logger.debug('Started streaming tasks for quotes, greeks, and candles')
		except Exception as e:
			logger.error(f'Failed to start streaming: {e}', exc_info=True)

	async def _update_accounts(self):
		"""
		Task for listening to account updates
		"""
		logger.debug(f'_update_accounts started, alert_streamer={id(self._alert_streamer) if self._alert_streamer else None}')
		try:
			# Check if streamer is still valid before entering the loop
			if self._alert_streamer is None:
				logger.debug('Alert streamer is None, cannot start account updates loop')
				return
			
			streamer_id = id(self._alert_streamer)
			logger.debug(f'Starting async for loop with streamer {streamer_id}')
			async for order in self._alert_streamer.listen(PlacedOrder):
				logger.debug(f'Received order event in loop (streamer {streamer_id}): {order.id} status {order.status}')
				additional_info = ''
				if order.status == OrderStatus.REJECTED:
					additional_info = f'Reason: {order.reject_reason}'
				logger.debug(f'Update on order {order.id} status {order.status} {additional_info}')			
				ignore_order_event = False
				# Cancel Events von Preisanpassungen ignorieren, da sie kein echtes Cancel sind
				for replaced_order in self._replacedOrders:
					if replaced_order.id == order.id and order.status == OrderStatus.CANCELLED:
						#self._replacedOrders.remove(replaced_order)
						ignore_order_event = True
						logger.debug('Ignoring cancel event for replaced order')
						continue
					if replaced_order.id == order.id and (order.status == OrderStatus.ROUTED or order.status == OrderStatus.LIVE):
						if order.status == OrderStatus.LIVE:
							self._replacedOrders.remove(replaced_order)
						ignore_order_event = True
						logger.debug('Ignoring placement of new replacement order')
						continue
		
				if not ignore_order_event:
					relevantOrder: GenericOrder = None
					for managedOrder in self._orders:
						broker_specific_order: PlacedOrder = managedOrder.brokerSpecific['order']
						if broker_specific_order.id == order.id:
							relevantOrder = managedOrder
							break
				
					if relevantOrder == None:
						logger.debug(f'No managed order matched the status event')
					else:
						relevantOrder.brokerSpecific['order'] = order
						filledAmount = int(order.size)
						relevantOrder.averageFillPrice = abs(float(order.price)) if order.price != None else 0
						order_status =	self._genericOrderStatus(order.status)
						if order_status and order_status != relevantOrder.status:
							self._emitOrderStatusEvent(relevantOrder, order_status, filledAmount)
							# Emit execution details when order is filled
							#if order.status == OrderStatus.FILLED:
							#	logger.debug(f'Order {order.id} is filled, emitting execution details')
							#	self._emit_execution_details_for_order(relevantOrder, order)
						else:
							logger.debug(f'Order status {order.status} not mapped to generic order status')
		except asyncio.CancelledError:
			logger.debug(f'Account updates task cancelled, stopping order listener (streamer {id(self._alert_streamer) if self._alert_streamer else None})')
			raise  # Re-raise to allow proper task cancellation
		except Exception as exc:
			logger.error(f'Unexpected error in _update_accounts: {exc}', exc_info=True)
		finally:
			logger.debug(f'_update_accounts exiting (streamer {id(self._alert_streamer) if self._alert_streamer else None})')

	async def _update_quotes(self):
		async for e in self._streamer.listen(Quote):
			logger.trace(f'Received Quote: {e.event_symbol} bid price: {e.bid_price} ask price: {e.ask_price}')
			# Preisdaten speichern if the broker is subscribed to ticker data
			if self._subscribed_ticker_data is None:
				continue

			if not e.event_symbol.startswith('.'):
				# Symbol ist ein Basiswert
				try:
					genericSymbol = self._symbolReverseLookup[e.event_symbol]
					symbolData: TastySymbolData  = self._symbolData[genericSymbol]
					midPrice = float((e.bid_price + e.ask_price) / 2)
					atmStrike = OptionHelper.roundToStrikePrice(midPrice)
					symbolData.lastPrice = midPrice
					if symbolData.lastAtmStrike != atmStrike:  # Check for missing Option Data only if ATM Strike has changed
						symbolData.lastAtmStrike = atmStrike
						asyncio.create_task(self._requestMissingOptionData(symbolData, atmStrike))
					
				except KeyError as keyErr:
					logger.error(f'No generic symbol found for tastytrade symbol {e.event_symbol}')
			else:
				# Symbol ist eine Option
				try:
					symbol, optionType, expiration, strike = self._getOptionInfos(e.event_symbol)
					symbol_information = symbolInfo.symbol_infos[symbol]
					symbolData = self._symbolData[symbol]
					optionStrikeData = symbolData.optionPriceData[expiration]
					optionStrikePriceData = optionStrikeData.strikeData[strike]
					if optionType == OptionType.CALL:
						optionStrikePriceData.callBid = float(e.bid_price)
						optionStrikePriceData.callAsk = float(e.ask_price)
					else:
						optionStrikePriceData.putBid = float(e.bid_price)
						optionStrikePriceData.putAsk = float(e.ask_price)
					optionStrikePriceData.lastUpdated = dt.datetime.now(symbol_information.timezone)
					self._last_option_price_update_time = optionStrikePriceData.lastUpdated
					await self._monitor_bid_ask_spread(optionStrikePriceData, genericSymbol, strike)
				except Exception as exc:
					logger.error(f'Error getting option infos: {exc}')
	
	async def _update_greeks(self):
		async for e in self._streamer.listen(Greeks):
			logger.trace(f'Received Greeks: {e.event_symbol} delta: {e.delta}')
			if e.event_symbol.startswith('.'):
				# Symbol ist eine Option
				try:
					symbol, optionType, expiration, strike = self._getOptionInfos(e.event_symbol)
					symbol_information = symbolInfo.symbol_infos[symbol]
					symbolData = self._symbolData[symbol]
					optionStrikeData = symbolData.optionPriceData[expiration]
					optionStrikePriceData = optionStrikeData.strikeData[strike]
					if optionType == OptionType.CALL:
						optionStrikePriceData.callDelta = float(e.delta)
					else:
						optionStrikePriceData.putDelta = float(e.delta)

				except Exception as exc:
					logger.error(f'Error getting option infos: {exc}')

	async def _update_candle(self):
		async for e in self._streamer.listen(Candle):
			logger.trace(f'Received Candle: {e.event_symbol} close: {e.close}')
			if not e.event_symbol.startswith('.'):
				# Symbol ist ein Basiswert
				try:
					symbol = e.event_symbol.split('{')[0]
					genericSymbol = self._symbolReverseLookup[symbol]
					symbolData: TastySymbolData  = self._symbolData[genericSymbol]
					symbolData.lastPrice = float(e.close)
				except KeyError as keyErr:
					logger.error(f'No generic symbol found for tastytrade symbol {e.event_symbol}')

	async def eod_settlement_tasks(self) -> None:
		"""
		Perform End of Day settlement tasks
		"""
		await super().eod_settlement_tasks()

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

	def get_option_strike_price_data(self, symbol: str, expiration: date, strike: float) -> OptionStrikePriceData:
		""" 
		Returns the option strike price data for the given symbol, expiration date, strike price and right.
		Returns None if no price data is available for the expiration date or strike.
		"""
		symbolData = self._symbolData[symbol]
		try:
			optionStrikeData = symbolData.optionPriceData[expiration]
		except KeyError:
			# No price data available for this expiration date (e.g., after trade recovery)
			return None
		
		if strike in optionStrikeData.strikeData.keys():
			return optionStrikeData.strikeData[strike]
		else:
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
		# TODO: Implement in base class, because TWS Connector got the same code
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

	def getFillPrice(self, order: GenericOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		try:
			tastyOrder: PlacedOrder = order.brokerSpecific['order']
			if tastyOrder.status == OrderStatus.FILLED:
				return abs(float(tastyOrder.price))
			else:
				return 0
		except KeyError as keyErr:
			logger.error(f'No fill price available for order {order}')
	
	def getLastPrice(self, symbol: str) -> float:
		""" 
		Returns the last price of the given symbol
		"""
		try:
			symbolData = self._symbolData[symbol]
			return symbolData.lastPrice
		except KeyError as keyErr:
			logger.error(f'No last price available for symbol {symbol}')
			return 0

	def oco_as_complex_order(self) -> bool:
		"""
		With Tastytrade, the OCO orders have to be placed as one complex order
		"""
		return True
	
	def uses_oco_orders(self) -> bool:
		""" 
		The TWS Connector uses OCO orders for take profit and stop loss orders
		"""
		return True
	
	async def unsubscribe_ticker_data(self):
		"""
		Unsubscribe from ticker data - including base symbols and all options
		"""
		await super().unsubscribe_ticker_data()
		
		# First, unsubscribe from all option symbols
		for symbolData in self._symbolData.values():
			try:
				for day_option_price_data in symbolData.optionPriceData.values():
					streamer_symbols = []
					for value in day_option_price_data.strikeData.values():
						option_price_data: OptionStrikePriceData = value
						
						try:
							call_streamer_symbol = option_price_data.brokerSpecific['call_streamer_symbol']
							streamer_symbols.append(call_streamer_symbol)
							self._quote_symbols.remove(call_streamer_symbol)
						except KeyError:
							pass

						try:
							put_streamer_symbol = option_price_data.brokerSpecific['put_streamer_symbol']
							streamer_symbols.append(put_streamer_symbol)
							self._quote_symbols.remove(put_streamer_symbol)
						except KeyError:
							pass

					if streamer_symbols:
						try:
							await self._streamer.unsubscribe(Quote, streamer_symbols)
							await self._streamer.unsubscribe(Greeks, streamer_symbols)
						except ConnectionClosedOK:
							logger.debug('Streamer already closed, ignore')
							pass
				symbolData.optionPriceData.clear()
				symbolData.lastAtmStrike = 0
				symbolData.lastPrice = 0
			except KeyError:
				pass
		
		# Now unsubscribe from base symbols (SPX, VIX, etc.)
		# This ensures a clean state for re-subscription at new day start
		if self._quote_symbols:
			logger.debug(f'Unsubscribing from {len(self._quote_symbols)} base quote symbols')
			await self._streamer.unsubscribe(Quote, self._quote_symbols)
		if self._greeks_symbols:
			logger.debug(f'Unsubscribing from {len(self._greeks_symbols)} base greeks symbols')
			await self._streamer.unsubscribe(Greeks, self._greeks_symbols)
		if self._candle_symbols:
			logger.debug(f'Unsubscribing from {len(self._candle_symbols)} base candle symbols')
			await self._streamer.unsubscribe(Candle, self._candle_symbols)

	async def _requestMissingOptionData(self, symbolData: TastySymbolData, atmStrike: float):
		"""
		Request option data for the given symbol and expiration date
		"""
		relevant_expirations = self._determine_relevant_expirations(symbolData)
		symbolInformation = symbolInfo.symbol_infos[symbolData.symbol]
		strikes_of_interest = self._determine_strikes_of_interest(symbolData, atmStrike)	
	
		for relevant_expiration in relevant_expirations:
			# Optain saved options data for the expiration date
			try:
				#expiration_date_str = relevant_expiration.strftime('%Y%m%d')
				optionStrikeData = symbolData.optionPriceData[relevant_expiration]
			except KeyError as keyErr:
				# Wenn noch keine Optionsdaten für das Verfallsdatum vorhanden sind, dann bei Tasty anfragen ob es Optionsdaten gibt

				optionStrikeData = OptionStrikeData()
				symbolData.optionPriceData[relevant_expiration] = optionStrikeData

			for chain_at_expiration in symbolData.chain.expirations:
				if chain_at_expiration.expiration_date >= relevant_expiration:
					break
			if chain_at_expiration == None or chain_at_expiration.expiration_date != relevant_expiration:
				logger.error(f'No options available for symbol {symbolData.tastySymbol} and expiration date {relevant_expiration}')
				continue
			
			# Convert the available strikes to a list of decimal numbers
			# if not done yet
			try:
				available_strikes = chain_at_expiration._optrabot_strikes
			except AttributeError as attrErr:
				chain_at_expiration._optrabot_strikes = []
				available_strikes = chain_at_expiration._optrabot_strikes
				for strike in chain_at_expiration.strikes:
					available_strikes.append(strike.strike_price)

			options_to_be_requested = []
			for strike_price in strikes_of_interest:	
				try:
					optionStrikeData.strikeData[strike_price]
				except KeyError as keyErr:
					option_strike_price_data = OptionStrikePriceData()
					optionStrikeData.strikeData[strike_price] = option_strike_price_data
					options_to_be_requested.append(strike_price)

			if len(options_to_be_requested) > 0:
				streamer_symbols = []
				for item in chain_at_expiration.strikes:
					strike: Strike = item
					if strike.strike_price in options_to_be_requested:
						option_strike_data = optionStrikeData.strikeData[strike.strike_price]
						option_strike_data.brokerSpecific['call_option'] = strike.call
						option_strike_data.brokerSpecific['call_streamer_symbol'] = strike.call_streamer_symbol
						option_strike_data.brokerSpecific['put_option'] =  strike.put
						option_strike_data.brokerSpecific['put_streamer_symbol']  = strike.put_streamer_symbol
						streamer_symbols.append(strike.call_streamer_symbol)
						streamer_symbols.append(strike.put_streamer_symbol)
						self._quote_symbols.append(strike.call_streamer_symbol)
						self._quote_symbols.append(strike.put_streamer_symbol)
				await self._streamer.subscribe(Quote, streamer_symbols)
				await self._streamer.subscribe(Greeks, streamer_symbols)
		
	def _getOptionInfos(self, tastySymbol: str) -> tuple:
		"""
		Extracts the generic symbol and expiration date, strike and option side from the tastytrade option symbol.
		If the option symbol information cannot be parsed as expected, a ValueError exception is raised.
		"""
		error = False
		pattern = r'^.(?P<optionsymbol>[A-Z]+)(?P<expiration>[0-9]+)(?P<type>[CP])(?P<strike>[0-9]+)'
		compiledPattern = re.compile(pattern)
		match = compiledPattern.match(tastySymbol)
		try:
			if match:
				optionSymbol = match.group('optionsymbol')
				for symbol, symbol_info in symbolInfo.symbol_infos.items():
					if symbol_info.symbol + symbol_info.option_symbol_suffix == optionSymbol:
						genericSymbol = symbol_info.symbol
						break
				expirationDate = dt.datetime.strptime(match.group('expiration'), '%y%m%d').date()
				strike = float(match.group('strike'))
				optionType = OptionType.CALL if match.group('type') == 'C' else OptionType.PUT
		except IndexError as indexErr:
			logger.error(f'Invalid option symbol {tastySymbol}')
			error = True
		except ValueError as valueErr:
			logger.error(f'Invalid option symbol {tastySymbol}')
			error = True
		if genericSymbol == None or error == True:
			raise ValueError(f'Invalid option symbol {tastySymbol}')
		return genericSymbol, optionType, expirationDate, strike
	
	def _mappedOrderAction(self, orderAction: GenericOrderAction, legAction: GenericOrderAction) -> OrderAction:
		"""
		Maps the general order action to the Tasty specific order action
		For Closing orders, the leg actions need to be inverted
		eg. BUY -> SELL_TO_CLOSE
		eg. SELL -> BUY_TO_CLOSE
		"""
		match orderAction:
			case GenericOrderAction.BUY_TO_OPEN:
				if legAction == GenericOrderAction.BUY:
					return OrderAction.BUY_TO_OPEN
				if legAction == GenericOrderAction.SELL:
					return OrderAction.SELL_TO_OPEN
				else:
					raise ValueError(f'Unknown leg action: {legAction}')
			case GenericOrderAction.SELL_TO_OPEN:
				if legAction == GenericOrderAction.SELL:
					return OrderAction.SELL_TO_OPEN
				elif legAction == GenericOrderAction.BUY:
					return OrderAction.BUY_TO_OPEN
				else:
					raise ValueError(f'Unknown leg action: {legAction}')
			case GenericOrderAction.BUY_TO_CLOSE:
				if legAction == GenericOrderAction.BUY:
					return OrderAction.BUY_TO_CLOSE
				if legAction == GenericOrderAction.SELL:
					return OrderAction.SELL_TO_CLOSE
				else:
					raise ValueError(f'Unknown leg action: {legAction}')
			case GenericOrderAction.SELL_TO_CLOSE:
				if legAction == GenericOrderAction.SELL:
					return OrderAction.SELL_TO_CLOSE
				elif legAction == GenericOrderAction.BUY:
					return OrderAction.BUY_TO_CLOSE
				else:
					raise ValueError(f'Unknown leg action for SELL_TO_CLOSE: {legAction}')
			case _:
				raise ValueError(f'Unknown order action: {orderAction}')
			
	async def _request_account_updates(self):
		"""
		Request Account Updates - runs as a background task.
		
		If the AlertStreamer encounters a fatal error (e.g., AUTH timeout),
		this method will attempt to reconnect automatically.
		"""
		task_id = id(asyncio.current_task())
		logger.debug(f'_request_account_updates started (task {task_id})')
		try:
			self._alert_streamer = await AlertStreamer(self._session, disconnect_fn=self._on_alert_streamer_disconnect)
			streamer_id = id(self._alert_streamer)
			logger.debug(f'Created alert streamer {streamer_id} (task {task_id})')
			await self._alert_streamer.subscribe_accounts(self._tasty_accounts)
			
			# Start the update loop directly without creating nested tasks
			logger.debug(f'Starting _update_accounts (task {task_id}, streamer {streamer_id})')
			await self._update_accounts()
		except asyncio.CancelledError:
			logger.debug(f'Cancelled listening to account updates (task {task_id})')
			raise  # Re-raise to allow proper task cancellation
		except Exception as exc:
			logger.error(f'Error in account updates (task {task_id}): {exc}')
			# OTB-264: Attempt to reconnect the AlertStreamer on fatal errors
			# (e.g., "The timeout for waiting for AUTH has been reached")
			await self._handle_alert_streamer_error(exc)
		finally:
			logger.debug(f'_request_account_updates exiting (task {task_id})')

	def _genericOrderStatus(self, status: OrderStatus) -> GenericOrderStatus:
		"""
		Maps the Tastytrade order status to the generic order status
		"""
		match status:
			case OrderStatus.RECEIVED:
				return GenericOrderStatus.OPEN
			case OrderStatus.LIVE:
				return GenericOrderStatus.OPEN
			case OrderStatus.CONTINGENT:
				return GenericOrderStatus.OPEN
			case OrderStatus.CANCELLED:
				return GenericOrderStatus.CANCELLED
			case OrderStatus.FILLED:
				return GenericOrderStatus.FILLED
			case OrderStatus.REJECTED:
				return GenericOrderStatus.CANCELLED
			case _:
				return None