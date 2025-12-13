"""
API endpoint for frontend status polling
"""
from typing import List, Optional

from fastapi import APIRouter, Request
from loguru import logger
from pydantic import BaseModel

router = APIRouter()


class BrokerStatus(BaseModel):
    id: str
    name: str
    connected: bool
    accounts: List[str] = []  # Account IDs managed by this broker


class StatusResponse(BaseModel):
    status: str = 'ok'
    version: str
    instanceId: Optional[str] = None
    instanceName: Optional[str] = None  # Display name for the instance
    hubConnected: bool = False
    brokers: List[BrokerStatus] = []
    connectedAccounts: List[str] = []  # All connected account IDs (for easy filtering)
    # Computed fields for backward compatibility
    brokerConnected: bool = False  # True if ALL brokers connected
    brokerPartial: bool = False    # True if SOME but not all connected


@router.get('/status', response_model=StatusResponse)
async def get_status(request: Request) -> StatusResponse:
    """
    Get the current status of the OptraBot instance.
    Used by the frontend to poll connection status.
    """
    from optrabot.broker.brokerfactory import BrokerFactory
    from optrabot.optrabot import get_version
    
    optrabot = request.app.optraBot
    
    # Check hub connection status
    hub_connected = False
    if hasattr(optrabot, 'thc') and optrabot.thc:
        hub_connected = optrabot.thc.isHubConnectionOK()
    
    # Check broker connection status
    broker_factory = BrokerFactory()
    connectors = broker_factory.get_broker_connectors()
    
    brokers: List[BrokerStatus] = []
    connected_count = 0
    all_connected_accounts: List[str] = []
    
    if connectors:
        for connector_id, connector in connectors.items():
            is_conn = connector.isConnected() or False  # Ensure boolean even if isConnected() returns None
            account_ids: List[str] = []
            
            if is_conn:
                connected_count += 1
                # Get accounts for connected brokers
                try:
                    accounts = connector.getAccounts()
                    account_ids = [acc.id for acc in accounts]
                    all_connected_accounts.extend(account_ids)
                except Exception as e:
                    logger.warning(f'Failed to get accounts for broker {connector_id}: {e}')
            
            brokers.append(BrokerStatus(
                id=connector_id,
                name=type(connector).__name__,
                connected=is_conn,
                accounts=account_ids
            ))
    
    total_brokers = len(brokers)
    all_connected = total_brokers > 0 and connected_count == total_brokers
    partial_connected = connected_count > 0 and connected_count < total_brokers
    
    # Get instance ID and name from config
    instance_id = None
    instance_name = None
    if hasattr(optrabot, 'config') and optrabot.config:
        instance_id = optrabot.config.getInstanceId()
        # Use instance ID as display name if it differs from default
        if instance_id and instance_id.lower() != 'optrabot':
            instance_name = instance_id
    
    return StatusResponse(
        status='ok',
        version=get_version(),
        instanceId=instance_id,
        instanceName=instance_name,
        hubConnected=hub_connected,
        brokers=brokers,
        connectedAccounts=all_connected_accounts,
        brokerConnected=all_connected,
        brokerPartial=partial_connected
    )
