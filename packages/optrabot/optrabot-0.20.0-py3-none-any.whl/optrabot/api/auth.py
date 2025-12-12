from fastapi import APIRouter
from loguru import logger

router = APIRouter(prefix='/auth')
@router.get('/tasty_callback')
async def auth_tasty_callback(code: str) -> None:
    # Handle the callback from Tastytrade authentication
    logger.debug(f'Received Tastytrade auth callback with code: {code}')
