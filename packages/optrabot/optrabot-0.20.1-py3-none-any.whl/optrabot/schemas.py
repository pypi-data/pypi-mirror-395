from datetime import date, datetime

from pydantic import BaseModel


class AccountBase(BaseModel):
	id: str
	name: str
	broker: str
	pdt: bool

class AccountCreate(AccountBase):
	pass

class Account(AccountBase):
	class Config:
		from_attributes = True

class TransactionBase(BaseModel):
	tradeid: int
	id: int
	type: str
	sectype: str
	timestamp: datetime
	expiration: date
	strike: float
	contracts: int
	price: float
	fee: float
	commission: float
	notes: str
	exec_id: str

class TransactionCreate(TransactionBase):
	pass

class Transaction(TransactionBase):
	class Config:
		from_attributes = True

class TradeBase(BaseModel):
	account: str
	symbol: str
	strategy: str
	template_name: str | None = None  # OTB-253: Optional for backward compatibility

class TradeCreate(TradeBase):
	pass

class Trade(TradeBase):
	id: int
	status: str
	realizedPNL: float
	status: str 
	transactions: list[Transaction] = []

	class Config:
		from_attributes = True