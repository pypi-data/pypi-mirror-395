"""
OTB-258: NTP Time Synchronization Module

This module checks the system time against NTP servers to detect clock drift.
If the time difference exceeds 30 seconds, it sends a warning via Telegram.

The time check is scheduled to run:
- Once at startup
- Once daily at 6:00 AM Eastern Time
"""

import ntplib
from datetime import datetime, timezone
from typing import Optional, Tuple
from loguru import logger

from optrabot.tradinghubclient import TradinghubClient


class TimeSync:
    """
    Manages time synchronization monitoring with NTP servers.
    
    This class provides functionality to:
    - Query NTP servers for accurate time
    - Compare system time with NTP time
    - Send warnings via Telegram if drift exceeds threshold
    """
    
    # NTP servers in order of preference
    NTP_SERVERS = [
        'pool.ntp.org',       # Global NTP pool
        'time.google.com',    # Google's NTP server
        'time.apple.com'      # Apple's NTP server
    ]
    
    # Maximum allowed time difference in seconds
    MAX_DRIFT_SECONDS = 10
    
    def __init__(self, trading_hub_client: TradinghubClient =None):
        """
        Initialize TimeSync.
        
        Args:
            trading_hub_client: Optional TradingHubClient instance for sending alerts
        """
        self.trading_hub_client = trading_hub_client
        self.ntp_client = ntplib.NTPClient()
    
    @staticmethod
    def format_time_drift(seconds: float) -> str:
        """
        Format time drift in human-readable format.
        
        Automatically chooses the appropriate unit:
        - < 60s: seconds
        - < 3600s: minutes and seconds
        - < 86400s: hours and minutes
        - >= 86400s: days and hours
        
        Args:
            seconds: Time drift in seconds
            
        Returns:
            Formatted string (e.g., "45s", "2m 30s", "1h 15m", "2d 3h")
        """
        abs_seconds = abs(seconds)
        
        if abs_seconds < 60:
            return f"{abs_seconds:.1f}s"
        
        if abs_seconds < 3600:
            minutes = int(abs_seconds // 60)
            remaining_seconds = int(abs_seconds % 60)
            return f"{minutes}m {remaining_seconds}s"
        
        if abs_seconds < 86400:
            hours = int(abs_seconds // 3600)
            remaining_minutes = int((abs_seconds % 3600) // 60)
            return f"{hours}h {remaining_minutes}m"
        
        # >= 1 day
        days = int(abs_seconds // 86400)
        remaining_hours = int((abs_seconds % 86400) // 3600)
        return f"{days}d {remaining_hours}h"
    
    def get_ntp_time(self) -> Optional[datetime]:
        """
        Query NTP servers to get accurate current time.
        
        Tries multiple NTP servers in order until one responds.
        
        Returns:
            datetime: Current time from NTP server (UTC timezone-aware)
            None: If all NTP servers fail
        """
        for server in self.NTP_SERVERS:
            try:
                logger.debug(f"Querying NTP server: {server}")
                response = self.ntp_client.request(server, version=3, timeout=5)
                ntp_time = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
                logger.debug(f"NTP time from {server}: {ntp_time}")
                return ntp_time
            except Exception as e:
                logger.warning(f"Failed to get time from {server}: {e}")
                continue
        
        logger.error("All NTP servers failed")
        return None
    
    def get_system_time(self) -> datetime:
        """
        Get current system time.
        
        Returns:
            datetime: Current system time (UTC timezone-aware)
        """
        return datetime.now(timezone.utc)
    
    def calculate_time_drift(self) -> Optional[Tuple[float, datetime, datetime]]:
        """
        Calculate the time difference between system time and NTP time.
        
        Returns:
            Tuple[float, datetime, datetime]: (drift_seconds, system_time, ntp_time)
            None: If NTP time cannot be retrieved
        """
        ntp_time = self.get_ntp_time()
        if ntp_time is None:
            return None
        
        system_time = self.get_system_time()
        drift = (system_time - ntp_time).total_seconds()
        
        logger.debug(f"Time drift: {drift:.2f} seconds")
        logger.debug(f"System time: {system_time}")
        logger.debug(f"NTP time: {ntp_time}")
        
        return drift, system_time, ntp_time

    async def send_warning_notification(self, drift: float, system_time: datetime, ntp_time: datetime):
        """
        Send a warning about time drift.

        Args:
            drift: Time difference in seconds
            system_time: Current system time
            ntp_time: Correct NTP time
        """
        if self.trading_hub_client is None:
            logger.warning("Cannot send notification- no client configured")
            return
        
        try:
            from optrabot.tradinghubclient import NotificationType
            
            drift_formatted = self.format_time_drift(drift)
            
            message = (
                f"⚠️ TIME SYNC WARNING ⚠️\n\n"
                f"System time is off by {drift_formatted}.\n\n"
                f"System time: {system_time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
                f"NTP time: {ntp_time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
                f"Please check and adjust system time manually."
            )

            await self.trading_hub_client.send_notification(NotificationType.WARN, message)
            logger.debug("Telegram warning sent")
            
        except Exception as e:
            logger.error(f"Failed to send Telegram warning: {e}")
    
    async def check_and_sync_time(self):
        """
        Main time synchronization check.
        
        This method:
        1. Queries NTP servers for accurate time
        2. Calculates time drift
        3. Sends Telegram warning if drift > threshold
        
        This is the method called by APScheduler.
        """
        NUM_OF_CHARS = 70
        logger.debug("=" * NUM_OF_CHARS)
        logger.debug("Starting time synchronization check")
        logger.debug("=" * NUM_OF_CHARS)

        # Get time drift
        result = self.calculate_time_drift()
        if result is None:
            logger.error("Cannot check time drift - NTP servers unavailable")
            return
        
        drift, system_time, ntp_time = result
        
        # Check if drift exceeds threshold
        if abs(drift) <= self.MAX_DRIFT_SECONDS:
            drift_formatted = self.format_time_drift(drift)
            logger.info(f"✅ Time drift within acceptable range: {drift_formatted} (max: {self.MAX_DRIFT_SECONDS}s)")
            return
        
        # Drift exceeds threshold - send warning
        drift_formatted = self.format_time_drift(drift)
        logger.warning(
            f"⚠️ Time drift exceeds threshold: {drift_formatted} "
            f"(max: {self.MAX_DRIFT_SECONDS}s)"
        )

        # Send warning notification
        await self.send_warning_notification(drift, system_time, ntp_time)

        logger.debug("=" * NUM_OF_CHARS)
        logger.debug("Time synchronization check completed")
        logger.debug("=" * NUM_OF_CHARS)
