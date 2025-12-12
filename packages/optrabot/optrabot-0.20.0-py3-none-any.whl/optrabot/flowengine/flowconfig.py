"""
Flow Configuration Data Classes

This module defines the data structures for flow configurations
loaded from the config.yaml file.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from .flowevent import FlowEventType


class FlowActionType(str, Enum):
    """Enumeration of available flow action types"""
    SEND_NOTIFICATION = "send_notification"
    PROCESS_TEMPLATE = "process_template"


@dataclass
class FlowEventConfig:
    """Configuration for a flow event trigger"""
    type: FlowEventType
    template: str  # Required: Template name that must trigger this flow


@dataclass
class SendNotificationAction:
    """Configuration for send_notification action"""
    message: str
    type: str = "INFO"  # Default notification type


@dataclass
class ProcessTemplateAction:
    """Configuration for process_template action"""
    template: str
    amount: Any  # Can be int or expression string
    premium: Any  # Can be float or expression string
    expiration: Any = None  # Optional: Can be date or expression string
    time: datetime = None  # Optional: Parsed datetime with timezone (e.g. from "15:00 EST")


@dataclass
class FlowAction:
    """Wrapper for flow actions"""
    action_type: FlowActionType
    action_config: Any  # SendNotificationAction or ProcessTemplateAction


@dataclass
class Flow:
    """Configuration for a complete flow"""
    id: str
    name: Optional[str] = None
    enabled: bool = True
    event: Optional[FlowEventConfig] = None
    actions: List[FlowAction] = field(default_factory=list)
    
    def get_display_name(self) -> str:
        """Returns the flow name or ID if name is not set"""
        return self.name if self.name else self.id
