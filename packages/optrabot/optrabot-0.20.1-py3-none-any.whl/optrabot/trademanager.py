import asyncio
import copy
import json
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import SchedulerNotRunningError
from loguru import logger
from sqlalchemy.orm import Session

import optrabot.symbolinfo as symbolInfo
from optrabot import crud, schemas
from optrabot.broker.brokerconnector import BrokerConnector
from optrabot.broker.brokerfactory import BrokerFactory
from optrabot.broker.order import (Execution, Leg, OptionRight, Order,
                                   OrderAction, OrderStatus, OrderType,
                                   PriceEffect)
from optrabot.database import get_db_engine
from optrabot.exceptions.orderexceptions import (PlaceOrderException,
                                                 PrepareOrderException)
from optrabot.flowengine.flowevent import FlowEventType
from optrabot.managedtrade import ManagedTrade
from optrabot.models import Trade
from optrabot.optionhelper import OptionHelper
from optrabot.stoplossadjuster import StopLossAdjuster
from optrabot.tradehelper import SecurityStatusData, TradeHelper
from optrabot.tradestatus import TradeStatus
from optrabot.tradetemplate.earlyexittrigger import EarlyExitTriggerType
from optrabot.tradetemplate.templatefactory import Template
from optrabot.util.singletonmeta import SingletonMeta


@dataclass
class ContractUsageData:
    trade_id: int
    account: str
    contracts: int

