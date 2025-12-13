import re
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Tuple

from ib_async import Fill
from loguru import logger

from optrabot import models
from optrabot.broker.order import OrderAction
from optrabot.tradestatus import TradeStatus


@dataclass
class SecurityStatusData:
	securityId: str
	sec_type: str
	strike: float
	expiration: date
	openContracts: int
	fees: float
	unrealPNL: float
	realPNL: float


@dataclass
class LegSummary:
	"""Summary of a trade leg (grouped from transactions)"""
	strike: float
	sectype: str  # 'C' or 'P'
	expiration: date
	action: str  # 'BUY' or 'SELL' (the entry action)
	contracts: int  # Total contracts for this leg
	total_premium: float  # Sum of (price * contracts) with sign
	

@dataclass
class TransactionGrouping:
	"""Result of grouping transactions into entry and exit groups"""
	entry_legs: List[LegSummary] = field(default_factory=list)
	exit_legs: List[LegSummary] = field(default_factory=list)
	total_entry_premium: float = 0.0
	total_exit_premium: float = 0.0
	trade_amount: int = 1  # Max contracts per leg
	total_fees: float = 0.0
	total_commission: float = 0.0
	expiration: date = None


def group_transactions(transactions: List[models.Transaction]) -> TransactionGrouping:
	"""
	Group transactions into entry and exit legs.
	
	Logic:
	- For each unique (strike, sectype, expiration), track contracts per action type (BUY/SELL)
	- Entry = transactions that open a position
	- Exit = transactions that close a position (opposite action to entry)
	- Handles partial fills correctly by summing contracts per leg
	
	The key insight: A position is opened with either BUY or SELL, and closed with the opposite.
	For credit spreads (selling options), entry is SELL, exit is BUY.
	For debit spreads (buying options), entry is BUY, exit is SELL.
	
	We determine entry vs exit by tracking which action comes FIRST for each leg.
	
	Args:
		transactions: List of Transaction objects
		
	Returns:
		TransactionGrouping with entry_legs, exit_legs, and calculated totals
	"""
	result = TransactionGrouping()
	
	# Track per leg: (strike, sectype, expiration) -> {action: contracts, ...}
	leg_actions: Dict[Tuple[float, str, date], Dict[str, List[models.Transaction]]] = {}
	
	# Sort by ID to ensure chronological order (handle missing id attribute)
	sorted_txs = sorted(transactions, key=lambda t: getattr(t, 'id', 0) or 0)
	
	for tx in sorted_txs:
		result.total_fees += getattr(tx, 'fee', 0.0) or 0.0
		result.total_commission += getattr(tx, 'commission', 0.0) or 0.0
		
		if result.expiration is None and getattr(tx, 'expiration', None):
			result.expiration = tx.expiration
		
		if getattr(tx, 'strike', None) is None or getattr(tx, 'sectype', None) is None:
			continue
			
		leg_key = (tx.strike, tx.sectype, getattr(tx, 'expiration', None))
		tx_type = getattr(tx, 'type', None)
		tx_action = (tx_type.value if hasattr(tx_type, 'value') else str(tx_type or '')).upper()
		
		if leg_key not in leg_actions:
			leg_actions[leg_key] = {}
		
		if tx_action not in leg_actions[leg_key]:
			leg_actions[leg_key][tx_action] = []
		
		leg_actions[leg_key][tx_action].append(tx)
	
	# Now determine entry vs exit for each leg
	# The action that appears first chronologically (lowest tx.id) is the entry action
	for leg_key, actions_dict in leg_actions.items():
		strike, sectype, expiration = leg_key
		
		# Find entry action (the one with the earliest transaction)
		entry_action = None
		min_tx_id = float('inf')
		
		for action, txs in actions_dict.items():
			if txs:
				tx_id = getattr(txs[0], 'id', 0) or 0
				if tx_id < min_tx_id:
					min_tx_id = tx_id
					entry_action = action
		
		if entry_action is None:
			continue
		
		# Process entry transactions
		entry_txs = actions_dict.get(entry_action, [])
		entry_contracts = 0
		entry_premium = 0.0
		
		for tx in entry_txs:
			contracts = getattr(tx, 'contracts', 0) or 0
			price = getattr(tx, 'price', 0.0) or 0.0
			entry_contracts += contracts
			# SELL adds credit, BUY adds debit
			if entry_action == 'SELL':
				entry_premium += price * contracts
			else:
				entry_premium -= price * contracts
		
		if entry_contracts > 0:
			result.entry_legs.append(LegSummary(
				strike=strike,
				sectype=sectype,
				expiration=expiration,
				action=entry_action,
				contracts=entry_contracts,
				total_premium=entry_premium
			))
			result.total_entry_premium += entry_premium
		
		# Process exit transactions (opposite action)
		exit_action = 'BUY' if entry_action == 'SELL' else 'SELL'
		exit_txs = actions_dict.get(exit_action, [])
		exit_contracts = 0
		exit_premium = 0.0
		
		for tx in exit_txs:
			contracts = getattr(tx, 'contracts', 0) or 0
			price = getattr(tx, 'price', 0.0) or 0.0
			exit_contracts += contracts
			# For exit: BUY (closing short) costs money, SELL (closing long) brings money
			if exit_action == 'BUY':
				exit_premium -= price * contracts
			else:
				exit_premium += price * contracts
		
		if exit_contracts > 0:
			result.exit_legs.append(LegSummary(
				strike=strike,
				sectype=sectype,
				expiration=expiration,
				action=exit_action,
				contracts=exit_contracts,
				total_premium=exit_premium
			))
			result.total_exit_premium += exit_premium
	
	# Trade amount is max contracts of any entry leg
	if result.entry_legs:
		result.trade_amount = max(leg.contracts for leg in result.entry_legs)
	
	return result

