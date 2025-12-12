from sqlalchemy import (TIMESTAMP, Boolean, Column, Date, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship

from .database import Base
from .tradestatus import TradeStatus


class Account(Base):
	__tablename__ = "accounts"

	id = Column(String, primary_key=True)
	name = Column(String)
	broker = Column(String)
	pdt = Column(Boolean, default=False)

class Trade(Base):
	__tablename__ = "trades"

	id = Column(Integer, primary_key=True, autoincrement=True)
	trade_group_id = Column(String, nullable=True)  # Groups related trades (e.g., rollover chains)
	template_name = Column(String, nullable=True)  # OTB-253: Template name for trade recovery
	account = Column(String, ForeignKey('accounts.id'))
	symbol = Column(String)
	strategy = Column(String)
	status = Column(String, default=TradeStatus.NEW) # Status: NEW, OPEN, CLOSED, or EXPIRED
	openDate = Column(TIMESTAMP, nullable=True)  # When the trade was opened (entry order filled)
	closeDate = Column(TIMESTAMP, nullable=True)  # When the trade was closed
	realizedPNL = Column(Float, default=0.0)
	transactions = relationship("Transaction", back_populates="trade")

	def __str__(self) -> str:
		""" Returns a string representation of the Trade
		"""
		tradeString = ('ID: ' + str(self.id) + ' Account: ' + self.account + ' Strategy: ' + self.strategy + ' Symbol: ' + str(self.status) + ' RealizedPNL: ' + str(self.realizedPNL))
		return tradeString

class Transaction(Base):
	__tablename__ = 'transactions'

	tradeid = Column(Integer, ForeignKey('trades.id'), primary_key=True)
	id = Column(Integer, primary_key=True)
	type = Column(String) # SELL,BUY,EXP
	sectype = Column(String) # C, P, S
	timestamp = Column(TIMESTAMP, ) # Timestamp of transaction in UTC
	expiration = Column(Date)
	strike = Column(Float)
	contracts = Column(Integer, default=1)
	price = Column(Float, default=0)
	fee = Column(Float, default=0)
	commission = Column(Float, default=0)
	notes = Column(String, default='')
	exec_id = Column(String, nullable=True, default='')  # Execution ID from broker

	trade = relationship("Trade", back_populates="transactions")


class Setting(Base):
	"""
	Key-Value store for application settings and flags.
	
	Can be used for:
	- One-time migration flags (e.g., 'pnl_correction_done')
	- UI preferences (e.g., 'ui_theme', 'ui_language')
	- Feature flags (e.g., 'feature_x_enabled')
	- System state (e.g., 'last_maintenance_date')
	"""
	__tablename__ = 'settings'

	key = Column(String, primary_key=True)  # Setting name/identifier
	value = Column(String, nullable=True)   # Setting value (stored as string, parse as needed)
	description = Column(String, nullable=True)  # Optional description of the setting
	updated_at = Column(TIMESTAMP, nullable=True)  # When this setting was last updated

	def __str__(self) -> str:
		return f"Setting({self.key}={self.value})"