class TradeManager(metaclass=SingletonMeta):
	"""
	The Trade Manager is a singleton class which is responsible for opening new trades and
	managing existing trades. It is monitoring the open trades and their attached orders.
	"""
	def __init__(self) -> None:
		self._trades: List[ManagedTrade] = []
		self._backgroundScheduler = AsyncIOScheduler()
		self._backgroundScheduler.start()
		# Start monitoring of open trades in next 5 seconds mark
		now = datetime.now()
		next_run_time = (now + timedelta(seconds=(5 - now.second % 5))).replace(microsecond=0)
		self._backgroundScheduler.add_job(self._monitorOpenTrades, 'interval', seconds=5, id='MonitorOpenTrades', misfire_grace_time = None, next_run_time=next_run_time)
		self._backgroundScheduler.add_job(self._performEODTasks, 'cron', hour=16, minute=0, timezone=pytz.timezone('US/Eastern'), id='EODTasks', misfire_grace_time = None)
		self._backgroundScheduler.add_job(self._performEODSettlement, 'cron', hour=16, minute=34, timezone=pytz.timezone('US/Eastern'), id='EODSettlement', misfire_grace_time = None)
		self._backgroundScheduler.add_job(self._report_excuted_trades, 'interval', seconds=30, id='ReportExecutedTrades', misfire_grace_time = None)
		BrokerFactory().orderStatusEvent += self._onOrderStatusChanged
		BrokerFactory().commissionReportEvent += self._onCommissionReportEvent
		BrokerFactory().orderExecutionDetailsEvent += self._onOrderExecutionDetailsEvent
		self._lock = asyncio.Lock()
		self._execution_transaction_map = {} # Maps the Execution ID to the Transaction ID
		self._last_trade_monitoring_time = datetime.now()	# Timestamp of last Trade monitoring
		self._undelivered_contracts: Dict[int, ContractUsageData] = {}  # Maps trade id to number of filled contracts to be reported to the OptraBot Hub
		self._lock_upload_usage = asyncio.Lock()	# Lock for uploading contracts usage

	async def shutdown(self) -> None:
		"""
		Shutdown the TradeManager. Cancels pending entry orders and stops the background scheduler.
		"""
		logger.debug('Shutting down TradeManager')
		
		# Cancel pending entry orders before shutdown
		await self._cancel_pending_entry_orders()
		
		try:
			self._backgroundScheduler.remove_all_jobs()
		except (SchedulerNotRunningError, AttributeError) as e:
			logger.debug(f'TradeManager scheduler jobs already cleared or not running: {e}')
		except Exception as e:
			logger.warning(f'Error removing jobs from TradeManager scheduler: {e}')
				
		# Fahre den Scheduler herunter, falls er läuft
		try:
			if  self._backgroundScheduler.running:
				self._backgroundScheduler.shutdown()
				logger.debug('TradeManager scheduler shutdown completed')
			else:
				logger.debug('TradeManager scheduler was not running')
		except SchedulerNotRunningError:
			logger.debug('TradeManager scheduler already stopped')
		except Exception as e:
			logger.warning(f'Error shutting down TradeManager scheduler: {e}')

	async def _cancel_pending_entry_orders(self) -> None:
		"""
		Cancels all pending entry orders for trades that have not been filled yet.
		Called during shutdown to ensure no orphaned orders remain at the broker.
		Waits up to 5 seconds for each cancellation to be confirmed.
		"""
		cancelled_orders = []  # List of (account, template_name) tuples for notification
		
		for managed_trade in self._trades:
			# Check if trade is NEW (entry order not filled) and entry order is still open
			if managed_trade.status == TradeStatus.NEW:
				if managed_trade.entryOrder and managed_trade.entryOrder.status == OrderStatus.OPEN:
					try:
						broker_connector = BrokerFactory().getBrokerConnectorByAccount(managed_trade.template.account)
						if broker_connector and broker_connector.isConnected():
							logger.info(f'Cancelling pending entry order for trade {managed_trade.trade.id} ({managed_trade.template.name}) during shutdown')
							await broker_connector.cancel_order(managed_trade.entryOrder)
							
							# Wait up to 5 seconds for cancellation confirmation
							timeout = 5.0
							start_time = time.time()
							while managed_trade.entryOrder.status != OrderStatus.CANCELLED:
								if time.time() - start_time > timeout:
									logger.warning(f'Timeout waiting for cancellation confirmation for trade {managed_trade.trade.id}')
									break
								await asyncio.sleep(0.1)
							
							if managed_trade.entryOrder.status == OrderStatus.CANCELLED:
								logger.info(f'Entry order for trade {managed_trade.trade.id} successfully cancelled')
								cancelled_orders.append((managed_trade.template.account, managed_trade.template.name))
							else:
								# Still add to list for notification even if timeout
								cancelled_orders.append((managed_trade.template.account, managed_trade.template.name))
					except Exception as e:
						logger.warning(f'Failed to cancel entry order for trade {managed_trade.trade.id}: {e}')
		
		# Send notification if orders were cancelled
		if cancelled_orders:
			from optrabot.tradinghubclient import NotificationType, TradinghubClient
			try:
				# Build notification message with account and template details
				details = '\n'.join([f'Template {template} in Account {account} at Broker {broker_connector.broker}' for account, template in cancelled_orders])
				await TradinghubClient().send_notification(
					NotificationType.WARN,
					f'📣 OptraBot Shutdown: {len(cancelled_orders)} pending entry order(s) were cancelled:\n{details}'
				)
			except Exception as e:
				logger.warning(f'Failed to send shutdown cancellation notification: {e}')

	async def openTrade(self, entryOrder: Order, template: Template):
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(template.account)
		if brokerConnector == None:
			error_msg = f'No active broker connection found for account {template.account}'
			logger.error(f'{error_msg}. Unable to place entry order.')
			raise ValueError(error_msg)
		
		if brokerConnector.isConnected() == False:
			error_msg = f'Broker connection for account {template.account} is not connected'
			logger.error(f'{error_msg}. Unable to place entry order.')
			raise ValueError(error_msg)
		
		if template.maxOpenTrades > 0:
			openTrades = 0
			for managedTrade in self._trades:
				if managedTrade.template == template and managedTrade.status == TradeStatus.OPEN:
					openTrades += 1
			if openTrades >= template.maxOpenTrades:
				error_msg = f'Maximum number of open trades ({template.maxOpenTrades}) for template {template.name} reached'
				logger.warning(f'{error_msg}. Unable to place new trade.')
				raise ValueError(error_msg)

		if brokerConnector.isTradingEnabled() == False:
			error_msg = f'Trading is disabled for account {template.account}'
			logger.error(f'{error_msg}. Unable to place entry order.')
			raise ValueError(error_msg)
		
		try:
			await brokerConnector.prepareOrder(entryOrder)
			self._circuit_breaker_check(entryOrder)

		except PrepareOrderException as e:
			logger.error(f'Failed to prepare entry order for account {template.account}. Reason: {e.reason}')

			# Send Telegram-Notificiation via OptraBot Server
			from optrabot.tradinghubclient import NotificationType, TradinghubClient
			try:
				await TradinghubClient().send_notification(
					NotificationType.ERROR, 
					f"❌ Failed to prepare entry order for trade {template.strategy}.\n*Reason:* {e.reason}\n*Strikes:* {self._strikes_from_order(entryOrder)}\n*Account:* {template.account}"
				)
			except Exception as notify_error:
				logger.error(f"Unable to send telegram notification: {notify_error}")
			return
		
		logger.info(f'Opening trade at strikes {self._strikes_from_order(entryOrder)}')

		# Midprice calculation and premium checks
		entryOrder.price = self._calculateMidPrice(brokerConnector, entryOrder)
		logger.info(f'Calculated midprice for entry order: {entryOrder.price}')
		if template.meetsMinimumPremium(entryOrder.price) == False:
			logger.error(f'Entry order for account {template.account} does not meet minimum premium requirement. Unable to place entry order')
			return
		if template.meets_maximum_premium(entryOrder.price) == False:
			logger.error(f'Entry order for account {template.account} exceeds maximum premium requirement. Unable to place entry order')
			return

		# Create the Trade in the database
		async with self._lock: # Mit Lock arbeiten, damit die Trade IDs nicht doppelt vergeben werden
			with Session(get_db_engine()) as session:
				newTradeSchema = schemas.TradeCreate(
					account=template.account, 
					symbol=entryOrder.symbol, 
					strategy=template.strategy,
					template_name=template.name  # OTB-253: Store template name for recovery
				)
				newTrade = crud.create_trade(session, newTradeSchema)
				
				# Set trade_group_id if provided by template (e.g., from Flow Engine rollover)
				if hasattr(template, 'trade_group_id') and template.trade_group_id:
					newTrade.trade_group_id = template.trade_group_id
					logger.info(f'Trade {newTrade.id} assigned to Trade Group: {template.trade_group_id}')
				else:
					# Generate new trade_group_id for standalone trades
					newTrade.trade_group_id = self._generate_trade_group_id(session)
					logger.debug(f'Trade {newTrade.id} assigned new Trade Group: {newTrade.trade_group_id}')
				
				session.commit()
				# Load all relationships before session closes to prevent lazy-load errors
				session.refresh(newTrade)
				# Access transactions to force loading
				_ = newTrade.transactions
				# Make newTrade usable outside the session
				session.expunge(newTrade)
			
			newManagedTrade = ManagedTrade(trade=newTrade, entryOrder=entryOrder, template=template, account=template.account)
			self._trades.append(newManagedTrade)
		entryOrder.orderReference = self._composeOrderReference(newManagedTrade, 'Open')
		try:
			await brokerConnector.placeOrder(newManagedTrade, entryOrder)
			entryOrderPlaced = True
		except PlaceOrderException as e:
			logger.error(f"Failed to place entry order: {e.reason}")
			
			# Send Telegram-Notificiation via OptraBot Server
			from optrabot.tradinghubclient import NotificationType, TradinghubClient
			try:
				await TradinghubClient().send_notification(
					NotificationType.ERROR, 
					f"❌ Failed to place entry order for trade {template.strategy}.\n*Reason:* {e.reason}\n*Strikes:* {self._strikes_from_order(entryOrder)}\n*Account:* {template.account}\n*Price:* ${entryOrder.price:.2f}\n*Quantity:* {entryOrder.quantity}"
				)
			except Exception as notify_error:
				logger.error(f"Unable to send telegram notification: {notify_error}")
			
			# Trade aus der Datenbank löschen, da die Order nicht platziert werden konnte
			await self._deleteTrade(newManagedTrade, "order placement failed")
			entryOrderPlaced = False

		if entryOrderPlaced:
			logger.debug(f'Entry order for account placed. Now track its execution')
			entryOrder.status = OrderStatus.OPEN
			#asyncio.create_task(self._trackEntryOrder(newManagedTrade), name='TrackEntryOrder' + str(newManagedTrade.trade.id))
			self._backgroundScheduler.add_job(self._trackEntryOrder, 'interval', seconds=5, id='TrackEntryOrder' + str(newManagedTrade.trade.id), args=[newManagedTrade], max_instances=1, misfire_grace_time=None)

	def _onCommissionReportEvent(self, order: Order, execution_id: str, commission: float, fee: float):
		"""
		Handles the commission and fee reporting event from the Broker Connector.
		It adds the commission and fee to the transaction in the database.
		"""
		# Determine the transaction based on the execution ID
		try:
			transaction_id = self._execution_transaction_map.get(execution_id)
		except KeyError:
			logger.error(f'No trade transaction found for fill execution id {execution_id}')
			return
		
		for managed_trade in self._trades:
			if order == managed_trade.entryOrder or order == managed_trade.takeProfitOrder or order == managed_trade.stopLossOrder or order == managed_trade.closing_order:
				logger.debug(f'Trade {managed_trade.trade.id}: Commission Report for Order received. Commission: {commission} Fee: {fee}')
				with Session(get_db_engine()) as session:
					db_trade = crud.getTrade(session, managed_trade.trade.id)
					transaction = crud.getTransactionById(session, managed_trade.trade.id, transaction_id)
					if transaction == None:
						logger.error('Transaction with id {} for trade {} not found in database!', transaction_id, managed_trade.trade.id)
						return
					for managed_transaction in managed_trade.transactions:
						if managed_transaction.id == transaction.id:
							managed_transaction.commission += commission
							managed_transaction.fee += fee
							break
					transaction.commission += commission
					transaction.fee += fee
					TradeHelper.updateTrade(db_trade, session)
					session.commit()
					logger.debug(f'Commissions saved to transaction {transaction.id} for trade {managed_trade.trade.id}')
				break

	def _onOrderExecutionDetailsEvent(self, order: Order, execution: Execution):
		"""
		Handles the order execution details which are sent from the Broker Connector
		when a order has been executed.
		"""
		logger.debug(f'Trade Manager Order Execution Details:')
		for managed_trade in self._trades:
			if order not in [managed_trade.entryOrder, managed_trade.takeProfitOrder, managed_trade.stopLossOrder, managed_trade.closing_order]:
				continue
			with Session(get_db_engine()) as session:
				existing_transaction = crud.get_transaction_by_execution_id(session, managed_trade.trade.id, execution.id)
				if existing_transaction:
					logger.debug(f'Trade {managed_trade.trade.id}: Execution with id {execution.id} has already been processed. Skipping.')
					continue				
				max_transaction_id = crud.getMaxTransactionId(session, managed_trade.trade.id)
				db_trade = crud.getTrade(session, managed_trade.trade.id)
				if max_transaction_id == 0:
					# Opening transaction of the trade
					db_trade.status = TradeStatus.OPEN
				elif order == managed_trade.takeProfitOrder or order == managed_trade.stopLossOrder or order == managed_trade.closing_order:
					# Set status to closed if take profit or stop loss order is filled, in order to prevent them to be reestablished
					# by the monitorOpenTrades background job.
					managed_trade.status = TradeStatus.CLOSED
				max_transaction_id += 1
				new_transaction = schemas.TransactionCreate(tradeid=managed_trade.trade.id, transactionid=max_transaction_id,
															id=max_transaction_id,
															symbol=order.symbol,
															type=execution.action,
															sectype=execution.sec_type,
															contracts=execution.amount,
															price=execution.price, 
															expiration=execution.expiration,
															strike=execution.strike,
															fee=0,
															commission=0,
															notes='',
															exec_id=str(execution.id),
															timestamp=execution.timestamp)
				self._execution_transaction_map[execution.id] = new_transaction.id # Memorize the the Execution ID for later commission report
				crud.createTransaction(session, new_transaction)
				managed_trade.transactions.append(new_transaction)

				# Check if trade is closed with all these transactions
				TradeHelper.updateTrade(db_trade, session)
				session.commit()
				if order == managed_trade.entryOrder:
					# Collect the trade execution report in background
					self._backgroundScheduler.add_job(self._keep_contract_usage, id='KeepContractUsage' + str(managed_trade.trade.id) + '-' + execution.id, args=[managed_trade.trade.id, managed_trade.template.account, execution.amount], misfire_grace_time = None)

	async def _onOrderStatusChanged(self, order: Order, status: OrderStatus, filledAmount: int = 0):
		"""
		Handles the status change event of an order
		"""
		from optrabot.tradinghubclient import NotificationType, TradinghubClient
		logger.debug(f'Trade Manager Order status changed: {order.symbol} - {status}')
		for managedTrade in self._trades:
			brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
			if managedTrade.entryOrder == order:
				if status == OrderStatus.CANCELLED and managedTrade.status != TradeStatus.OPEN:
					managedTrade.entryOrder.status = OrderStatus.CANCELLED
					logger.debug(f'Entry order for trade {managedTrade.trade.id} was cancelled')
					
					try:
						job_id = 'TrackEntryOrder' + str(managedTrade.trade.id)
						if self._backgroundScheduler.get_job(job_id):
							logger.debug(f"Removing tracking job for trade {managedTrade.trade.id}")
							self._backgroundScheduler.remove_job(job_id)
					except Exception as e:
						logger.debug(f"No tracking job found for trade {managedTrade.trade.id} or error removing job: {e}")
					
					await self._deleteTrade(managedTrade, "entry order was cancelled")
				if status == OrderStatus.FILLED:
					managedTrade.entryOrder.status = OrderStatus.FILLED
					logger.info(f'Entry Order of trade {managedTrade.trade.id} has been filled at ${managedTrade.entryOrder.averageFillPrice:.2f} (Qty: {filledAmount}) and trade is now running.' )
					if managedTrade.status != TradeStatus.OPEN:
						managedTrade.status = TradeStatus.OPEN
						managedTrade.current_legs = managedTrade.entryOrder.legs
						
						# Set openDate when trade is first opened
						import datetime

						import pytz
						open_date = datetime.datetime.now(pytz.UTC)
						
						# Update trade in database by reloading it in a new session
						with Session(get_db_engine()) as session:
							trade = crud.getTrade(session, managedTrade.trade.id)
							trade.status = TradeStatus.OPEN
							trade.openDate = open_date
							session.commit()
						
						# Update the in-memory trade object
						managedTrade.trade.status = TradeStatus.OPEN
						managedTrade.trade.openDate = open_date

						logger.debug('Create TP SL Order Job')
						self._backgroundScheduler.add_job(self._createTakeProfitAndStop, id='CreateTakeProfitAndStop' + str(managedTrade.trade.id), args=[managedTrade], misfire_grace_time = None)

						# Extract expiration from first leg for notification and flow event
						trade_expiration = None
						if managedTrade.entryOrder and managedTrade.entryOrder.legs:
							trade_expiration = managedTrade.entryOrder.legs[0].expiration
						
						# Build expiration line for notification
						expiration_line = f'\n*Expiration:* {trade_expiration.strftime("%Y-%m-%d")}' if trade_expiration else ''

						# Send Telegram Notification via OptraBot Server
						await TradinghubClient().send_notification(NotificationType.INFO, f'🚀 Trade {managedTrade.trade.id} opened at {brokerConnector.broker}.\n*Strategy:* {managedTrade.template.strategy}\n*Strikes:* {self._strikes_from_order(managedTrade.entryOrder)}{expiration_line}\n*Account:* {managedTrade.account}\n*Price:* ${managedTrade.entryOrder.averageFillPrice:.2f}\n*Quantity:* {filledAmount}')

						try:
							from optrabot.flowengine import FlowEngine
							from optrabot.flowengine.flowevent import TradeOpenedEventData

							event_data = TradeOpenedEventData(
						        event_type=FlowEventType.TRADE_OPENED,
						        trade_id=managedTrade.trade.id,
						        trade_amount=managedTrade.template.amount,
						        trade_symbol=managedTrade.trade.symbol,
						        trade_strategy=managedTrade.template.strategy,
						        template_name=managedTrade.template.name,
						        trade_entry_price=managedTrade.entryOrder.averageFillPrice,
						        trade_expiration=trade_expiration,
						        trade_group_id=managedTrade.trade.trade_group_id)
							FlowEngine().emit_event(event_data)
							logger.debug(f'Emitted trade_opened flow event for trade {managedTrade.trade.id}')
						except Exception as e:
							logger.error(f'Error emitting trade_opened flow event for trade {managedTrade.trade.id}: {e}')
					else:
						logger.debug('Trade is already open. No need to create TP SL Order Job')
			elif managedTrade.takeProfitOrder == order:
				if status == OrderStatus.FILLED:
					managedTrade.takeProfitOrder.status = OrderStatus.FILLED
					logger.debug(f'Take Profit order for trade {managedTrade.trade.id} was filled. Closing trade now')
					
					# Guard against duplicate FILLED events from IBKR (one per leg fill)
					# Check if trade was already closed by execution details event
					# If so, skip _close_trade() but still send notifications
					if managedTrade.status != TradeStatus.CLOSED:
						self._close_trade(managedTrade)
					else:
						logger.debug(f'Trade {managedTrade.trade.id} already closed by execution details, skipping _close_trade()')
					
					logger.success('Take Profit Order has been filled. Trade with id {} finished', managedTrade.trade.id)
					await TradinghubClient().send_notification(NotificationType.INFO, f'🎯 Trade {managedTrade.trade.id}\n*Take Profit* order executed at ${order.averageFillPrice:.2f}.') 
					
					# Emit take_profit_hit flow event with delay for transaction processing
					await self._emit_trade_exit_event_delayed(managedTrade, FlowEventType.TAKE_PROFIT_HIT)
				elif status == OrderStatus.CANCELLED:
					managedTrade.takeProfitOrder.status = OrderStatus.CANCELLED
					logger.debug(f'Take Profit order for trade {managedTrade.trade.id} was cancelled.')
				if status == OrderStatus.FILLED or status == OrderStatus.CANCELLED:
					if not brokerConnector.uses_oco_orders() and managedTrade.stopLossOrder:
						logger.info(f'Trade {managedTrade.trade.id} does not use OCO orders. Cancelling Stop Loss order')
						await brokerConnector.cancel_order(managedTrade.stopLossOrder)

			elif managedTrade.stopLossOrder == order:
				if status == OrderStatus.FILLED:
					managedTrade.stopLossOrder.status = OrderStatus.FILLED
					logger.debug(f'Stop Loss order for trade {managedTrade.trade.id} was filled. Closing trade now')
					
					# Guard against duplicate FILLED events from IBKR (one per leg fill)
					# Check if trade was already closed by execution details event
					# If so, skip _close_trade() but still send notifications
					if managedTrade.status != TradeStatus.CLOSED:
						self._close_trade(managedTrade)
					else:
						logger.debug(f'Trade {managedTrade.trade.id} already closed by execution details, skipping _close_trade()')
					
					logger.error('Stop Loss Order has been filled. Trade with id {} finished', managedTrade.trade.id)
					await TradinghubClient().send_notification(NotificationType.INFO, f'🏁 Trade {managedTrade.trade.id}\n*Stop Loss* order executed at ${order.averageFillPrice:.2f}.') 
					
					# Emit stop_loss_hit flow event with delay for transaction processing
					await self._emit_trade_exit_event_delayed(managedTrade, FlowEventType.STOP_LOSS_HIT)
				elif status == OrderStatus.CANCELLED:
					managedTrade.stopLossOrder.status = OrderStatus.CANCELLED
					logger.debug(f'Stop Loss order for trade {managedTrade.trade.id} was cancelled')
				if status == OrderStatus.FILLED or status == OrderStatus.CANCELLED:
					if not brokerConnector.uses_oco_orders() and managedTrade.takeProfitOrder:
						logger.info(f'Trade {managedTrade.trade.id} does not use OCO orders. Cancelling Take Profit order')
						await brokerConnector.cancel_order(managedTrade.takeProfitOrder)
			elif managedTrade.closing_order == order:
				logger.debug(f'Closing order status update for trade {managedTrade.trade.id}: {status}')
				if status == OrderStatus.FILLED:
					# Guard against duplicate FILLED events (Tastytrade sends one per leg)
					# Only process the FIRST FILLED event for this closing order
					if managedTrade.closing_order.status == OrderStatus.FILLED:
						logger.debug(f'Closing order for trade {managedTrade.trade.id} already processed, ignoring duplicate FILLED event')
						return
					
					managedTrade.closing_order.status = OrderStatus.FILLED
					logger.debug(f'Closing order for trade {managedTrade.trade.id} was filled. Closing trade now')
					
					# Create $0 transactions for legs that were excluded from closing order (no bid price)
					if managedTrade.excluded_closing_legs:
						await self._create_zero_price_closing_transactions(managedTrade, managedTrade.excluded_closing_legs)
						managedTrade.excluded_closing_legs = []  # Clear after processing
					
					# Check if trade was already closed by execution details event
					# If so, skip _close_trade() but still send notifications
					if managedTrade.status != TradeStatus.CLOSED:
						self._close_trade(managedTrade)
					else:
						logger.debug(f'Trade {managedTrade.trade.id} already closed by execution details, skipping _close_trade()')
					
					logger.success(f'Closing Order has been filled at ${order.averageFillPrice:.2f}. Trade with id {managedTrade.trade.id} finished')
					await TradinghubClient().send_notification(NotificationType.INFO, f'🏁 Trade {managedTrade.trade.id}\n*Closing* order executed at ${order.averageFillPrice:.2f}.')
					
					# Emit flow event based on whether this was a manual close
					# Check for manual close flag (set by close_trade_manually)
					is_manual_close = getattr(managedTrade, '_manual_close_trigger_flow', None) is not None
					if is_manual_close:
						# Manual close - check if flow events should be triggered
						if managedTrade._manual_close_trigger_flow:
							await asyncio.sleep(1)  # Wait for transaction processing
							self._emit_manual_close_event(managedTrade)
						else:
							logger.info(f'Manual close for trade {managedTrade.trade.id} - flow events suppressed')
						# Clean up the flag
						delattr(managedTrade, '_manual_close_trigger_flow')
					else:
						# Normal early exit - emit EARLY_EXIT event with delay for transaction processing
						await self._emit_trade_exit_event_delayed(managedTrade, FlowEventType.EARLY_EXIT)
					
					# Stop tracking the closing order
					try:
						job_id = 'TrackClosingOrder' + str(managedTrade.trade.id)
						if self._backgroundScheduler.get_job(job_id):
							logger.debug(f"Removing closing order tracking job for trade {managedTrade.trade.id}")
							self._backgroundScheduler.remove_job(job_id)
					except Exception as e:
						logger.error(f"Error removing closing order tracking job: {e}")
				elif status == OrderStatus.CANCELLED:
					managedTrade.closing_order.status = OrderStatus.CANCELLED
					logger.debug(f'Closing order for trade {managedTrade.trade.id} was cancelled')

					# Stop Tracking the closing order
					try:
						job_id = 'TrackClosingOrder' + str(managedTrade.trade.id)
						if self._backgroundScheduler.get_job(job_id):
							logger.debug(f"Removing closing order tracking job for trade {managedTrade.trade.id}")
							self._backgroundScheduler.remove_job(job_id)
					except Exception as e:
						logger.debug(f"No closing order tracking job found for trade {managedTrade.trade.id} or error removing job: {e}")
					
					# Reset closing order so a new one can be created
					managedTrade.closing_order = None
					managedTrade.excluded_closing_legs = []
			else:
				# Try to find a matching adjustment order and update its status
				adjustment_order = next((ord for ord in managedTrade.adjustment_orders if ord == order), None)
				if adjustment_order:
					logger.debug(f'Found matching adjustment order for trade {managedTrade.trade.id}')
					adjustment_order.status = status

	def getManagedTrades(self) -> List[ManagedTrade]:
		"""
		Returns a list of all trades currenty managed by the TradeManager 
		"""
		return self._trades
	
	def _calculate_trade_premium(self, managed_trade: ManagedTrade) -> float:
		"""
		Calculate the premium (entry price) for a trade including fees.
		
		Args:
			managed_trade: The managed trade
			
		Returns:
			float: The trade premium with fees (positive value for received premium)
		"""
		if not managed_trade.entryOrder:
			return 0.0
		
		# Get symbol info for multiplier
		symbol_info = symbolInfo.symbol_infos[managed_trade.entryOrder.symbol]
		multiplier = symbol_info.multiplier
		
		# Get base premium from entry order
		premium = managed_trade.entryOrder.averageFillPrice or 0.0
		
		# Apply multiplier and make positive (premium received)
		premium = abs(premium) * multiplier * managed_trade.template.amount
		
		# Subtract fees (fees reduce the received premium)
		if hasattr(managed_trade.entryOrder, 'fees') and managed_trade.entryOrder.fees:
			premium -= managed_trade.entryOrder.fees
			
		return premium
	
	def _calculate_trade_net_result(self, managed_trade: ManagedTrade) -> float:
		"""
		Calculate the net result (profit/loss) for a trade based on all transactions.
		
		This calculates the P&L by summing all transaction values:
		- SELL transactions add to the result (premium received)
		- BUY transactions subtract from the result (cost to close)
		- All fees and commissions are subtracted
		
		Args:
			managed_trade: The managed trade
			
		Returns:
			float: The net result (positive for profit, negative for loss)
		"""
		# Get symbol info for multiplier
		symbol_info = symbolInfo.symbol_infos[managed_trade.entryOrder.symbol]
		multiplier = symbol_info.multiplier
		
		net_result = 0.0
		
		# Calculate P&L from all transactions
		for transaction in managed_trade.transactions:
			# Transaction value = price * contracts * multiplier
			transaction_value = transaction.price * transaction.contracts * multiplier
			
			# SELL transactions are positive (received premium), BUY transactions are negative (cost)
			if transaction.type == OrderAction.SELL:
				net_result += transaction_value
			else:  # BUY or other types
				net_result -= transaction_value
			
			# Subtract fees and commissions
			net_result -= (transaction.commission + transaction.fee)
		
		return net_result
	
	def _calculate_trade_fees(self, managed_trade: ManagedTrade) -> float:
		"""
		Calculate the total fees and commissions for a trade.
		
		Args:
			managed_trade: The managed trade
			
		Returns:
			float: The total fees and commissions
		"""
		total_fees = 0.0
		
		# Sum all fees and commissions from transactions
		for transaction in managed_trade.transactions:
			total_fees += (transaction.commission + transaction.fee)
		
		return total_fees
	
	async def _emit_trade_exit_event_delayed(self, managed_trade: ManagedTrade, event_type: FlowEventType) -> None:
		"""
		Emit a trade exit flow event with a delay to allow transaction processing.
		
		This method waits briefly for execution details and commission reports to be
		processed before emitting the flow event, ensuring all transaction data is available.
		
		Args:
			managed_trade: The managed trade that exited
			event_type: Type of exit event (FlowEventType enum)
		"""
		# Wait briefly for execution details and commission reports to be processed
		await asyncio.sleep(1)
		
		# Emit the flow event
		self._emit_trade_exit_event(managed_trade, event_type)
	
	def _emit_trade_exit_event(self, managed_trade: ManagedTrade, event_type: FlowEventType) -> None:
		"""
		Emit a flow event when a trade exits (early_exit, stop_loss_hit, or take_profit_hit)
		
		Args:
			managed_trade: The managed trade that exited
			event_type: Type of exit event (FlowEventType enum)
		"""
		try:
			from optrabot.flowengine import FlowEngine
			from optrabot.flowengine.flowevent import StopLossHitEventData  # noqa: E101
			from optrabot.flowengine.flowevent import \
			    TakeProfitHitEventData  # noqa: E101
			from optrabot.flowengine.flowevent import EarlyExitEventData

			# Calculate premium and net result
			trade_premium = self._calculate_trade_premium(managed_trade)
			net_result = round(self._calculate_trade_net_result(managed_trade), 2)
			logger.debug(f'Calculated net result for trade {managed_trade.trade.id}: {net_result}')
			trade_fees = round(self._calculate_trade_fees(managed_trade), 2)
			logger.debug(f'Calculated total fees for trade {managed_trade.trade.id}: {trade_fees}')
			
			# Determine exit price (always positive)
			if managed_trade.closing_order:
				exit_price = abs(managed_trade.closing_order.averageFillPrice or 0.0)
			elif managed_trade.stopLossOrder and managed_trade.stopLossOrder.status == OrderStatus.FILLED:
				exit_price = abs(managed_trade.stopLossOrder.averageFillPrice or 0.0)
			elif managed_trade.takeProfitOrder and managed_trade.takeProfitOrder.status == OrderStatus.FILLED:
				exit_price = abs(managed_trade.takeProfitOrder.averageFillPrice or 0.0)
			else:
				exit_price = 0.0
			
			# Extract expiration from first leg
			trade_expiration = None
			if managed_trade.entryOrder and managed_trade.entryOrder.legs:
				trade_expiration = managed_trade.entryOrder.legs[0].expiration
			
			# Create appropriate event data based on event type
			if event_type == FlowEventType.EARLY_EXIT:
				event_data = EarlyExitEventData(
					event_type=event_type,
					trade_id=managed_trade.trade.id,
					trade_amount=managed_trade.entryOrder.quantity,
					trade_symbol=managed_trade.trade.symbol,
					trade_strategy=managed_trade.template.strategy,
					template_name=managed_trade.template.name,
					trade_expiration=trade_expiration,
					trade_group_id=managed_trade.trade.trade_group_id,
					trade_entry_price=managed_trade.entry_price,
					trade_exit_price=exit_price,
					trade_net_result=net_result,
					trade_premium=trade_premium,
					trade_fees=trade_fees
				)
			elif event_type == FlowEventType.STOP_LOSS_HIT:
				event_data = StopLossHitEventData(
					event_type=event_type,
					trade_id=managed_trade.trade.id,
					trade_amount=managed_trade.template.amount,
					trade_symbol=managed_trade.trade.symbol,
					trade_strategy=managed_trade.template.strategy,
					template_name=managed_trade.template.name,
					trade_expiration=trade_expiration,
					trade_group_id=managed_trade.trade.trade_group_id,
					trade_entry_price=managed_trade.entry_price,
					trade_exit_price=exit_price,
					trade_net_result=net_result,
					trade_premium=trade_premium,
					trade_fees=trade_fees
				)
			elif event_type == FlowEventType.TAKE_PROFIT_HIT:
				event_data = TakeProfitHitEventData(
					event_type=event_type,
					trade_id=managed_trade.trade.id,
					trade_amount=managed_trade.template.amount,
					trade_symbol=managed_trade.trade.symbol,
					trade_strategy=managed_trade.template.strategy,
					template_name=managed_trade.template.name,
					trade_expiration=trade_expiration,
					trade_group_id=managed_trade.trade.trade_group_id,
					trade_entry_price=managed_trade.entry_price,
					trade_exit_price=exit_price,
					trade_net_result=net_result,
					trade_premium=trade_premium,
					trade_fees=trade_fees
				)
			else:
				logger.error(f'Unknown event type: {event_type}')
				return
			
			# Emit the event
			FlowEngine().emit_event(event_data)
			logger.debug(f'Emitted {event_type} flow event for trade {managed_trade.trade.id}')
			
		except Exception as e:
			logger.error(f'Error emitting flow event for trade {managed_trade.trade.id}: {e}')
	
	def _calculateMidPrice(self, broker_connector: BrokerConnector, order: Order) -> float:
		"""
		Calculates the midprice for the given order
		"""
		midPrice = 0
		for leg in order.legs:
			ask_price = leg.askPrice if leg.askPrice is not None and not OptionHelper.isNan(leg.askPrice) and leg.askPrice >= 0 else 0
			bid_price = leg.bidPrice if leg.bidPrice is not None and not OptionHelper.isNan(leg.bidPrice) and leg.bidPrice >= 0 else 0
			legMidPrice = (ask_price + bid_price) / 2
			if leg.action == OrderAction.SELL:
				midPrice -= legMidPrice
			else:
				midPrice += legMidPrice
		return self._round_order_price(broker_connector, order, midPrice)
	
	async def _keep_contract_usage(self, trade_id: int, account: str, filled_amount: int) -> None:
		""" 
		Keep the information about trade execution (fill) for further processing by the regular job which
		delivers the data to the OptraBot Hub
		"""
		async with self._lock_upload_usage:
			if trade_id in self._undelivered_contracts:
				data = self._undelivered_contracts[trade_id]
				data.contracts += filled_amount
			else:
				self._undelivered_contracts[trade_id] = ContractUsageData(
					trade_id=trade_id,
					account=account,
					contracts=filled_amount
				)

	async def _process_adjustment_orders(self, managed_trade: ManagedTrade):
		"""
		This Background Job function takes care of execution of the adjustment orders
		"""
		logger.debug(f'Start processing of adjustment orders for trade {managed_trade.trade.id}')
		broker_connector = BrokerFactory().getBrokerConnectorByAccount(managed_trade.template.account)
		oco_cancelled = False
		# Cancel existing Take Profit and Stop Loss Orders for the trade
		if managed_trade.takeProfitOrder and managed_trade.takeProfitOrder.status == OrderStatus.OPEN:
			logger.info(f'Cancelling existing Take Profit order for trade {managed_trade.trade.id} before placing adjustment orders')
			await broker_connector.cancel_order(managed_trade.takeProfitOrder)
			oco_cancelled = True
		if managed_trade.stopLossOrder and managed_trade.stopLossOrder.status == OrderStatus.OPEN:
			if (oco_cancelled == False and broker_connector.uses_oco_orders()) or not broker_connector.uses_oco_orders():
				logger.info(f'Cancelling existing Stop Loss order for trade {managed_trade.trade.id} before placing adjustment orders')
				await broker_connector.cancel_order(managed_trade.stopLossOrder)
		# Wait for the orders to be cancelled
		remaining_time = 60
		while remaining_time > 0:
			if (managed_trade.takeProfitOrder == None or managed_trade.takeProfitOrder.status != OrderStatus.CANCELLED) and (managed_trade.stopLossOrder == None or managed_trade.stopLossOrder.status != OrderStatus.CANCELLED):
				break
			await asyncio.sleep(1)
			remaining_time -= 1

		# If we reach here, the orders are either cancelled or the time has run out
		if remaining_time == 0:
			logger.error(f'Timeout reached while waiting for orders to be cancelled for trade {managed_trade.trade.id}')
			return
		
		symbol_info = symbolInfo.symbol_infos[managed_trade.entryOrder.symbol]
		round_base = symbol_info.multiplier * symbol_info.quote_step
		
		# Process the adjustment orders
		for adjustment_order in managed_trade.adjustment_orders:
			adjustment_order.price = self._calculateMidPrice(broker_connector, adjustment_order)
			logger.info(f'Calculated midprice for adjustment order: {adjustment_order.price}')
			# Debit Orders must have a price > 0
			if adjustment_order.price_effect == PriceEffect.DEBIT and adjustment_order.price <= 0:
				adjustment_order.price += broker_connector.get_min_price_increment(adjustment_order.price)

			try:
				await broker_connector.prepareOrder(adjustment_order)
				self._circuit_breaker_check(adjustment_order)
			except PrepareOrderException as e:
				logger.error(f'Failed to prepare adjustment order for trade {managed_trade.trade.id}. Skipping adjustment orders.')
				managed_trade.adjustment_orders = []
				return

			try:
				await broker_connector.placeOrder(managed_trade, adjustment_order)
			except PlaceOrderException as e:
				logger.error(f'Failed to place adjustment order for trade {managed_trade.trade.id}: {e}')
				managed_trade.adjustment_orders = []
				return
			
			# Adjustment Order has been placed.....wait for execution
			remaining_time = 60
			while remaining_time > 0:
				await asyncio.sleep(5)
				remaining_time -= 5

				if adjustment_order.status == OrderStatus.FILLED:
					logger.info(f'Adjustment order for trade {managed_trade.trade.id} has been filled at ${adjustment_order.averageFillPrice:.2f}')
					managed_trade.update_current_legs(adjustment_order)
					
					break
				elif adjustment_order.status == OrderStatus.CANCELLED:
					logger.error(f'Adjustment order for trade {managed_trade.trade.id} has been cancelled.')
					managed_trade.adjustment_orders = []
					return

				calc_adjusted_price = adjustment_order.price + broker_connector.get_min_price_increment(adjustment_order.price)

				# If the calculated Price is below the midprice, adjust it to the midprice...to prevent the market running away
				calculated_mid_price = self._calculateMidPrice(broker_connector, adjustment_order)
				if calc_adjusted_price < calculated_mid_price:
					logger.info('Calculated adjusted price is below current mid price. Adjusting to order price to mid price.')
					calc_adjusted_price = calculated_mid_price

				if len(adjustment_order.legs) == 1:
					# For Single Leg orders the round base depends on the price and the brokers rules
					round_base = broker_connector.get_min_price_increment(calc_adjusted_price) * symbol_info.multiplier
				adjustedPrice = OptionHelper.roundToTickSize(calc_adjusted_price, round_base)
				logger.info('Adjusting adjustment order. Current Limit Price: {} Adjusted Limit Price: {}', OptionHelper.roundToTickSize(adjustment_order.price), adjustedPrice)

				if await broker_connector.adjustOrder(managed_trade, adjustment_order, adjustedPrice) == True:
					adjustment_order.price = adjustedPrice
			
			if remaining_time == 0:
				logger.error(f'Timeout reached while waiting for adjustment order to be filled for trade {managed_trade.trade.id}')
				return
			
		managed_trade.adjustment_orders = [] # Clear the adjustment orders
		logger.success(f'All adjustment orders for trade {managed_trade.trade.id} have been processed successfully.')

	async def _check_and_adjust_stoploss(self, managedTrade: ManagedTrade):
		"""
		Checks if there are Stop Loss adjusters in the template of the trade and if any adjustment of the stop loss is required.
		If so it performs the adjustment of the stoploss order.

		If the trade is a credit trade and multi legged and the a long leg of the stop loss order got no bid price
		anymore because of declining value, the leg needs to be removed from the Stop Loss order.
		"""
		broker_connector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
		if broker_connector == None:
			logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to check and adjust stop loss order.')
			return
		if len(managedTrade.stoploss_adjusters) > 0:
			adjuster_index = 0
			for adjuster in managedTrade.stoploss_adjusters:
				# Find first adjuster which has not been triggered yet
				adjuster_index += 1
				if not adjuster.isTriggered():
					logger.debug(f'Checking {adjuster_index}. SL adjuster for trade {managedTrade.trade.id} at profit level {adjuster._trigger}%')
					adjusted_stoploss_price = adjuster.execute(managedTrade.current_price)
					if adjusted_stoploss_price:
						adjusted_stoploss_price = self._round_order_price(broker_connector, managedTrade.stopLossOrder, adjusted_stoploss_price)
						logger.info(f'{adjuster_index}. Stoploss adjustment for trade {managedTrade.trade.id} at profit level {adjuster._trigger}% to ${adjusted_stoploss_price:.2f}')
						if managedTrade.template.is_credit_trade() == False and adjusted_stoploss_price <= 0:
							# Stop Loss order has not been placed yet.
							logger.info(f'Stoploss price is invalid. Not placing stop loss order for trade {managedTrade.trade.id}')
							break
						
						if managedTrade.stopLossOrder.status == None:
							# Stop Loss order has not been placed yet.
							managedTrade.stopLossOrder.price = adjusted_stoploss_price
							try:
								await broker_connector.placeOrder(managedTrade, managedTrade.stopLossOrder, parent_order = managedTrade.entryOrder)
								managedTrade.stopLossOrder.status = OrderStatus.OPEN
							except PlaceOrderException as e:
								logger.error(f"Failed to place stop loss order: {e.reason}")
						else:
							await broker_connector.adjustOrder(managedTrade, managedTrade.stopLossOrder, adjusted_stoploss_price)
					break
		if managedTrade.template.is_credit_trade() and len(managedTrade.stopLossOrder.legs) > 1:
			remaining_long_legs = False
			managedTrade.long_legs_removed = False
			for leg in managedTrade.stopLossOrder.legs[:]:
				if leg.action == OrderAction.BUY: # Watch long leg
					strike_price_data = broker_connector.get_option_strike_price_data(leg.symbol, leg.expiration, leg.strike)
					bid_price = strike_price_data.callBid if leg.right == OptionRight.CALL else strike_price_data.putBid
					if bid_price <= 0:
						# This leg needs to be removed from the stop loss order
						logger.info(f'Long leg of stop loss order at strike {leg.strike} for trade {managedTrade.trade.id} has no bid price anymore. Removing leg from stop loss order.')
						managedTrade.stopLossOrder.legs.remove(leg)
						managedTrade.long_legs_removed = True
					else:
						remaining_long_legs = True

			if managedTrade.long_legs_removed:
				await broker_connector.cancel_order(managedTrade.stopLossOrder) # Cancel the old order. Order Monitoring will create new one
				if not remaining_long_legs:
					# The remaining Short legs must be reverted
					for leg in managedTrade.stopLossOrder.legs:
						if leg.action == OrderAction.SELL:
							leg.action = OrderAction.BUY
						else:
							leg.action = OrderAction.SELL
					if managedTrade.template.is_credit_trade():
						if managedTrade.stopLossOrder:
							managedTrade.stopLossOrder.price = managedTrade.stopLossOrder.price * -1
							if managedTrade.stopLossOrder.action == OrderAction.SELL_TO_CLOSE:
								managedTrade.stopLossOrder.action = OrderAction.BUY_TO_CLOSE
							else:
								managedTrade.stopLossOrder.action = OrderAction.SELL_TO_CLOSE
						if managedTrade.takeProfitOrder:
							managedTrade.takeProfitOrder.price = managedTrade.takeProfitOrder.price * -1
							if managedTrade.takeProfitOrder.action == OrderAction.SELL_TO_CLOSE:
								managedTrade.takeProfitOrder.action = OrderAction.BUY_TO_CLOSE
							else:
								managedTrade.takeProfitOrder.action = OrderAction.SELL_TO_CLOSE

	async def _check_and_adjust_delta(self, managedTrade: ManagedTrade):
		"""
		Checks and adjusts the delta for the managed trade
		"""
		for adjuster in managedTrade.delta_adjusters:
			# Check if the from time for the adjuster is reached already
			if adjuster.from_time.time() > datetime.now().time():
				continue
			
			# If Position Delta is > defined threshold -> an adjustment must be performed.
			relevant_delta = round(abs(managedTrade.current_delta) * 100, 1)
			logger.debug(f'Trade {managedTrade.trade.id} - Delta: {relevant_delta}')
			if relevant_delta > adjuster.threshold and len(managedTrade.adjustment_orders) == 0:
				logger.info(f'Adjusting delta for trade {managedTrade.trade.id} with current delta {managedTrade.current_delta} and threshold {adjuster.threshold}')
				from optrabot.tradinghubclient import NotificationType, TradinghubClient
				notification_message = '📋 Trade ' + str(managedTrade.trade.id) + ': Delta @' + str(relevant_delta) + '. Adjustment required!'
				await TradinghubClient().send_notification(NotificationType.INFO, notification_message) 
				adjustment_orders = adjuster.execute(managedTrade)
				if adjustment_orders:
					managedTrade.adjustment_orders += adjustment_orders
					self._backgroundScheduler.add_job(self._process_adjustment_orders, id='ExecuteDeltaAdjustment ' + str(managedTrade.trade.id), args=[managedTrade], misfire_grace_time = None)

	async def _check_and_perform_early_exit(self, managed_trade: ManagedTrade) -> bool:
		"""
		Checks if an early exit condition for the trade is met and closes the trade
		if necessary.
		In case of the trade is closed, it returns true, otherwise false
		"""
		if managed_trade.closing_order != None:
			logger.debug(f'Trade {managed_trade.trade.id} already has a closing order. No early exit check required any further.')
			return False
		
		early_exit = managed_trade.template.get_early_exit()
		if early_exit:
			if early_exit.type == EarlyExitTriggerType.Breakeven:
				brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managed_trade.template.account)
				underlying_price = brokerConnector.getLastPrice(symbol=managed_trade.entryOrder.symbol)
				if underlying_price == 0 or underlying_price is None:
					logger.debug(f'Unable to get underlying price for trade {managed_trade.trade.id}. Skipping breakeven check.')
					return False
				breakeven_reached = False
				for leg in managed_trade.current_legs:
					if leg.action == OrderAction.SELL:
						if leg.right == OptionRight.CALL:
							breakeven = float(leg.strike) + abs(managed_trade.entryOrder.averageFillPrice)
							if underlying_price >= breakeven:
								breakeven_reached = True
								break
						elif leg.right == OptionRight.PUT:
							breakeven = float(leg.strike) - abs(managed_trade.entryOrder.averageFillPrice)
							if underlying_price <= breakeven:
								breakeven_reached = True
								break
				if breakeven_reached:
					# Trade must be closed
					logger.debug(f'Breakeven reached for trade {managed_trade.trade.id}. Closing trade now.')
					from optrabot.tradinghubclient import NotificationType, TradinghubClient
					notification_message = '📋 Trade ' + str(managed_trade.trade.id) + ': Breakeven reached. Position will be closed now.'
					await TradinghubClient().send_notification(NotificationType.INFO, notification_message) 
					self._backgroundScheduler.add_job(self._create_closing_order, id='CreateClosingOrder' + str(managed_trade.trade.id), args=[managed_trade], misfire_grace_time = None)
					return True
		return False

	def _circuit_breaker_check(self, order: Order) -> None:
		"""
		Perform a circuit breaker check before placing an order. This method can be called after prepareOrder and the leg prices are set.
		The circuit breaker check ensure that no orders are placed when the option prices are irrationally. The bid/ask spreads must not
		exceed the double of the bid price.
		If bid price is 0.05, the maximum allowed spread is 0.20
		"""
		for leg in order.legs:
			ask_price = leg.askPrice if leg.askPrice is not None and not OptionHelper.isNan(leg.askPrice) and leg.askPrice >= 0 else 0
			bid_price = leg.bidPrice if leg.bidPrice is not None and not OptionHelper.isNan(leg.bidPrice) and leg.bidPrice >= 0 else 0
			if bid_price > 0:
				spread = round(ask_price - bid_price, 2)
				max_allowed_spread = bid_price * 2
				if bid_price < 0.1:
					# For very low priced options the maximum allowed spread is 0.10
					max_allowed_spread = 0.10
				if spread > max_allowed_spread:
					raise PrepareOrderException(f'Bid/Ask spread {spread} of option at {leg.strike} exceeds maximum allowed spread of {max_allowed_spread}.', order)

	def _composeOrderReference(self, managedTrade: ManagedTrade, action: str) -> str:
		"""
		Composes the order reference for the given trade and action
		"""
		orderReference = 'OTB (' + str(managedTrade.trade.id) + '): ' + managedTrade.template.name + ' - ' + action
		return orderReference

	def _generate_trade_group_id(self, session: Session) -> str:
		"""
		Generate a unique trade group ID in the format: TG{YYYYMMDD}-{NNN}
		
		Example: TG20251025-001, TG20251025-002, etc.
		
		Args:
			session: Database session to query existing trade group IDs
			
		Returns:
			Unique trade group ID string
		"""

		
		today = datetime.now().strftime('%Y%m%d')
		prefix = f'TG{today}-'
		
		# Find highest counter for today
		max_id_result = session.query(Trade.trade_group_id)\
			.filter(Trade.trade_group_id.like(f'{prefix}%'))\
			.order_by(Trade.trade_group_id.desc())\
			.first()
		
		if max_id_result and max_id_result[0]:
			# Extract counter from format TG20251025-001
			try:
				counter = int(max_id_result[0].split('-')[1]) + 1
			except (IndexError, ValueError):
				counter = 1
		else:
			counter = 1
		
		return f'{prefix}{counter:03d}'

	def _round_order_price(self, broker_connector: BrokerConnector, order: Order, price: float) -> float:
		"""
		Rounds the given price to the tick size or if it is a single legged order to the minimum allowed price increment
		"""
		symbolInformation = symbolInfo.symbol_infos[order.symbol]
		roundBase = symbolInformation.multiplier * symbolInformation.quote_step
		# If there is on leg only, the round base depends on the price and the brokers rules
		if len(order.legs) == 1:
			leg = order.legs[0]
			roundBase = broker_connector.get_min_price_increment(price) * symbolInformation.multiplier
		return OptionHelper.roundToTickSize(price, roundBase)

	async def _performEODTasks(self):
		"""
		Performs the end of day tasks at market close
		- Cancel any open orders for trades expiring today
		- Trades with future expiration dates continue running
		"""
		logger.info('Performing EOD tasks ...')
		today = datetime.now().date()
		has_active_trades = False
		
		for managedTrade in self._trades:
			if not managedTrade.isActive():
				continue
				
			# Get expiration date from first leg of entry order
			trade_expiration = None
			if managedTrade.entryOrder and managedTrade.entryOrder.legs:
				trade_expiration = managedTrade.entryOrder.legs[0].expiration
			
			# Only process trades that expire today
			if trade_expiration and trade_expiration > today:
				logger.debug(f'Trade {managedTrade.trade.id} expires on {trade_expiration} (future). Skipping EOD tasks.')
				continue
			
			logger.info(f'Trade {managedTrade.trade.id} is still active and expires today ({trade_expiration}). Processing EOD tasks.')
			has_active_trades = True
			managedTrade.expired = True
			
			brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
			if not brokerConnector:
				continue
				
			open_orders = 0
			if managedTrade.stopLossOrder:
				if managedTrade.stopLossOrder.status != OrderStatus.FILLED:
					logger.info(f'Cancelling Stop Loss order for trade {managedTrade.trade.id}')
					open_orders += 1
					await brokerConnector.cancel_order(managedTrade.stopLossOrder)
			if managedTrade.takeProfitOrder:
				if managedTrade.stopLossOrder and managedTrade.stopLossOrder.ocaGroup == managedTrade.takeProfitOrder.ocaGroup:
					logger.info(f'Take Profit order is cancelled automatically.')
				else:
					if managedTrade.takeProfitOrder.status != None and managedTrade.takeProfitOrder.status != OrderStatus.FILLED:
						logger.info(f'Cancelling Take Profit order for trade {managedTrade.trade.id}')
						open_orders += 1
						await brokerConnector.cancel_order(managedTrade.takeProfitOrder)
			if open_orders == 0:
				logger.info(f'No orders to be cancelled for trade {managedTrade.trade.id}.')
				
		if has_active_trades == False:
			logger.info('No active trades expiring today found. Nothing to do.')

	async def _performEODSettlement(self):
		"""
		Performs the end of day settlement tasks.
		Open Trades, which are expired (marked in EOD tasks) get settled and closed.
		Only processes trades that actually expired today.
		"""
		logger.info('Performing EOD Settlement ...')
		today = datetime.now().date()
		
		for managedTrade in self._trades:
			if managedTrade.expired == True and managedTrade.status == 'OPEN':
				# Double-check expiration date to ensure we only settle trades expiring today
				trade_expiration = None
				if managedTrade.entryOrder and managedTrade.entryOrder.legs:
					trade_expiration = managedTrade.entryOrder.legs[0].expiration
				
				if trade_expiration and trade_expiration > today:
					logger.warning(f'Trade {managedTrade.trade.id} is marked as expired but expiration is {trade_expiration} (future). Skipping settlement.')
					managedTrade.expired = False  # Reset expired flag
					continue
				
				logger.info(f'Settling and closing trade {managedTrade.trade.id} (expiration: {trade_expiration})')
				broker_connector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
				settlement_price = broker_connector.getLastPrice(managedTrade.entryOrder.symbol)
				logger.debug(f'Last price for symbol {managedTrade.entryOrder.symbol} is {settlement_price}')
				
				# Reload trade from database BEFORE processing to get latest transactions
				# This ensures we have all transactions including any that were added after trade creation
				with Session(get_db_engine()) as session:
					fresh_trade = crud.getTrade(session, managedTrade.trade.id)
					if not fresh_trade:
						logger.error(f'Could not reload trade {managedTrade.trade.id} from database for EOD settlement')
						continue
					
					# Set status to EXPIRED before updating trade
					# (TradeHelper.updateTrade() creates closing transactions for EXPIRED trades)
					fresh_trade.status = TradeStatus.EXPIRED
					
					# Update PNL based on transactions (creates closing transactions for open positions)
					# OTB-262: Pass session to avoid "database is locked" error from concurrent sessions
					TradeHelper.updateTrade(fresh_trade, session)
					
					# Store calculated values
					calculated_pnl = fresh_trade.realizedPNL
					calculated_status = fresh_trade.status
					
					# Update in database
					crud.update_trade(session, fresh_trade)
					logger.info(f'Trade {managedTrade.trade.id} settled: Status={calculated_status}, RealizedPNL=${calculated_pnl}')
					
					# Update managed trade reference
					managedTrade.trade = fresh_trade
					managedTrade.status = TradeStatus.EXPIRED
		
		for value in BrokerFactory().get_broker_connectors().values():
			broker_connector: BrokerConnector = value
			if broker_connector.isConnected() == True:
				await broker_connector.eod_settlement_tasks()
				await broker_connector.unsubscribe_ticker_data()

	def _strikes_from_order(self, order: Order) -> str:
		"""
		Returns the strike prices from the legs of the given order
		"""
		strikes = ''
		for leg in order.legs:
			if strikes != '':
				strikes += '/'
			strikes += str(leg.strike)
		return strikes

	async def _trackEntryOrder(self, managedTrade: ManagedTrade):
		"""
		Tracks the execution of the entry order
		"""
		jobId = 'TrackEntryOrder' + str(managedTrade.trade.id)
		logger.debug(f'Tracking entry order for trade {managedTrade.trade.id} on account {managedTrade.template.account}')
		if not managedTrade in self._trades:
			logger.info(f'Entry order for trade {managedTrade.trade.id} has been cancelled.')
			self._backgroundScheduler.remove_job(jobId)
			return
		
		if managedTrade.entryOrder.status == OrderStatus.FILLED:
			logger.debug(f'Entry order for trade {managedTrade.trade.id} is filled already. Stop tracking it')
			self._backgroundScheduler.remove_job(jobId)
			return

		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
		if brokerConnector == None:
			logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to adjust entry order')
			return
		
		# If broker handles adjustments internally (e.g., C2 multileg orders), skip external adjustment
		if brokerConnector.handles_adjustments_internally() and len(managedTrade.entryOrder.legs) > 1:
			logger.debug(f'Broker handles adjustments internally for multileg orders. Skipping external adjustment for trade {managedTrade.trade.id}')
			return
		
		if brokerConnector.isConnected() == False:
			logger.error(f'Broker connection for account {managedTrade.template.account} is not connected. Unable to adjust entry order')
			return
		
		if brokerConnector.isTradingEnabled() == False:
			logger.error(f'Trading is disabled for account {managedTrade.template.account}. Unable to adjust entry order')
			return
		
		# Check if max entry adjustments limit is reached
		if managedTrade.template.maxEntryAdjustments is not None and managedTrade.entry_adjustment_count >= managedTrade.template.maxEntryAdjustments:
			logger.info(f'Maximum number of {managedTrade.template.maxEntryAdjustments} entry order adjustments reached for trade {managedTrade.trade.id}. Stopping price adjustments and canceling entry order.')
			# from optrabot.tradinghubclient import TradinghubClient, NotificationType
			# await TradinghubClient().send_notification(
			# 	NotificationType.INFO, 
			# 	f'⚠️ Entry order for trade {managedTrade.trade.id} reached max adjustments ({managedTrade.template.maxEntryAdjustments}).\n*Strategy:* {managedTrade.template.strategy}\n*Account:* {managedTrade.template.account}\n*Current Price:* ${managedTrade.entryOrder.price:.2f}'
			# )
			self._backgroundScheduler.remove_job(jobId)
			await brokerConnector.cancel_order(managedTrade.entryOrder)
			return
		
		# Angepassten Preis berechnen und prüfen ob er über dem Minimum liegt
		symbol_info = symbolInfo.symbol_infos[managedTrade.entryOrder.symbol]
		round_base = symbol_info.multiplier * symbol_info.quote_step
		calc_adjusted_price = managedTrade.entryOrder.price + managedTrade.template.adjustmentStep

		# If the calculated Price is below the midprice, adjust it to the midprice...to prevent the market running away
		calculated_mid_price = self._calculateMidPrice(brokerConnector, managedTrade.entryOrder)
		if calc_adjusted_price < calculated_mid_price:
			logger.info('Calculated adjusted price is below current mid price. Adjusting to order price to mid price.')
			calc_adjusted_price = calculated_mid_price

		if len(managedTrade.entryOrder.legs) == 1:
			# For Single Leg orders the round base depends on the price and the brokers rules
			round_base = brokerConnector.get_min_price_increment(calc_adjusted_price) * symbol_info.multiplier
		adjustedPrice = OptionHelper.roundToTickSize(calc_adjusted_price, round_base)

		# The adjusted price must not cross zero
		if (managedTrade.entryOrder.price < 0 and adjustedPrice >= 0) or (managedTrade.entryOrder.price > 0 and adjustedPrice <= 0):
			logger.info('Cannot adjust the order anymore. Stopping the adjustement of the order. Order will be cancelled!')
			self._backgroundScheduler.remove_job(jobId)
			await brokerConnector.cancel_order(managedTrade.entryOrder)
			return

		logger.info('Adjusting entry order. Current Limit Price: {} Adjusted Limit Price: {}', OptionHelper.roundToTickSize(managedTrade.entryOrder.price), adjustedPrice)

		if not managedTrade.template.meetsMinimumPremium(adjustedPrice):
			logger.info('Adjusted price does not meet minimum premium requirement. Canceling entry order')
			self._backgroundScheduler.remove_job(jobId)
			await brokerConnector.cancel_order(managedTrade.entryOrder)
			return

		if not managedTrade.template.meets_maximum_premium(adjustedPrice):
			logger.info('Adjusted price exceeds maximum premium requirement. Canceling entry order')
			self._backgroundScheduler.remove_job(jobId)
			await brokerConnector.cancel_order(managedTrade.entryOrder)
			return

		if await brokerConnector.adjustOrder(managedTrade, managedTrade.entryOrder, adjustedPrice) == True:
			managedTrade.entryOrder.price = adjustedPrice
			managedTrade.entry_adjustment_count += 1
			logger.debug(f'Entry order adjustment count for trade {managedTrade.trade.id}: {managedTrade.entry_adjustment_count}/{managedTrade.template.maxEntryAdjustments or "unlimited"}')

	async def _trackClosingOrder(self, managed_trade: ManagedTrade):
		"""
		Track the closing order of the given trade and adjust the price to get filled
		"""
		job_id = 'TrackClosingOrder' + str(managed_trade.trade.id)
		logger.debug(f'Tracking closing order for trade {managed_trade.trade.id} on account {managed_trade.template.account}')

		if managed_trade.closing_order.status == OrderStatus.FILLED:
			logger.debug(f'Closing order for trade {managed_trade.trade.id} is filled already. Stop tracking it')
			self._backgroundScheduler.remove_job(job_id)
			return
		
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managed_trade.template.account)
		if brokerConnector == None:
			logger.error(f'No active broker connection found for account {managed_trade.template.account}. Unable to adjust closing order')
			return

		# If broker handles adjustments internally (e.g., C2 multileg orders), skip external adjustment
		if brokerConnector.handles_adjustments_internally() and len(managed_trade.closing_order.legs) > 1:
			logger.debug(f'Broker handles adjustments internally for multileg orders. Skipping external adjustment for trade {managed_trade.trade.id}')
			return

		if brokerConnector.isTradingEnabled() == False:
			logger.error(f'Trading is disabled for account {managed_trade.template.account}. Unable to adjust closing order')
			return
		
		# Calculate the adjusted price
		symbol_info = symbolInfo.symbol_infos[managed_trade.entryOrder.symbol]
		round_base = symbol_info.multiplier * symbol_info.quote_step
		calculated_mid_price = self._calculateMidPrice(brokerConnector, managed_trade.closing_order)
		if managed_trade.closing_order.price_effect == PriceEffect.DEBIT:
			# Debit Order - increase the price to get filled
			calc_adjusted_price = managed_trade.closing_order.price + managed_trade.template.adjustmentStep
			if calc_adjusted_price < calculated_mid_price:
				logger.info('Calculated adjusted price is below current mid price. Adjusting to order price to mid price.')
				calc_adjusted_price = calculated_mid_price
		else:
			# Credit Order - decrease the price to get filled
			calc_adjusted_price = managed_trade.closing_order.price - managed_trade.template.adjustmentStep
			if calc_adjusted_price > calculated_mid_price:
				logger.info('Calculated adjusted price is above current mid price. Adjusting to order price to mid price.')
				calc_adjusted_price = calculated_mid_price

		if len(managed_trade.entryOrder.legs) == 1:
			# For Single Leg orders the round base depends on the price and the brokers rules
			round_base = brokerConnector.get_min_price_increment(calc_adjusted_price) * symbol_info.multiplier
		calc_adjusted_price = OptionHelper.roundToTickSize(calc_adjusted_price, round_base)

		logger.info('Adjusting closing order. Current Limit Price: {} Adjusted Limit Price: {}', OptionHelper.roundToTickSize(managed_trade.closing_order.price), calc_adjusted_price)

		if await brokerConnector.adjustOrder(managed_trade, managed_trade.closing_order, calc_adjusted_price) == True:
			managed_trade.closing_order.price = calc_adjusted_price	

	async def _create_closing_order(self, managed_trade: ManagedTrade):
		"""
		Creates the closing order for the given trade.
		Legs without bid price (worthless options) are excluded from the closing order
		and stored in managed_trade.excluded_closing_legs. The $0 closing transactions
		for these legs are created only when the closing order is actually FILLED.
		"""
		logger.debug(f'Acquiring Lock for closing order for trade {managed_trade.trade.id}')
		async with self._lock:
			logger.debug(f'Creating closing order for trade {managed_trade.trade.id}')
			brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managed_trade.template.account)
			if brokerConnector == None:
				logger.error(f'No active broker connection found for account {managed_trade.template.account}. Unable to create closing order')
				return
			
			logger.debug(f'Current position value {managed_trade.current_price}')
			closing_order_legs: List[Leg] = []
			excluded_legs: List[Leg] = []  # Track legs excluded due to no bid price
			
			for current_leg in managed_trade.current_legs:
				# Check if BUY leg has no bid price (worthless option)
				# bidPrice might be None for recovered trades, so check for that first
				if current_leg.action == OrderAction.BUY and current_leg.bidPrice is not None and current_leg.bidPrice <= 0:
					logger.info(f'Leg with strike {current_leg.strike} has no bid price. It will not be closed but treated as expired worthless.')
					excluded_legs.append(current_leg)
					continue
				# Invert the leg actions for the closing order.
				closing_leg = copy.deepcopy(current_leg)	
				if current_leg.action == OrderAction.SELL:
					closing_leg.action = OrderAction.BUY
				elif current_leg.action == OrderAction.BUY:
					closing_leg.action = OrderAction.SELL
				closing_order_legs.append(closing_leg)
			
			# Store excluded legs for later - transactions will be created when closing order is FILLED
			if excluded_legs:
				managed_trade.excluded_closing_legs = excluded_legs
				logger.debug(f'Trade {managed_trade.trade.id}: {len(excluded_legs)} leg(s) excluded from closing order (no bid price). $0 transactions will be created when order is filled.')
			
			closing_price = OptionHelper.roundToTickSize(abs(managed_trade.current_price), 5)
			quantity = managed_trade.entryOrder.quantity
			
			# Determine the closing order action (inverse of entry order action)
			closing_action = OrderAction.BUY_TO_CLOSE if managed_trade.entryOrder.action == OrderAction.SELL_TO_OPEN else OrderAction.SELL_TO_CLOSE
			logger.debug(f'Entry order action: {managed_trade.entryOrder.action}, Closing order action: {closing_action}')
			
			closing_order = Order(symbol=managed_trade.trade.symbol, legs=closing_order_legs, action=closing_action, quantity=quantity, type=OrderType.LIMIT, price=closing_price)
			closing_order.orderReference = self._composeOrderReference(managed_trade, 'Close')

			try:
				await brokerConnector.prepareOrder(closing_order, True)
				self._circuit_breaker_check(closing_order)
			except PrepareOrderException as e:
				logger.error(f'Failed to prepare closing order. Reason: {e.reason}')
				return

			try:
				await brokerConnector.placeOrder(managed_trade, closing_order)
				managed_trade.closing_order = closing_order
				managed_trade.closing_order.status = OrderStatus.OPEN
				# Now Track the closing order and adjust the price to get filled
				self._backgroundScheduler.add_job(self._trackClosingOrder, 'interval', seconds=5, id='TrackClosingOrder' + str(managed_trade.trade.id), args=[managed_trade], max_instances=1, misfire_grace_time=None)

			except PlaceOrderException as e:
				logger.error(f'Failed to place the closing order for trade {managed_trade.trade.id}: {e.reason}')
				notification_message = f'Failed to close trade {managed_trade.trade.id}'
				from optrabot.tradinghubclient import NotificationType, TradinghubClient
				await TradinghubClient().send_notification(NotificationType.INFO, notification_message) 

			# TODO: At the end the stop loss and/or take profit orders need to be cancelled if they're in place.
		logger.debug(f'Releasing Lock for closing order creation for trade {managed_trade.trade.id}')

	async def _create_zero_price_closing_transactions(self, managed_trade: ManagedTrade, excluded_legs: List[Leg]) -> None:
		"""
		Creates closing transactions at $0 for legs that were excluded from the closing order
		because they have no bid price (worthless options).
		
		This ensures correct PNL calculation even when some legs cannot be sold.
		
		Args:
			managed_trade: The managed trade
			excluded_legs: List of legs that were excluded from the closing order
		"""
		with Session(get_db_engine()) as session:
			max_tx_id = crud.getMaxTransactionId(session, managed_trade.trade.id)
			db_trade = crud.getTrade(session, managed_trade.trade.id)
			
			for leg in excluded_legs:
				max_tx_id += 1
				
				# Determine closing action (inverse of the leg's current action)
				# BUY position -> SELL to close
				closing_action = OrderAction.SELL if leg.action == OrderAction.BUY else OrderAction.BUY
				sec_type = 'C' if leg.right == OptionRight.CALL else 'P'
				
				new_transaction = schemas.TransactionCreate(
					tradeid=managed_trade.trade.id,
					transactionid=max_tx_id,
					id=max_tx_id,
					symbol=managed_trade.trade.symbol,
					type=closing_action,
					sectype=sec_type,
					contracts=managed_trade.entryOrder.quantity,
					price=0.0,  # Worthless - no bid price available
					expiration=leg.expiration,
					strike=leg.strike,
					fee=0.0,
					commission=0.0,
					notes='Closed at $0 - no bid price available',
					exec_id='',
					timestamp=datetime.now(pytz.UTC)
				)
				
				crud.createTransaction(session, new_transaction)
				managed_trade.transactions.append(new_transaction)
				logger.info(f'Trade {managed_trade.trade.id}: Created $0 closing transaction for {sec_type}@{leg.strike} (no bid price)')
			
			# Update the trade to recalculate PNL
			TradeHelper.updateTrade(db_trade, session)
			session.commit()
			logger.debug(f'Trade {managed_trade.trade.id}: Created {len(excluded_legs)} zero-price closing transactions')

	async def _createTakeProfitAndStop(self, managedTrade: ManagedTrade):
		"""
		Creates the take profit and stop loss orders for the given trade
		"""
		from optrabot.tradetemplate.processor.templateprocessor import \
		    TemplateProcessor  # noqa: E101
		logger.debug(f'Acquiring Lock for TP SL creation for trade {managedTrade.trade.id}')
		async with self._lock:
			logger.debug(f'Creating take profit and stop loss orders for trade {managedTrade.trade.id}')
			brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
			if brokerConnector == None:
				logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to create take profit and stop loss orders')
				return
			
			managedTrade.entry_price = brokerConnector.getFillPrice(managedTrade.entryOrder)
			logger.debug(f'Fill price for entry order was {managedTrade.entry_price}')

			templateProcessor = TemplateProcessor().createTemplateProcessor(managedTrade.template)

			managedTrade.setup_stoploss_adjusters()
			managedTrade.setup_delta_adjusters()

			notification_message = '⚖️ Trade ' + str(managedTrade.trade.id) + ': following orders attached...'

			# Create and Prepare the Take Profit Order if a take profit is defined in the template
			orderPlaced = False
			if managedTrade.template.hasTakeProfit():
				managedTrade.takeProfitOrder = templateProcessor.composeTakeProfitOrder(managedTrade, managedTrade.entry_price)
				managedTrade.takeProfitOrder.orderReference = self._composeOrderReference(managedTrade, 'TP')
			
				try:
					await brokerConnector.prepareOrder(managedTrade.takeProfitOrder, False)
				except PrepareOrderException as e:
					logger.error(f'Failed to prepare take profit order. Reason: {e.reason}')
					return
			else:
				logger.info(f'Template {managedTrade.template.name} does not have a take profit defined. No take profit order will be created.')

			# Create and Prepare the Stop Loss Order
			if managedTrade.template.hasStopLoss():
				managedTrade.stopLossOrder = templateProcessor.composeStopLossOrder(managedTrade, managedTrade.entry_price)
				managedTrade.stopLossOrder.orderReference = self._composeOrderReference(managedTrade, 'SL')
				try:
					await brokerConnector.prepareOrder(managedTrade.stopLossOrder, False)
				except PrepareOrderException as e:
					logger.error(f'Failed to prepare stop loss order. Reason: {e.reason}')
					return
			else:
				logger.info(f'Template {managedTrade.template.name} does not have a stop loss defined. No stop loss order will be created.')
			
			# Set an OCA Group for the Take Profit and Stop Loss Orders if both are defined
			if managedTrade.takeProfitOrder != None and managedTrade.stopLossOrder != None:
				now = datetime.now()
				ocaGroup = str(managedTrade.trade.id) + '_' + now.strftime('%H%M%S')
				managedTrade.takeProfitOrder.ocaGroup = ocaGroup
				managedTrade.stopLossOrder.ocaGroup = ocaGroup

			if brokerConnector.oco_as_complex_order() and managedTrade.takeProfitOrder != None and managedTrade.stopLossOrder != None:
				# Place the OCO order as one complex order
				orderPlaced = await brokerConnector.place_complex_order(managedTrade.takeProfitOrder, managedTrade.stopLossOrder, managedTrade.template)
				if orderPlaced == True:
					if managedTrade.takeProfitOrder != None:
						managedTrade.takeProfitOrder.status = OrderStatus.OPEN
						notification_message += f'\n*Take Profit:* ${managedTrade.takeProfitOrder.price:.2f}'
					if managedTrade.stopLossOrder != None:
						managedTrade.stopLossOrder.status = OrderStatus.OPEN
						notification_message += f'\n*Stop Loss:* ${managedTrade.stopLossOrder.price:.2f}'
			else:
				if managedTrade.takeProfitOrder != None:
					if managedTrade.template.has_soft_take_profit():
						logger.info(f'Template is using soft take profit. No take profit order will be created.')
						notification_message += f'\n*Take Profit (soft):* ${managedTrade.takeProfitOrder.price:.2f}'
						orderPlaced = True
					else:
						try:
							await brokerConnector.placeOrder(managedTrade, managedTrade.takeProfitOrder, parent_order = managedTrade.entryOrder)
							orderPlaced = True
							logger.debug(f'Take Profit order for account {managedTrade.account} placed.')
							managedTrade.takeProfitOrder.status = OrderStatus.OPEN
							notification_message += f'\n*Take Profit:* ${managedTrade.takeProfitOrder.price:.2f}'
						except PlaceOrderException as e:
							logger.error(f'Failed to place take profit order: {e.reason}')
				else:
					notification_message += '\n*Take Profit:* n/d'

				if managedTrade.stopLossOrder != None:
					if managedTrade.template.is_credit_trade() == False and managedTrade.stopLossOrder.price == 0:
						# Debit Trades with Stop Loss Price of 0 must not be placed here
						logger.info(f'Stop Loss order for trade {managedTrade.trade.id} has a price of 0. No stop loss order will send to broker.')
						notification_message += f'\n*Stop Loss:* ${managedTrade.stopLossOrder.price:.2f}'
					else:
						try:
							await brokerConnector.placeOrder(managedTrade, managedTrade.stopLossOrder, parent_order = managedTrade.entryOrder)
							orderPlaced = True
							logger.debug(f'Stop Loss order for account {managedTrade.account} placed.')
							managedTrade.stopLossOrder.status = OrderStatus.OPEN
							notification_message += f'\n*Stop Loss:* ${managedTrade.stopLossOrder.price:.2f}'
						except PlaceOrderException as e:
							logger.error(f'Failed to place stop loss order: {e.reason}')
				else:
					notification_message += '\n*Stop Loss:* n/d'

			# Send Telegram Notification via OptraBot Server
			if orderPlaced == True:
				from optrabot.tradinghubclient import NotificationType, TradinghubClient
				await TradinghubClient().send_notification(NotificationType.INFO, notification_message) 

		logger.debug(f'Releasing Lock for TP SL creation for trade {managedTrade.trade.id}')

	async def _monitorOpenTrades(self):
		"""
		Monitors the open trades and their orders.
		Skips monitoring for trades that expire in the future when market is closed,
		as no price data is available outside trading sessions.
		"""
		now = datetime.now()
		today = now.date()
		market_open = BrokerFactory().is_market_open()
		pre_market = BrokerFactory().is_pre_market()

		for managedTrade in self._trades:
			if managedTrade.status != TradeStatus.OPEN or managedTrade.expired == True:
				continue

			# Check if trade expires in the future (not today)
			trade_expiration = managedTrade.get_expiration_date()
			
			# Skip monitoring for future-expiring trades when market is closed
			# (no price data available outside trading sessions)
			if not market_open and not pre_market:
				continue

			# Update current price and delta - skip trade if price data is not available
			if not self._update_current_price_and_delta(managedTrade):
				logger.debug(f'Skipping monitoring of trade {managedTrade.trade.id} - price data not available yet')
				continue

			await self._check_and_adjust_delta(managedTrade)

			if market_open:
				if await self._check_and_perform_early_exit(managedTrade):
					# No further order management required if trade has been exited.
					continue

			# Check if stop loss order is in place
			if managedTrade.stopLossOrder != None and managedTrade.adjustment_orders == []:
				if managedTrade.stopLossOrder.status == OrderStatus.CANCELLED:
					logger.warning(f'Stop Loss order for open trade {managedTrade.trade.id} was cancelled. Reestablishing it.')
					await self._reestablishStopLossOrder(managedTrade)
				else:
					# Check if the stop loss order needs to be adjusted
					await self._check_and_adjust_stoploss(managedTrade)

			if managedTrade.template.has_soft_take_profit() == False:
				if managedTrade.takeProfitOrder != None and managedTrade.adjustment_orders == []:
					if managedTrade.takeProfitOrder.status == OrderStatus.CANCELLED:
						logger.warning(f'Take Profit order for open trade {managedTrade.trade.id} was cancelled. Restablishing it.')
						await self._reestablishTakeProfitOrder(managedTrade)
			elif managedTrade.takeProfitOrder != None:
				# Check every full minute if the take profit level of the soft take profit has been reached
				if now.minute != self._last_trade_monitoring_time.minute and managedTrade.takeProfitOrder.status == None:
					logger.debug(f'Check if Take Profit has been reached for trade {managedTrade.trade.id}')
					logger.debug(f'Current Price: {managedTrade.current_price:.2f} Take Profit Price: {managedTrade.takeProfitOrder.price:.2f}')
					take_profit_reached = True if (managedTrade.template.is_credit_trade() and managedTrade.current_price <= managedTrade.takeProfitOrder.price) or (not managedTrade.template.is_credit_trade() and managedTrade.current_price >= managedTrade.takeProfitOrder.price) else False
					if take_profit_reached:
						logger.info(f'Take Profit level has been reached for trade {managedTrade.trade.id}. Placing closing take profit order now.')
						
						brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
						if brokerConnector == None:
							logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to create take profit and stop loss orders')
							continue
						
						managedTrade.takeProfitOrder.type = OrderType.MARKET
						try:
							await brokerConnector.prepareOrder(managedTrade.takeProfitOrder, False)
						except PrepareOrderException as e:
							logger.error(f'Failed to prepare take profit order. Reason: {e.reason}')
							continue

						try:
							await brokerConnector.placeOrder(managedTrade, managedTrade.takeProfitOrder, parent_order = managedTrade.entryOrder)
							logger.debug(f'Take Profit order for account {managedTrade.account} placed.')
							managedTrade.takeProfitOrder.status = OrderStatus.OPEN
							notification_message = '⚖️ Trade ' + str(managedTrade.trade.id) + ':'
							notification_message += f'\n*Soft Take Profit:* Placed market close order @ ${managedTrade.current_price:.2f}'
							from optrabot.tradinghubclient import NotificationType, TradinghubClient
							await TradinghubClient().send_notification(NotificationType.INFO, notification_message)
						except PlaceOrderException as e:
							logger.error(f'Failed to place take profit order: {e.reason}')
			
		self._last_trade_monitoring_time = now

	async def _reestablishStopLossOrder(self, managedTrade: ManagedTrade):
		"""
		Reestablishes the stop loss order for the given trade
		"""
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
		if brokerConnector == None:
			logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to reestablish stop loss order')
			return
		
		managedTrade.stopLossOrder.status = OrderStatus.OPEN
		managedTrade.stopLossOrder.price = self._round_order_price(brokerConnector, managedTrade.stopLossOrder, managedTrade.stopLossOrder.price)
		try:
			await brokerConnector.prepareOrder(managedTrade.stopLossOrder, False)
		except PrepareOrderException as e:
			logger.error(f'Failed to prepare stop loss order. Reason: {e.reason}')
			return
		
		if brokerConnector.oco_as_complex_order() and managedTrade.takeProfitOrder != None and managedTrade.stopLossOrder != None:
			orderPlaced = await brokerConnector.place_complex_order(managedTrade.takeProfitOrder, managedTrade.stopLossOrder, managedTrade.template)
		else:
			try:
				await brokerConnector.placeOrder(managedTrade, managedTrade.stopLossOrder, parent_order = managedTrade.entryOrder)
				orderPlaced = True
			except PlaceOrderException as e:
				logger.error(f'Failed to place stop loss order: {e.reason}')
				orderPlaced = False

		if orderPlaced == True:
			logger.info(f'Stop Loss order for trade {managedTrade.trade.id} reestablished successfully.')

	async def _reestablishTakeProfitOrder(self, managedTrade: ManagedTrade):
		"""
		Reestablishes the take profit order for the given trade
		"""
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
		if brokerConnector == None:
			logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to reestablish stop loss order')
			return
		
		managedTrade.takeProfitOrder.status = OrderStatus.OPEN
		managedTrade.takeProfitOrder.price = self._round_order_price(brokerConnector, managedTrade.takeProfitOrder, managedTrade.takeProfitOrder.price)
		try:
			await brokerConnector.prepareOrder(managedTrade.takeProfitOrder, False)
		except PrepareOrderException as e:
			logger.error(f'Failed to prepare take profit order. Reason: {e.reason}')
			return
		
		try:
			await brokerConnector.placeOrder(managedTrade, managedTrade.takeProfitOrder, parent_order = managedTrade.entryOrder)
			logger.info(f'Take Profit order for trade {managedTrade.trade.id} reestablished successfully.')
		except PlaceOrderException as e:
			logger.error(f'Failed to reestablish Take Profit order for trade {managedTrade.trade.id}. Reason: {e.reason}')
			return

	async def _report_excuted_trades(self) -> None:
		"""
		Reports all executed trades with their contracts to the OptraBot Hub
		It tries to report the event 3 times before giving up.
		"""
		from optrabot.tradinghubclient import TradinghubClient
		async with self._lock_upload_usage:
			try:
				# Create a copy of the values to avoid RuntimeError when modifying dict during iteration
				for contract_usage_data in list(self._undelivered_contracts.values()):
					additional_data = {
						'trade_id': contract_usage_data.trade_id,
						'account': contract_usage_data.account,
						'contracts': contract_usage_data.contracts
					}
					reporterror = False
					try_count = 0
					while try_count < 3:
						try:
							if await TradinghubClient().reportAction('CT', additional_data=json.dumps(additional_data)):
								self._undelivered_contracts.pop(contract_usage_data.trade_id, None)
								break
							else:
								logger.debug(f'Error reporting trade open event for trade {contract_usage_data.trade_id} to OptraBot Hub.')
								try_count += 1
								reporterror = True
						except Exception:
							reporterror = True
							try_count += 1
					if reporterror:
						logger.error(f'Error reporting trade open event for trade {contract_usage_data.trade_id} to OptraBot Hub within 3 tries.')
			except Exception as e:
				logger.debug(f'Unexpected error reporting executed trades to OptraBot Hub: {e}')

	def _update_current_price_and_delta(self, managed_trade: ManagedTrade):
		"""
		Updates the current price and delta of the managed Trade based on the price data from the broker.
		Returns False if price data is not available, True otherwise.
		"""
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managed_trade.template.account)
		if brokerConnector == None or brokerConnector.isConnected() == False:
			logger.error(f'No active broker connection found for account {managed_trade.template.account}. Unable to update current price')
			return False
		
		total_price: float = 0
		total_delta: float = 0
		for leg in managed_trade.current_legs:
			current_leg_price_data = brokerConnector.get_option_strike_price_data(symbol=managed_trade.entryOrder.symbol, expiration=leg.expiration, strike=leg.strike)
			
			# Check if price data is available (can be None for expired options or after trade recovery)
			if current_leg_price_data is None:
				logger.debug(f'Price data not available for trade {managed_trade.trade.id} leg at strike {leg.strike}, expiration {leg.expiration}. Skipping price update.')
				# Return False to indicate that price data is incomplete - don't process this trade further
				return False
			
			leg.midPrice = current_leg_price_data.getCallMidPrice() if leg.right == OptionRight.CALL else current_leg_price_data.getPutMidPrice()
			leg.bidPrice = current_leg_price_data.callBid if leg.right == OptionRight.CALL else current_leg_price_data.putBid
			leg.askPrice = current_leg_price_data.callAsk if leg.right == OptionRight.CALL else current_leg_price_data.putAsk
			current_leg_delta = current_leg_price_data.callDelta if leg.right == OptionRight.CALL else current_leg_price_data.putDelta
			
			# Handle missing delta (can be None for expired/unavailable options)
			if current_leg_delta is None:
				logger.debug(f'Delta not available for leg at strike {leg.strike}, using 0.0')
				current_leg_delta = 0.0
			
			if leg.action == OrderAction.SELL:
				# If it was sell, price and delta have to be negated
				current_leg_delta *= -1
			leg.delta = current_leg_delta * leg.quantity
			leg.midPrice = leg.midPrice * leg.quantity
			
			total_price += leg.midPrice if leg.action == OrderAction.BUY else leg.midPrice * -1
			total_delta += leg.delta

		total_price = abs(total_price)
		managed_trade.current_price = total_price
		managed_trade.current_delta = total_delta
		logger.trace(f'Current price for trade {managed_trade.trade.id} is {managed_trade.current_price:.2f}')
		return True

		# securityStatus = {}
		# for element in managed_trade.transactions:
		# 	transaction: schemas.Transaction = element
		# 	security = transaction.sectype + str(transaction.expiration) + str(transaction.strike)
		# 	change = transaction.contracts
		# 	fees = transaction.fee + transaction.commission
		# 	if transaction.type == OrderAction.SELL or transaction.type == 'EXP':
		# 		change = change * -1
		# 	try:
		# 		statusData = securityStatus[security]
		# 		statusData.openContracts += change
		# 	except KeyError:
		# 		statusData = SecurityStatusData(securityId=security, sec_type=transaction.sectype, strike=transaction.strike, expiration=transaction.expiration, openContracts=change, fees=transaction.fee, unrealPNL=0, realPNL = 0)
		# 		securityStatus.update({security:statusData})
		# 	statusData.unrealPNL -= ((transaction.price * symbol_info.multiplier * change) + fees)
		
		# total_unreal_pnl = 0
		# for security, statusData in securityStatus.items():
		# 	if statusData.openContracts == 0:
		# 		# contract transactions are closed
		# 		statusData.realPNL = statusData.unrealPNL
		# 		statusData.unrealPNL = 0
		# 	else:
		# 		# Contract is still open. Get current price data and
		# 		# calculate the unrealized PNL
		# 		option_price_data = brokerConnector.get_option_strike_price_data(symbol=managed_trade.entryOrder.symbol, expiration=statusData.expiration, strike=statusData.strike)
		# 		assert option_price_data != None
		# 		current_price = option_price_data.getCallMidPrice() if statusData.sec_type == OptionRight.CALL else option_price_data.getPutMidPrice()
		# 		assert current_price != None
		# 		#original_cost = (transaction.price * symbol_info.multiplier * statusData.openContracts)
		# 		current_ta_price = current_price * statusData.openContracts
		# 		#current_cost = (current_price * symbol_info.multiplier * statusData.openContracts * -1)
		# 		#unreal_pnl = current_cost - original_cost
		# 		total_price
	def _close_trade(self, managedTrade: ManagedTrade):
		"""
		Marks the trade as closed and sets the closeDate timestamp.
		Updates the trade in the database.
		
		Args:
			managedTrade: Trade to be closed
		"""
		import datetime

		import pytz
		
		managedTrade.status = TradeStatus.CLOSED
		
		# Update trade in database by reloading it in a new session
		with Session(get_db_engine()) as session:
			trade = crud.getTrade(session, managedTrade.trade.id)
			trade.status = TradeStatus.CLOSED
			trade.closeDate = datetime.datetime.now(pytz.UTC)
			session.commit()
			
		# Update the in-memory trade object
		managedTrade.trade.status = TradeStatus.CLOSED
		managedTrade.trade.closeDate = datetime.datetime.now(pytz.UTC)

	async def _deleteTrade(self, managedTrade: ManagedTrade, reason: str):
		"""
		Deletes the trade from the database and the list of managed trades.
		
		Args:
			managedTrade: Trade to be deleted
			reason: Reason for deletion
		"""
		logger.debug(f"Deleting trade {managedTrade.trade.id} from database because {reason}")
		
		# Trade aus der Datenbank löschen
		with Session(get_db_engine()) as session:
			crud.delete_trade(session, managedTrade.trade)
		
		# Trade aus der Liste der verwalteten Trades entfernen
		if managedTrade in self._trades:
			self._trades.remove(managedTrade)
		
		logger.debug(f"Trade {managedTrade.trade.id} successfully removed")

	async def close_trade_manually(self, managed_trade: ManagedTrade, trigger_flow: bool = True) -> None:
		"""
		Manually close a trade initiated by user from the UI.
		
		This will:
		1. Cancel any existing Take Profit and Stop Loss orders
		2. Create a closing order at the current mid price
		3. Monitor and adjust the limit price until filled
		
		Args:
			managed_trade: The trade to close
			trigger_flow: If True, emit MANUAL_CLOSE flow event. If False, no flow event.
		"""
		logger.info(f'Manual close requested for trade {managed_trade.trade.id} (trigger_flow={trigger_flow})')
		
		broker_connector = BrokerFactory().getBrokerConnectorByAccount(managed_trade.template.account)
		if broker_connector is None:
			logger.error(f'No active broker connection found for account {managed_trade.template.account}')
			raise Exception(f'No active broker connection for account {managed_trade.template.account}')
		
		# Store the trigger_flow flag on the managed_trade for later use when closing order is filled
		managed_trade._manual_close_trigger_flow = trigger_flow
		
		# Cancel existing Take Profit and Stop Loss orders
		oco_cancelled = False
		if managed_trade.takeProfitOrder and managed_trade.takeProfitOrder.status == OrderStatus.OPEN:
			logger.info(f'Cancelling Take Profit order for trade {managed_trade.trade.id}')
			try:
				await broker_connector.cancel_order(managed_trade.takeProfitOrder)
				oco_cancelled = True
			except Exception as e:
				logger.warning(f'Error cancelling Take Profit order: {e}')
		
		if managed_trade.stopLossOrder and managed_trade.stopLossOrder.status == OrderStatus.OPEN:
			if (not oco_cancelled and broker_connector.uses_oco_orders()) or not broker_connector.uses_oco_orders():
				logger.info(f'Cancelling Stop Loss order for trade {managed_trade.trade.id}')
				try:
					await broker_connector.cancel_order(managed_trade.stopLossOrder)
				except Exception as e:
					logger.warning(f'Error cancelling Stop Loss order: {e}')
		
		# Wait briefly for cancellation confirmations
		await asyncio.sleep(1)
		
		# Create the closing order (same logic as _create_closing_order)
		self._backgroundScheduler.add_job(
			self._create_closing_order, 
			id='CreateClosingOrder' + str(managed_trade.trade.id), 
			args=[managed_trade], 
			misfire_grace_time=None
		)
		
		logger.info(f'Manual close initiated for trade {managed_trade.trade.id}')
	
	def _emit_manual_close_event(self, managed_trade: ManagedTrade) -> None:
		"""
		Emit a MANUAL_CLOSE flow event for the trade.
		
		Args:
			managed_trade: The managed trade that was manually closed
		"""
		try:
			from optrabot.flowengine import FlowEngine
			from optrabot.flowengine.flowevent import ManualCloseEventData

			# Calculate premium and net result
			trade_premium = self._calculate_trade_premium(managed_trade)
			net_result = round(self._calculate_trade_net_result(managed_trade), 2)
			trade_fees = round(self._calculate_trade_fees(managed_trade), 2)
			
			# Determine exit price
			exit_price = 0.0
			if managed_trade.closing_order:
				exit_price = abs(managed_trade.closing_order.averageFillPrice or 0.0)
			
			# Extract expiration from first leg
			trade_expiration = None
			if managed_trade.entryOrder and managed_trade.entryOrder.legs:
				trade_expiration = managed_trade.entryOrder.legs[0].expiration
			
			event_data = ManualCloseEventData(
				event_type=FlowEventType.MANUAL_CLOSE,
				trade_id=managed_trade.trade.id,
				trade_amount=managed_trade.template.amount,
				trade_symbol=managed_trade.trade.symbol,
				trade_strategy=managed_trade.template.strategy,
				template_name=managed_trade.template.name,
				trade_expiration=trade_expiration,
				trade_group_id=managed_trade.trade.trade_group_id,
				trade_entry_price=managed_trade.entry_price,
				trade_exit_price=exit_price,
				trade_net_result=net_result,
				trade_premium=trade_premium,
				trade_fees=trade_fees
			)
			
			FlowEngine().emit_event(event_data)
			logger.debug(f'Emitted MANUAL_CLOSE flow event for trade {managed_trade.trade.id}')
			
		except Exception as e:
			logger.error(f'Error emitting MANUAL_CLOSE flow event for trade {managed_trade.trade.id}: {e}')