class TradeHelper:

	@staticmethod
	def getTradeIdFromOrderRef(orderRef: str) -> int:
		""" Extracts the OptraBot Trade Id from the order reference of a fill
		"""
		tradeId = 0
		pattern = r'^OTB\s\((?P<tradeid>[0-9]+)\):[\s0-9A-Za-z]*'
		compiledPattern = re.compile(pattern)
		match = compiledPattern.match(orderRef)
		if match:
			tradeId = int(match.group('tradeid'))
		return tradeId
	
	@staticmethod
	def isTransactionsComplete(trade: models.Trade, adjustExpired: bool = False) -> bool:
		""" Checks if the transactions of the trade with the given Id are complete,
		which means everything liquidated or expired.
		If 'adjustExpired' is True, then missing EXP transactions are created if the contract is expired already
		"""
		securityStatus = {}
		isComplete = True
		for ta in trade.transactions:
			# Dictionary aus Security-String und dem aktuellen Bestand
			# Am Ende müssen die Bestände 0 sein, damit der Trade Complete ist
			security = ta.sectype + str(ta.expiration) + str(ta.strike)
			change = ta.contracts
			if ta.type == 'SELL':
				change = change * -1
			try:
				currentStatus = securityStatus[security]
				securityStatus[security] = currentStatus+change
			except KeyError:
				securityStatus.update({security:change})
		
		for security, status in securityStatus.items():
			if status != 0:
				isComplete = False
		
		return isComplete
	
	@staticmethod
	def updateTrade(trade: models.Trade, session = None):
		""" Analyzes the transactions of the given trade and 
			- updates the status of the trade
			- calculates the realized PNL
			
		Args:
			trade: The trade to update
			session: Optional SQLAlchemy session to use for database operations.
					 If None, a new session will be created (backward compatible).
		"""
		from optrabot import symbolinfo

		# Get symbol multiplier (default to 100 if symbol not found)
		multiplier = 100
		if trade.symbol in symbolinfo.symbol_infos:
			multiplier = symbolinfo.symbol_infos[trade.symbol].multiplier
		else:
			logger.warning(f'Symbol {trade.symbol} not found in symbol_infos, using default multiplier 100')
		
		securityStatus = {}
		isComplete = True
		for ta in trade.transactions:
			security = ta.sectype + str(ta.expiration) + str(ta.strike)
			change = ta.contracts
			taFee = ta.fee + ta.commission
			# OTB-262: Case-insensitive transaction type comparison
			# Database has 'Buy', 'Sell' (from OrderAction enum values)
			# But need to handle legacy or broker-specific variations
			tx_type = ta.type
			is_sell = (tx_type == OrderAction.SELL or 
					   tx_type == 'Sell' or 
					   (isinstance(tx_type, str) and tx_type.upper() == 'SELL'))
			if is_sell:
				change = change * -1
			try:
				statusData = securityStatus[security]
				statusData.openContracts += change
			except KeyError:
				statusData = SecurityStatusData(securityId=security, sec_type=ta.sectype, strike=ta.strike, expiration=ta.expiration, openContracts=change, fees=ta.fee, unrealPNL=0, realPNL = 0)
				securityStatus.update({security:statusData})
			statusData.fees += taFee
			# Track unrealized P&L (price impact + fees)
			statusData.unrealPNL -= ((ta.price * multiplier * change) + taFee)
		
		# For EXPIRED trades: Create closing transactions for open positions
		if trade.status == TradeStatus.EXPIRED:
			logger.debug(f'Trade {trade.id} is EXPIRED - checking for open positions requiring closing transactions')
			import datetime

			import pytz

			from optrabot import crud
			from optrabot.database import SessionLocal

			# Use provided session or create a new one
			use_existing_session = session is not None
			db_session = session if use_existing_session else SessionLocal()
			
			try:
				max_tx_id = crud.getMaxTransactionId(db_session, trade.id)
				exp_transactions_created = 0
				
				for security, statusData in securityStatus.items():
					if statusData.openContracts != 0:
						# Position is open - create closing transaction at $0 (expired worthless)
						# If openContracts > 0: Long position → SELL to close
						# If openContracts < 0: Short position → BUY to close
						closing_type = OrderAction.SELL if statusData.openContracts > 0 else OrderAction.BUY
						
						max_tx_id += 1
						exp_transaction = models.Transaction(
							tradeid=trade.id,
							id=max_tx_id,
							type=closing_type,
							sectype=statusData.sec_type,
							timestamp=datetime.datetime.now(pytz.UTC),
							expiration=statusData.expiration,
							strike=statusData.strike,
							contracts=abs(statusData.openContracts),
							price=0.0,  # Expired worthless
							fee=0.0,
							commission=0.0,
							notes=f'Auto-generated closing transaction for expired {statusData.sec_type} position'
						)
						db_session.add(exp_transaction)
						exp_transactions_created += 1
						logger.debug(f'Created {closing_type} transaction for Trade {trade.id}: {statusData.sec_type}@{statusData.strike} ({abs(statusData.openContracts)} contracts) - expired worthless')
						
						# OTB-262: Update statusData to reflect the closed position
						# The closing transaction at $0 doesn't change the P&L (already in unrealPNL)
						statusData.openContracts = 0
						statusData.realPNL = statusData.unrealPNL
				
				if exp_transactions_created > 0:
					# Only commit if we created our own session
					if not use_existing_session:
						db_session.commit()
					logger.debug(f'Created {exp_transactions_created} closing transactions for Trade {trade.id}')
					
					# OTB-262: After creating closing transactions, all positions are now closed
					# Force isComplete to True so realizedPNL calculation happens below
					# Note: We already updated statusData.openContracts = 0 for all positions above
					isComplete = True
					logger.debug(f'Trade {trade.id}: All positions closed via expiration, isComplete=True')
				else:
					# No closing transactions were created - positions were already closed
					logger.debug(f'Trade {trade.id}: No closing transactions needed - all positions already closed')
			finally:
				# Only close session if we created it
				if not use_existing_session:
					db_session.close()
					# Check if trade is actually complete by examining securityStatus
					logger.debug(f'Trade {trade.id}: No closing transactions created (positions already closed or no open positions found)')
		
		# Calculate realized P&L based on final position status
		trade.realizedPNL = 0
		for security, statusData in securityStatus.items():
			if statusData.openContracts == 0:
				# Leg is closed - realized P&L is the full unrealized P&L
				statusData.realPNL = statusData.unrealPNL
				trade.realizedPNL += statusData.realPNL
			else:
				# Leg still open - only fees are realized (as costs), no P&L yet
				statusData.realPNL = -statusData.fees  # Negative because fees are costs
				# Don't add to trade.realizedPNL - open positions don't contribute to realized P&L
				# Trade is not complete yet
				# OTB-262: Only set isComplete to False if not already set by EXPIRED logic
				if trade.status != TradeStatus.EXPIRED:
					isComplete = False
		
		if isComplete == True:
			trade.realizedPNL = round(trade.realizedPNL, 2)
			logger.debug(f'Trade {trade.id}: Calculated realizedPNL = ${trade.realizedPNL}')
			# Only set status to CLOSED if it's not already EXPIRED
			# This preserves the distinction between regularly closed trades and expired trades
			if trade.status != TradeStatus.EXPIRED:
				trade.status = TradeStatus.CLOSED




			
				