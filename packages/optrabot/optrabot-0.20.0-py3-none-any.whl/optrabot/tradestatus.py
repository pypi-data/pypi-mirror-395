"""
Trade Status Constants

This module defines constants for the different trade statuses.
Separated into its own file to avoid circular imports.
"""

class TradeStatus:
	"""Trade status constants"""
	NEW = 'NEW'
	OPEN = 'OPEN'
	CLOSED = 'CLOSED'
	EXPIRED = 'EXPIRED'
