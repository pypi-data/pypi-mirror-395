"""
Flow Engine Module

This module provides the flow engine functionality for automating
actions based on trading events.
"""

from .flowconfig import FlowActionType
from .flowengine import FlowEngine
from .flowevent import (EarlyExitEventData, FlowEventData, FlowEventType,
                        ManualCloseEventData, StopLossHitEventData,
                        TakeProfitHitEventData, TradeOpenedEventData)

__all__ = [
    'FlowEngine',
    'FlowActionType',
    'FlowEventType',
    'FlowEventData',
    'TradeOpenedEventData',
    'EarlyExitEventData',
    'StopLossHitEventData',
    'TakeProfitHitEventData',
    'ManualCloseEventData'
]
