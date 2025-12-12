"""
Flow Event Data Classes

This module defines the event data structures that are passed to flows
when they are triggered.
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class FlowEventType(str, Enum):
    """Enumeration of available flow event types"""
    EARLY_EXIT = "early_exit"
    TRADE_OPENED = "trade_opened"
    STOP_LOSS_HIT = "stop_loss_hit"
    TAKE_PROFIT_HIT = "take_profit_hit"
    MANUAL_CLOSE = "manual_close"


@dataclass
class FlowEventData:
    """Base class for flow event data"""
    event_type: FlowEventType
    trade_id: int
    trade_amount: int
    trade_symbol: str
    trade_strategy: str
    template_name: str
    trade_expiration: date
    trade_group_id: str  # Trade group ID for grouping related trades (no default here!)
    
    def get_variables(self) -> dict:
        """
        Returns a dictionary of variables that can be used in flow expressions.
        Variable names use the EVENT-TRADE- prefix.
        """
        return {
            'EVENT_TRADE_ID': self.trade_id,
            'EVENT_TRADE_AMOUNT': self.trade_amount,
            'EVENT_TRADE_SYMBOL': self.trade_symbol,
            'EVENT_TRADE_STRATEGY': self.trade_strategy,
            'EVENT_TRADE_EXPIRATION': self.trade_expiration,
            'EVENT_TRADE_GROUP_ID': self.trade_group_id,
        }


@dataclass
class TradeOpenedEventData(FlowEventData):
    """Event data for trade_opened events"""
    trade_entry_price: float
    
    def __post_init__(self):
        self.event_type = FlowEventType.TRADE_OPENED
    
    def get_variables(self) -> dict:
        variables = super().get_variables()
        variables.update({
            'EVENT_TRADE_ENTRY_PRICE': self.trade_entry_price,
        })
        return variables


@dataclass
class TradeExitEventData(FlowEventData):
    """Base class for trade exit events (early_exit, stop_loss_hit, take_profit_hit)"""
    trade_entry_price: float
    trade_exit_price: float
    trade_net_result: float
    trade_premium: float
    trade_fees: float
    
    def get_variables(self) -> dict:
        variables = super().get_variables()
        variables.update({
            'EVENT_TRADE_ENTRY_PRICE': self.trade_entry_price,
            'EVENT_TRADE_EXIT_PRICE': self.trade_exit_price,
            'EVENT_TRADE_NET_RESULT': self.trade_net_result,
            'EVENT_TRADE_PREMIUM': self.trade_premium,
            'EVENT_TRADE_FEES': self.trade_fees,
        })
        return variables


@dataclass
class EarlyExitEventData(TradeExitEventData):
    """Event data for early_exit events"""
    
    def __post_init__(self):
        self.event_type = FlowEventType.EARLY_EXIT


@dataclass
class StopLossHitEventData(TradeExitEventData):
    """Event data for stop_loss_hit events"""
    
    def __post_init__(self):
        self.event_type = FlowEventType.STOP_LOSS_HIT


@dataclass
class TakeProfitHitEventData(TradeExitEventData):
    """Event data for take_profit_hit events"""
    
    def __post_init__(self):
        self.event_type = FlowEventType.TAKE_PROFIT_HIT


@dataclass
class ManualCloseEventData(TradeExitEventData):
    """Event data for manual_close events (when user manually closes a trade)"""
    
    def __post_init__(self):
        self.event_type = FlowEventType.MANUAL_CLOSE
