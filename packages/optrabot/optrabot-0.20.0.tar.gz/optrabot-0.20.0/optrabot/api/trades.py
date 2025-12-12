"""
Trades API Endpoints

This module provides API endpoints for managing and viewing trades.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

import pytz
from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from pydantic import BaseModel

from optrabot import config as optrabotcfg
from optrabot.broker.order import OrderAction
from optrabot.database import SessionLocal
from optrabot.managedtrade import ManagedTrade
from optrabot.models import Trade as TradeModel
from optrabot.models import Transaction as TransactionModel
from optrabot.signaldata import SignalData
from optrabot.trademanager import TradeManager
from optrabot.tradestatus import TradeStatus
from optrabot.tradetemplate.processor.templateprocessor import \
    TemplateProcessor
from optrabot.tradetemplate.templatefactory import Template

router = APIRouter(prefix='/api')


class LegInfo(BaseModel):
    """Leg information for display"""
    strike: float
    right: str  # 'CALL' or 'PUT'
    action: str  # 'BUY' or 'SELL'
    expiration: Optional[str] = None


class TradeInfo(BaseModel):
    """Trade information for the frontend"""
    id: int
    template_name: str
    template_group: Optional[str]
    strategy: str
    account: str
    symbol: str
    status: str
    entry_price: Optional[float]
    current_price: Optional[float]
    current_pnl: Optional[float]
    amount: int
    entry_time: Optional[str]
    close_time: Optional[str] = None
    fees: Optional[float] = None
    commission: Optional[float] = None
    legs: List[LegInfo]
    expiration: Optional[str]


class CloseTradeRequest(BaseModel):
    """Request model for closing a trade"""
    trade_id: int
    trigger_flow: bool = True  # If False, no flow events will be triggered


class CloseTradeResponse(BaseModel):
    """Response model for close trade request"""
    success: bool
    message: str
    trade_id: int


class TimeRange(str, Enum):
    """Time range filter options"""
    TODAY = 'today'
    YESTERDAY = 'yesterday'
    THIS_WEEK = 'this_week'
    ALL = 'all'


def _get_time_range_start(time_range: TimeRange) -> Optional[datetime]:
    """Get the start datetime for the given time range filter"""
    now = datetime.now(pytz.timezone('US/Eastern'))
    
    if time_range == TimeRange.TODAY:
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_range == TimeRange.YESTERDAY:
        yesterday = now - timedelta(days=1)
        return yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_range == TimeRange.THIS_WEEK:
        # Start of current week (Monday)
        days_since_monday = now.weekday()
        week_start = now - timedelta(days=days_since_monday)
        return week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        return None  # ALL - no filter


def _db_trade_to_info(db_trade: TradeModel, templates: list | None = None) -> TradeInfo:
    """Convert a database Trade model to TradeInfo for API response
    
    Args:
        db_trade: The database Trade model
        templates: Optional list of templates to look up template_group
    """
    
    # Try to find template_group from templates list
    template_group = None
    template_name = db_trade.template_name or db_trade.strategy
    if templates and template_name:
        for template in templates:
            if template.name == template_name:
                template_group = template.template_group
                break
    
    # Build leg information from transactions
    legs = []
    entry_price = 0.0
    close_price = 0.0
    expiration = None
    total_fees = 0.0
    total_commission = 0.0
    
    # Sort transactions by ID to ensure chronological order
    sorted_transactions = sorted(db_trade.transactions, key=lambda t: t.id)
    
    # Separate entry and exit transactions
    # Strategy: Track which strike/type combinations we've seen
    # First occurrence is entry, second occurrence is exit
    entry_transactions = []
    exit_transactions = []
    seen_legs: dict[tuple, bool] = {}  # (strike, sectype) -> has_entry
    
    for tx in sorted_transactions:
        total_fees += tx.fee or 0.0
        total_commission += tx.commission or 0.0
        
        # Check notes first for explicit Open/Close markers
        if tx.notes and 'Open' in tx.notes:
            entry_transactions.append(tx)
            continue
        if tx.notes and ('Close' in tx.notes or 'Exp' in tx.notes):
            exit_transactions.append(tx)
            continue
            
        # Fallback: use strike/type as key to determine entry vs exit
        if tx.strike and tx.sectype:
            leg_key = (tx.strike, tx.sectype)
            if leg_key not in seen_legs:
                # First time seeing this leg - it's an entry
                seen_legs[leg_key] = True
                entry_transactions.append(tx)
            else:
                # Second time seeing this leg - it's an exit
                exit_transactions.append(tx)
        else:
            # No strike info, use simple heuristic based on transaction count
            # First half are entries, second half are exits
            total_count = len(sorted_transactions)
            if tx.id <= sorted_transactions[total_count // 2 - 1].id if total_count > 1 else True:
                entry_transactions.append(tx)
            else:
                exit_transactions.append(tx)
    
    # Calculate entry price from entry transactions
    # Also determine the trade amount from contracts (max of any leg)
    trade_amount = 1  # Default to 1 if we can't determine from transactions
    for tx in entry_transactions:
        # Track max contracts across all entry legs
        if tx.contracts and tx.contracts > trade_amount:
            trade_amount = tx.contracts
        if tx.strike and tx.sectype:
            tx_type_upper = (tx.type or '').upper()
            legs.append(LegInfo(
                strike=tx.strike,
                right='CALL' if tx.sectype == 'C' else 'PUT',
                action='BUY' if tx_type_upper == 'BUY' else 'SELL',
                expiration=tx.expiration.strftime('%Y-%m-%d') if tx.expiration else None
            ))
            if expiration is None and tx.expiration:
                expiration = tx.expiration.strftime('%Y-%m-%d')
        # For SELL transactions, add price (credit); for BUY, subtract (debit)
        tx_type_upper = (tx.type or '').upper()
        if tx_type_upper == 'SELL':
            entry_price += tx.price or 0.0
        else:
            entry_price -= tx.price or 0.0
    
    # Calculate close price from exit transactions
    for tx in exit_transactions:
        # For BUY (close short), subtract; for SELL (close long), add
        tx_type_upper = (tx.type or '').upper()
        if tx_type_upper == 'BUY':
            close_price -= tx.price or 0.0
        else:
            close_price += tx.price or 0.0
    
    # Get entry time
    entry_time = None
    if db_trade.openDate:
        entry_time = db_trade.openDate.isoformat()
    
    # Get close time
    close_time = None
    if db_trade.closeDate:
        close_time = db_trade.closeDate.isoformat()
    
    return TradeInfo(
        id=db_trade.id,
        template_name=db_trade.template_name or db_trade.strategy or 'Unknown',
        template_group=template_group,  # Looked up from templates list
        strategy=db_trade.strategy or 'Unknown',
        account=db_trade.account or '',
        symbol=db_trade.symbol or '',
        status=db_trade.status,
        entry_price=round(entry_price, 2) if entry_price != 0 else None,
        current_price=round(close_price, 2) if close_price != 0 else None,
        current_pnl=db_trade.realizedPNL,
        amount=trade_amount,  # Determined from entry transactions
        entry_time=entry_time,
        close_time=close_time,
        fees=round(total_fees, 2) if total_fees > 0 else None,
        commission=round(total_commission, 2) if total_commission > 0 else None,
        legs=legs,
        expiration=expiration
    )


def _managed_trade_to_info(
    managed_trade: ManagedTrade, 
    transactions: list | None = None,
    db_realized_pnl: float | None = None
) -> TradeInfo:
    """Convert a ManagedTrade to TradeInfo for API response
    
    Args:
        managed_trade: The ManagedTrade object
        transactions: Optional list of transactions (pre-loaded from DB to avoid lazy-loading issues)
        db_realized_pnl: Optional realizedPNL from database (for closed trades)
    """
    
    # Build leg information
    legs = []
    for leg in managed_trade.current_legs:
        legs.append(LegInfo(
            strike=leg.strike,
            right='CALL' if leg.right.value == 'C' else 'PUT',
            action='BUY' if leg.action == OrderAction.BUY else 'SELL',
            expiration=leg.expiration.strftime('%Y-%m-%d') if leg.expiration else None
        ))
    
    # Get expiration from legs or entry order
    expiration = None
    if managed_trade.current_legs and len(managed_trade.current_legs) > 0:
        exp_date = managed_trade.current_legs[0].expiration
        if exp_date:
            expiration = exp_date.strftime('%Y-%m-%d')
    
    # Calculate fees and commission from transactions first (needed for PNL)
    # Use provided transactions list or fallback to trade.transactions (may fail if detached)
    total_fees = 0.0
    total_commission = 0.0
    tx_list = transactions if transactions is not None else (managed_trade.trade.transactions if managed_trade.trade else [])
    for tx in tx_list:
        total_fees += tx.fee or 0.0
        total_commission += tx.commission or 0.0
    
    # Calculate current PNL
    current_pnl = None
    # For closed/expired trades, use realizedPNL from database (already includes fees)
    if managed_trade.status in [TradeStatus.CLOSED, TradeStatus.EXPIRED]:
        # Prefer db_realized_pnl (fresh from DB) over managed_trade.trade.realizedPNL (may be stale)
        if db_realized_pnl is not None:
            current_pnl = db_realized_pnl
        elif managed_trade.trade and managed_trade.trade.realizedPNL is not None:
            current_pnl = managed_trade.trade.realizedPNL
    # For open trades, calculate from entry and current price
    # Only calculate if we have a valid current price (not None and not 0)
    elif managed_trade.entry_price is not None and managed_trade.current_price is not None and managed_trade.current_price != 0:
        # Use is_credit_trade() method from template to determine calculation
        # For credit trades: profit when current price < entry price (we want to buy back cheaper)
        # For debit trades: profit when current price > entry price (we want to sell higher)
        if managed_trade.template and managed_trade.template.is_credit_trade():
            current_pnl = (managed_trade.entry_price - managed_trade.current_price) * 100 * managed_trade.template.amount
        else:
            current_pnl = (managed_trade.current_price - managed_trade.entry_price) * 100 * (managed_trade.template.amount if managed_trade.template else 1)
        
        # Subtract fees and commissions from PNL to get net result
        current_pnl -= (total_fees + total_commission)
    
    # Get entry time from trade record
    entry_time = None
    if managed_trade.trade and managed_trade.trade.openDate:
        entry_time = managed_trade.trade.openDate.isoformat()
    
    # Get close time from trade record or calculate from transactions
    close_time = None
    close_price = None
    if managed_trade.status in [TradeStatus.CLOSED, TradeStatus.EXPIRED]:
        # First try to get from trade record
        if managed_trade.trade and managed_trade.trade.closeDate:
            close_time = managed_trade.trade.closeDate.isoformat()
        
        # Calculate close price and time from transactions if we have them
        # Use provided transactions list or fallback to trade.transactions
        tx_for_close = transactions if transactions is not None else (managed_trade.trade.transactions if managed_trade.trade else [])
        if tx_for_close:
            sorted_transactions = sorted(tx_for_close, key=lambda t: t.id)
            seen_legs: dict[tuple, bool] = {}
            exit_transactions = []
            
            for tx in sorted_transactions:
                if tx.strike and tx.sectype:
                    leg_key = (tx.strike, tx.sectype)
                    if leg_key not in seen_legs:
                        seen_legs[leg_key] = True
                    else:
                        exit_transactions.append(tx)
            
            # Calculate close price from exit transactions
            if exit_transactions:
                close_price = 0.0
                latest_timestamp = None
                for tx in exit_transactions:
                    tx_type_upper = (tx.type or '').upper()
                    if tx_type_upper == 'BUY':
                        close_price -= tx.price or 0.0
                    else:
                        close_price += tx.price or 0.0
                    # Track latest timestamp for close time
                    if tx.timestamp and (latest_timestamp is None or tx.timestamp > latest_timestamp):
                        latest_timestamp = tx.timestamp
                
                close_price = round(close_price, 2)
                
                # Use transaction timestamp as close time if not set
                if close_time is None and latest_timestamp:
                    close_time = latest_timestamp.isoformat()
    
    # For open trades, use current_price (but treat 0 as "not yet available")
    display_current_price = close_price if close_price is not None else managed_trade.current_price
    if display_current_price == 0:
        display_current_price = None
    
    return TradeInfo(
        id=managed_trade.trade.id if managed_trade.trade else 0,
        template_name=managed_trade.template.name if managed_trade.template else 'Unknown',
        template_group=managed_trade.template.template_group if managed_trade.template else None,
        strategy=managed_trade.template.strategy if managed_trade.template else 'Unknown',
        account=managed_trade.account or '',
        symbol=managed_trade.trade.symbol if managed_trade.trade else '',
        status=managed_trade.status,
        entry_price=managed_trade.entry_price,
        current_price=display_current_price,
        current_pnl=round(current_pnl, 2) if current_pnl is not None else None,
        amount=managed_trade.template.amount if managed_trade.template else 1,
        entry_time=entry_time,
        close_time=close_time,
        fees=round(total_fees, 2) if total_fees > 0 else None,
        commission=round(total_commission, 2) if total_commission > 0 else None,
        legs=legs,
        expiration=expiration
    )


@router.get('/trades/', response_model=List[TradeInfo])
async def get_trades(
    status: Optional[str] = Query(None, description='Filter by trade status (NEW, OPEN, CLOSED, EXPIRED)'),
    strategy: Optional[str] = Query(None, description='Filter by strategy name'),
    template_group: Optional[str] = Query(None, description='Filter by template group'),
    account: Optional[str] = Query(None, description='Filter by account'),
    time_range: TimeRange = Query(TimeRange.TODAY, description='Time range filter')
) -> List[TradeInfo]:
    """
    Get list of trades with optional filters.
    
    Returns managed trades from TradeManager and closed/expired trades from database.
    """
    from sqlalchemy import select

    import optrabot.config as optrabotcfg
    try:
        trade_manager = TradeManager()
        managed_trades = trade_manager.getManagedTrades()
        
        # Get all templates for looking up template_group
        config: optrabotcfg.Config = optrabotcfg.appConfig
        all_templates = config.getTemplates() if config else []
        
        # Track IDs of managed trades to avoid duplicates
        managed_trade_ids = {mt.trade.id for mt in managed_trades if mt.trade and mt.trade.id}
        logger.debug(f"Managed trade IDs for transaction loading: {managed_trade_ids}")
        
        # Get time range start for filtering
        time_range_start = _get_time_range_start(time_range)
        
        result = []
        
        # Use a session to load transactions for managed trades
        with SessionLocal() as session:
            # Pre-load transactions and realizedPNL for all managed trades from database directly
            trade_transactions: dict[int, list] = {}
            trade_realized_pnl: dict[int, float | None] = {}
            if managed_trade_ids:
                # Query transactions directly instead of using relationship
                from optrabot.models import Transaction as TransactionModel
                tx_query = select(TransactionModel).where(
                    TransactionModel.tradeid.in_(managed_trade_ids)
                )
                all_transactions = session.scalars(tx_query).all()
                logger.debug(f'Loaded {len(all_transactions)} transactions for {len(managed_trade_ids)} trades')
                
                # Group by trade ID (ensure integer keys)
                for tx in all_transactions:
                    trade_id_key = int(tx.tradeid)
                    if trade_id_key not in trade_transactions:
                        trade_transactions[trade_id_key] = []
                    trade_transactions[trade_id_key].append(tx)
                
                for trade_id, txs in trade_transactions.items():
                    logger.debug(f'Trade {trade_id} has {len(txs)} transactions')
                
                # Also load realizedPNL from database for closed trades
                pnl_query = select(TradeModel.id, TradeModel.realizedPNL).where(
                    TradeModel.id.in_(managed_trade_ids)
                )
                for row in session.execute(pnl_query):
                    trade_realized_pnl[row[0]] = row[1]
            
            # First, add active managed trades
            for managed_trade in managed_trades:
                # Apply status filter
                if status and managed_trade.status != status:
                    continue
                
                # Apply strategy filter
                if strategy and managed_trade.template and managed_trade.template.strategy != strategy:
                    continue
                
                # Apply template group filter
                if template_group:
                    trade_group = managed_trade.template.template_group if managed_trade.template else None
                    if template_group == 'none':
                        if trade_group is not None:
                            continue
                    elif trade_group != template_group:
                        continue
                
                # Apply account filter
                if account and managed_trade.account != account:
                    continue
                
                # Apply time range filter
                if time_range_start and managed_trade.trade:
                    # Get trade time - use openDate if available, otherwise include NEW trades
                    trade_time = managed_trade.trade.openDate
                    if trade_time is None:
                        # NEW trades without openDate should be included (they're current)
                        pass
                    else:
                        # Make sure we're comparing timezone-aware datetimes
                        if trade_time.tzinfo is None:
                            trade_time = pytz.UTC.localize(trade_time)
                        # Convert to same timezone for comparison
                        time_range_start_utc = time_range_start.astimezone(pytz.UTC)
                        trade_time_utc = trade_time.astimezone(pytz.UTC)
                        if trade_time_utc < time_range_start_utc:
                            continue
                
                # Get transactions and realizedPNL from preloaded data
                trade_id = managed_trade.trade.id if managed_trade.trade else None
                transactions = trade_transactions.get(trade_id, []) if trade_id else []
                db_pnl = trade_realized_pnl.get(trade_id) if trade_id else None
                logger.debug(f'Trade {trade_id}: found {len(transactions)} preloaded transactions, db_pnl={db_pnl}')
                result.append(_managed_trade_to_info(managed_trade, transactions, db_pnl))
            # Build query for closed/expired trades
            query = select(TradeModel).where(
                TradeModel.status.in_([TradeStatus.CLOSED, TradeStatus.EXPIRED])
            )
            
            # Apply filters
            if status:
                query = query.where(TradeModel.status == status)
            if strategy:
                query = query.where(TradeModel.strategy == strategy)
            if account:
                query = query.where(TradeModel.account == account)
            if time_range_start:
                # Filter by openDate (when the trade was opened)
                time_range_start_utc = time_range_start.astimezone(pytz.UTC)
                query = query.where(TradeModel.openDate >= time_range_start_utc)
            
            db_trades = session.scalars(query).all()
            
            for db_trade in db_trades:
                # Skip if already in managed trades
                if db_trade.id in managed_trade_ids:
                    continue
                result.append(_db_trade_to_info(db_trade, all_templates))
        
        # Sort by ID descending (newest first)
        result.sort(key=lambda x: x.id, reverse=True)
        
        return result
        
    except Exception as e:
        logger.error(f'Error fetching trades: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/trades/filters')
async def get_trade_filters():
    """
    Get available filter options based on current and historical trades.
    
    Returns unique values for strategy, template_group, and account.
    """
    from sqlalchemy import distinct, select
    try:
        trade_manager = TradeManager()
        managed_trades = trade_manager.getManagedTrades()
        
        strategies = set()
        template_groups = set()
        accounts = set()
        
        # Get filters from active managed trades
        for managed_trade in managed_trades:
            if managed_trade.template:
                if managed_trade.template.strategy:
                    strategies.add(managed_trade.template.strategy)
                if managed_trade.template.template_group:
                    template_groups.add(managed_trade.template.template_group)
            if managed_trade.account:
                accounts.add(managed_trade.account)
        
        # Also get filters from closed/expired trades in database
        with SessionLocal() as session:
            # Get distinct strategies
            db_strategies = session.scalars(
                select(distinct(TradeModel.strategy)).where(TradeModel.strategy.isnot(None))
            ).all()
            strategies.update(db_strategies)
            
            # Get distinct accounts
            db_accounts = session.scalars(
                select(distinct(TradeModel.account)).where(TradeModel.account.isnot(None))
            ).all()
            accounts.update(db_accounts)
        
        return {
            'strategies': sorted(list(strategies)),
            'template_groups': sorted(list(template_groups)),
            'accounts': sorted(list(accounts)),
            'statuses': [TradeStatus.NEW, TradeStatus.OPEN, TradeStatus.CLOSED, TradeStatus.EXPIRED],
            'time_ranges': [
                {'value': 'today', 'label': 'Heute'},
                {'value': 'yesterday', 'label': 'Gestern'},
                {'value': 'this_week', 'label': 'Diese Woche'},
                {'value': 'all', 'label': 'Alle'}
            ]
        }
        
    except Exception as e:
        logger.error(f'Error fetching trade filters: {e}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/trades/close', response_model=CloseTradeResponse)
async def close_trade(request: CloseTradeRequest) -> CloseTradeResponse:
    """
    Close a trade manually.
    
    This will:
    1. Cancel any existing Take Profit and Stop Loss orders
    2. Create a closing order at the current mid price
    3. Monitor and adjust the limit price until filled
    
    If trigger_flow is False, no flow events (MANUAL_CLOSE) will be fired.
    This is useful for emergency closings where you don't want flows to trigger.
    """
    try:
        trade_manager = TradeManager()
        
        # Find the managed trade
        managed_trade = None
        for mt in trade_manager.getManagedTrades():
            if mt.trade and mt.trade.id == request.trade_id:
                managed_trade = mt
                break
        
        if not managed_trade:
            raise HTTPException(status_code=404, detail=f'Trade {request.trade_id} not found')
        
        # Check if trade can be closed
        if managed_trade.status not in [TradeStatus.NEW, TradeStatus.OPEN]:
            raise HTTPException(
                status_code=400, 
                detail=f'Trade {request.trade_id} cannot be closed (status: {managed_trade.status})'
            )
        
        # Close the trade
        await trade_manager.close_trade_manually(
            managed_trade, 
            trigger_flow=request.trigger_flow
        )
        
        return CloseTradeResponse(
            success=True,
            message=f'Trade {request.trade_id} closing initiated',
            trade_id=request.trade_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error closing trade {request.trade_id}: {e}')
        raise HTTPException(status_code=500, detail=str(e)) from e


class InstantTradeRequest(BaseModel):
    """Request model for starting an instant trade"""
    template_name: str


class InstantTradeResponse(BaseModel):
    """Response model for instant trade request"""
    success: bool
    message: str
    template_name: str


@router.post('/trades/instant', response_model=InstantTradeResponse)
async def start_instant_trade(request: InstantTradeRequest) -> InstantTradeResponse:
    """
    Start an instant trade using the specified template.
    
    This triggers the template processing similar to a time-based trigger
    or an external signal from the OptraBot Hub.
    """
    try:
        config: optrabotcfg.Config = optrabotcfg.appConfig
        templates = config.getTemplates()
        
        # Find the requested template
        template: Template | None = None
        for t in templates:
            if t.name == request.template_name:
                template = t
                break
        
        if template is None:
            raise HTTPException(
                status_code=404, 
                detail=f'Template "{request.template_name}" not found'
            )
        
        if not template.is_enabled():
            raise HTTPException(
                status_code=400,
                detail=f'Template "{request.template_name}" is disabled'
            )
        
        # Create signal data with current timestamp
        signal_data = SignalData(
            timestamp=datetime.now().astimezone(pytz.UTC), 
            close=0, 
            strike=0
        )
        
        # Process the template
        template_processor = TemplateProcessor()
        
        try:
            await template_processor.processTemplate(template, signal_data)
        except ValueError as ve:
            # Template conditions not met or other validation errors
            raise HTTPException(status_code=400, detail=str(ve)) from ve
        except Exception as proc_error:
            logger.error(f'Error processing template {request.template_name}: {proc_error}')
            raise HTTPException(
                status_code=500, 
                detail=f'Failed to process template: {str(proc_error)}'
            ) from proc_error
        
        logger.info(f'Instant trade started for template {request.template_name}')
        
        return InstantTradeResponse(
            success=True,
            message=f'Trade for template "{request.template_name}" initiated successfully',
            template_name=request.template_name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error starting instant trade for {request.template_name}: {e}')
        raise HTTPException(status_code=500, detail=str(e)) from e
