"""
Flow Engine Implementation

The FlowEngine is responsible for managing and executing flows based on
trading events.
"""

import asyncio
import copy
from typing import Any, Dict, List, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from eventkit import Event
from loguru import logger
from simpleeval import simple_eval

from optrabot.tradetemplate.templatetrigger import TemplateTrigger
from optrabot.util.common import Common
from optrabot.util.singletonmeta import SingletonMeta

from .flowconfig import (Flow, FlowAction, FlowActionType,
                         ProcessTemplateAction, SendNotificationAction)
from .flowevent import FlowEventData, FlowEventType


class FlowEngine(metaclass=SingletonMeta):
    """
    The Flow Engine manages and executes flows based on trading events.
    It is implemented as a singleton to ensure consistent event handling.
    """
    
    def __init__(self):
        self._flows: List[Flow] = []
        self._scheduler: Optional[AsyncIOScheduler] = None
        
        # Create events for each event type
        self.early_exit_event = Event('early_exit_event')
        self.trade_opened_event = Event('trade_opened_event')
        self.stop_loss_hit_event = Event('stop_loss_hit_event')
        self.take_profit_hit_event = Event('take_profit_hit_event')
        self.manual_close_event = Event('manual_close_event')
        
        # Map event types to event objects
        self._event_map = {
            FlowEventType.EARLY_EXIT: self.early_exit_event,
            FlowEventType.TRADE_OPENED: self.trade_opened_event,
            FlowEventType.STOP_LOSS_HIT: self.stop_loss_hit_event,
            FlowEventType.TAKE_PROFIT_HIT: self.take_profit_hit_event,
            FlowEventType.MANUAL_CLOSE: self.manual_close_event,
        }
        
        logger.debug('FlowEngine initialized')
    
    def initialize(self, flows: List[Flow], scheduler: AsyncIOScheduler):
        """
        Initialize the flow engine with flows from configuration
        
        Args:
            flows: List of flow configurations
            scheduler: Background scheduler for async flow execution
        """
        self._flows = flows
        self._scheduler = scheduler
        
        if len(self._flows) == 0:
            logger.info('No flows configured')
            return
        
        # Connect event handlers
        for flow in self._flows:
            if flow.enabled and flow.event:
                event = self._event_map.get(flow.event.type)
                if event:
                    event.connect(self._create_flow_handler(flow))
                    logger.debug(f'Flow "{flow.get_display_name()}" registered for {flow.event.type} events on template {flow.event.template}')
        
        logger.info(f'FlowEngine initialized with {len(self._flows)} flow(s)')
    
    def _create_flow_handler(self, flow: Flow):
        """
        Creates an event handler function for the given flow
        
        Args:
            flow: Flow configuration
            
        Returns:
            Event handler function
        """
        def handler(event_data: FlowEventData):
            """Handler function that checks template match and schedules flow execution"""
            # Check if the event is from the correct template
            if flow.event.template != event_data.template_name:
                logger.trace(f'Flow "{flow.get_display_name()}" skipped: template mismatch (expected {flow.event.template}, got {event_data.template_name})')
                return
            
            logger.info(f'Flow "{flow.get_display_name()}" triggered by {event_data.event_type} event from trade {event_data.trade_id}')
            
            # Schedule flow execution asynchronously
            if self._scheduler:
                job_id = f'flow_execution_{flow.id}_{event_data.trade_id}'
                self._scheduler.add_job(
                    self._execute_flow,
                    args=[flow, event_data],
                    id=job_id,
                    max_instances=10,
                    misfire_grace_time=None
                )
            else:
                logger.error(f'Cannot execute flow "{flow.get_display_name()}": scheduler not initialized')
        
        return handler
    
    async def _execute_flow(self, flow: Flow, event_data: FlowEventData):
        """
        Execute all actions in a flow sequentially
        
        Args:
            flow: Flow configuration
            event_data: Event data containing variables
        """
        logger.debug(f'Executing flow "{flow.get_display_name()}" for trade {event_data.trade_id}')
        
        # Get variables from event data
        variables = event_data.get_variables()
        
        # Execute actions sequentially
        for action_index, action in enumerate(flow.actions, start=1):
            try:
                await self._execute_action(action, variables, flow)
            except Exception as e:
                error_msg = f'Flow "{flow.get_display_name()}" failed at action {action_index}/{len(flow.actions)} ({action.action_type.value}): {str(e)}'
                logger.error(error_msg)
                
                # Send detailed error notification
                from optrabot.tradinghubclient import (NotificationType,
                                                       TradinghubClient)
                try:
                    # Build message with Markdown formatting
                    # escape_markdown will preserve the Markdown syntax (*bold*) while escaping special chars in variable content
                    # Important: escape the entire message at once so the method can properly detect Markdown syntax
                    notification_msg = Common.escape_markdown(
                        f'❌ *Flow Execution Failed*\n'
                        f'*Flow:* {flow.get_display_name()}\n'
                        f'*Trade ID:* {event_data.trade_id}\n'
                        f'*Action:* {action_index} of {len(flow.actions)} ({action.action_type.value})\n'
                        f'*Error:* {str(e)}'
                    )
                    logger.debug(f'Sending error notification for flow "{flow.get_display_name()}"')
                    await TradinghubClient().send_notification(
                        NotificationType.ERROR,
                        notification_msg
                    )
                    logger.debug(f'Error notification sent successfully for flow "{flow.get_display_name()}"')
                except Exception as notify_error:
                    logger.error(f'Failed to send error notification: {notify_error}', exc_info=True)
                
                # Stop executing remaining actions
                logger.debug(f'Flow "{flow.get_display_name()}" execution aborted due to error')
                return
        
        logger.success(f'Flow "{flow.get_display_name()}" completed successfully')
    
    async def _execute_action(self, action: FlowAction, variables: Dict, flow: Flow):
        """
        Execute a single action
        
        Args:
            action: Action configuration
            variables: Variables available for expression evaluation
            flow: Parent flow (for logging)
        """
        if action.action_type == FlowActionType.SEND_NOTIFICATION:
            await self._execute_send_notification(action.action_config, variables, flow)
        elif action.action_type == FlowActionType.PROCESS_TEMPLATE:
            await self._execute_process_template(action.action_config, variables, flow)
        else:
            raise ValueError(f'Unknown action type: {action.action_type}')
    
    async def _execute_send_notification(self, config: SendNotificationAction, variables: Dict, flow: Flow):
        """
        Execute send_notification action
        
        Args:
            config: Send notification configuration
            variables: Variables for message interpolation
            flow: Parent flow (for logging)
        """
        logger.debug(f'Flow "{flow.get_display_name()}": Executing send_notification action')
        
        # Evaluate message (simple string replacement for now, could use template engine)
        message = config.message
        for var_name, var_value in variables.items():
            placeholder = f'${var_name}'
            message = message.replace(placeholder, str(var_value))
        
        # Determine notification type
        from optrabot.tradinghubclient import (NotificationType,
                                               TradinghubClient)
        
        notification_type_map = {
            'ERROR': NotificationType.ERROR,
            'INFO': NotificationType.INFO,
            'WARN': NotificationType.WARN,
        }
        
        notification_type = notification_type_map.get(config.type.upper(), NotificationType.INFO)
        
        # Send notification
        await TradinghubClient().send_notification(notification_type, message)
        logger.debug(f'Flow "{flow.get_display_name()}": Notification sent')
    
    async def _execute_process_template(self, config: ProcessTemplateAction, variables: Dict, flow: Flow):
        """
        Execute process_template action
        
        Args:
            config: Process template configuration
            variables: Variables for expression evaluation
            flow: Parent flow (for logging)
        """
        # Lazy imports to avoid circular dependencies
        import datetime as dt

        import pytz

        import optrabot.config as optrabotcfg
        from optrabot.signaldata import SignalData
        from optrabot.tradetemplate.processor.templateprocessor import \
            TemplateProcessor
        
        logger.debug(f'Flow "{flow.get_display_name()}": Executing process_template action for template {config.template}')
        
        # Get the template
        conf: optrabotcfg.Config = optrabotcfg.appConfig
        
        template = None
        for tmpl in conf.getTemplates():
            if tmpl.name == config.template:
                template = tmpl
                break
        
        if template is None:
            raise ValueError(f'Template "{config.template}" not found')
        
        if not template.is_enabled():
            logger.warning(f'Flow "{flow.get_display_name()}": Template "{config.template}" is disabled, skipping')
            return
        
        # Evaluate amount expression and round to nearest integer (< 0.5 rounds down, >= 0.5 rounds up)
        amount_value = self._evaluate_expression(config.amount, variables, 'amount')
        if not isinstance(amount_value, (int, float)):
            raise ValueError(f'Invalid amount value: {amount_value} (must be numeric)')
        amount = int(round(amount_value))
        if amount <= 0:
            raise ValueError(f'Invalid amount value: {amount} (must be positive integer)')
        
        # Evaluate premium expression and round to 2 decimal places
        premium = self._evaluate_expression(config.premium, variables, 'premium')
        if not isinstance(premium, (int, float)):
            raise ValueError(f'Invalid premium value: {premium} (must be numeric)')
        premium = round(premium, 2)
        
        # Evaluate expiration expression if provided
        expiration = None
        if config.expiration is not None:
            expiration = self._evaluate_expression(config.expiration, variables, 'expiration')
            # Verify it's a date object
            if not isinstance(expiration, dt.date):
                raise ValueError(f'Invalid expiration value: {expiration} (must be datetime.date)')
        
        logger.info(f'Flow "{flow.get_display_name()}": Processing template {config.template} with amount={amount}, premium={premium}, expiration={expiration}')
        
        # Create a deep copy of the template to avoid modifying the original
        template_copy = copy.deepcopy(template)
        template_copy.amount = amount
        
        # For premium-based templates, set the premium
        if hasattr(template_copy, 'premium'):
            template_copy.premium = premium
        
        # If expiration date is provided, set it explicitly on the template
        # This has priority over the template's dte value
        if expiration is not None:
            logger.debug(f'Flow "{flow.get_display_name()}": Setting explicit expiration date: {expiration}')
            template_copy.set_expiration_date(expiration)

        # Set the trigger type to Flow
        flow_trigger = TemplateTrigger({'type': 'flow', 'value': 'flow_engine'})
        template_copy.setTrigger(flow_trigger)
        
        # Pass trade_group_id from triggering trade to new trade (for rollover grouping)
        if 'EVENT_TRADE_GROUP_ID' in variables and variables['EVENT_TRADE_GROUP_ID']:
            template_copy.trade_group_id = variables['EVENT_TRADE_GROUP_ID']
            logger.info(f'Flow "{flow.get_display_name()}": Propagating Trade Group ID: {template_copy.trade_group_id}')
        
        # Check if time-based scheduling is requested
        if config.time is not None:
            await self._schedule_template_processing(config, template_copy, variables, flow)
            return
        
        # Immediate execution (no time parameter)
        # Create signal data
        signal_data = SignalData(
            timestamp=dt.datetime.now().astimezone(pytz.UTC),
            close=0,
            strike=0
        )
        
        # Process the template
        template_processor = TemplateProcessor()
        try:
            logger.debug(f'Flow "{flow.get_display_name()}": Calling processTemplate with amount={amount}, premium={premium}')
            await template_processor.processTemplate(template_copy, signal_data)
            logger.info(f'Flow "{flow.get_display_name()}": Template processing completed successfully')
        except Exception as template_error:
            error_msg = f'Template processing failed: {str(template_error)}'
            logger.error(f'Flow "{flow.get_display_name()}": {error_msg}', exc_info=True)
            raise ValueError(error_msg) from template_error
        
        logger.debug(f'Flow "{flow.get_display_name()}": Template processing initiated')
    
    async def _schedule_template_processing(self, config: ProcessTemplateAction, template_copy, variables: Dict, flow: Flow):
        """
        Schedule template processing for a specific time
        
        Args:
            config: Process template configuration (config.time is already parsed datetime)
            template_copy: Deep copy of template with updated values
            variables: Variables for notification
            flow: Parent flow (for logging)
        """
        import datetime as dt

        import pytz

        from optrabot.signaldata import SignalData
        from optrabot.tradetemplate.processor.templateprocessor import \
            TemplateProcessor
        
        logger.debug(f'Flow "{flow.get_display_name()}": Processing scheduled time: {config.time}')
        
        # config.time is already a parsed datetime object from config loading
        scheduled_time_parsed = config.time
        
        # Combine with today's date to get full datetime
        now = dt.datetime.now().astimezone(pytz.UTC)
        scheduled_datetime = dt.datetime.combine(
            now.date(), 
            scheduled_time_parsed.time(), 
            tzinfo=scheduled_time_parsed.tzinfo
        )
        
        # If the scheduled time is in the past, execute immediately
        if scheduled_datetime <= now:
            logger.warning(f'Flow "{flow.get_display_name()}": Scheduled time {scheduled_datetime.strftime("%H:%M %Z")} is in the past (current: {now.strftime("%H:%M %Z")}). Executing immediately.')
            
            # Create signal data and execute immediately
            signal_data = SignalData(
                timestamp=dt.datetime.now().astimezone(pytz.UTC),
                close=0,
                strike=0
            )
            
            template_processor = TemplateProcessor()
            try:
                await template_processor.processTemplate(template_copy, signal_data)
                logger.info(f'Flow "{flow.get_display_name()}": Template processing completed successfully (immediate execution due to past time)')
            except Exception as template_error:
                error_msg = f'Template processing failed: {str(template_error)}'
                logger.error(f'Flow "{flow.get_display_name()}": {error_msg}', exc_info=True)
                raise ValueError(error_msg) from template_error
            
            return  # Exit early, no scheduling needed
        
        # Create the job ID
        import time
        job_id = f'flow_{flow.id}_processtemplate_{int(time.time() * 1000)}'
        
        # Create signal data (will be used when job executes)
        signal_data = SignalData(
            timestamp=dt.datetime.now().astimezone(pytz.UTC),
            close=0,
            strike=0
        )
        
        # Schedule the job
        template_processor = TemplateProcessor()
        self._scheduler.add_job(
            template_processor.processTemplate,
            'date',
            run_date=scheduled_datetime,
            timezone=scheduled_time_parsed.tzinfo,
            args=[template_copy, signal_data],
            id=job_id,
            misfire_grace_time=None
        )
        
        logger.info(f'Flow "{flow.get_display_name()}": Scheduled template "{config.template}" for {scheduled_datetime.strftime("%Y-%m-%d %H:%M %Z")}')
        
        # Send success notification
        from optrabot.tradinghubclient import TradinghubClient

        # Build notification message
        notification_msg = (
            f'✅ Template Processing Scheduled\n\n'
            f'Flow: {flow.get_display_name()}\n'
            f'Template: {config.template}\n'
            f'Amount: {template_copy.amount}\n'
        )
        
        # Add premium line only if template has premium attribute set
        if hasattr(template_copy, 'premium') and template_copy.premium is not None:
            notification_msg += f'Premium: ${template_copy.premium:.2f}\n'
        
        notification_msg += f'Scheduled at: {scheduled_datetime.strftime("%H:%M %Z")}'
        
        await TradinghubClient().send_notification('INFO', notification_msg)

    def _evaluate_expression(self, expression: Any, variables: Dict, field_name: str) -> Any:
        """
        Evaluate an expression with the given variables
        
        Args:
            expression: Expression to evaluate (can be a value or string expression)
            variables: Variables available for evaluation
            field_name: Field name for error messages
            
        Returns:
            Evaluated value
        """
        # If it's not a string, return as-is (it's already a value)
        if not isinstance(expression, str):
            return expression
        
        # Check if it contains a variable reference
        if '$' not in expression:
            # Try to convert to number if possible
            try:
                if '.' in expression:
                    return float(expression)
                else:
                    return int(expression)
            except ValueError:
                return expression
        
        # Replace variable placeholders with underscore notation for simpleeval
        eval_expression = expression
        for var_name in variables.keys():
            placeholder = f'${var_name}'
            eval_expression = eval_expression.replace(placeholder, var_name)
        
        try:
            # Add commonly used functions to simpleeval
            functions = {
                'abs': abs,
                'min': min,
                'max': max,
                'round': round,
            }
            result = simple_eval(eval_expression, names=variables, functions=functions)
            logger.trace(f'Expression "{expression}" evaluated to: {result}')
            return result
        except Exception as e:
            raise ValueError(f'Failed to evaluate {field_name} expression "{expression}": {str(e)}')
    
    def emit_event(self, event_data: FlowEventData):
        """
        Emit an event to trigger matching flows
        
        Args:
            event_data: Event data to emit
        """
        event = self._event_map.get(event_data.event_type)
        if event:
            logger.debug(f'Emitting {event_data.event_type} event for trade {event_data.trade_id}')
            event.emit(event_data)
        else:
            logger.warning(f'Unknown event type: {event_data.event_type}')
    
    def shutdown(self):
        """Shutdown the flow engine"""
        logger.debug('Shutting down FlowEngine')
        
        # Clear all event handlers by clearing the event slots
        # eventkit stores handlers in _list attribute
        for event in self._event_map.values():
            if hasattr(event, '_list'):
                event._list.clear()
        
        self._flows = []
        self._scheduler = None
        
        logger.debug('FlowEngine shutdown completed')
