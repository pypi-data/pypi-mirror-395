from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas


#########################################
#### Acount							 ####
#########################################
def create_account(session: Session, account: schemas.AccountCreate) -> models.Account:
	""" Create a new account in the database
	"""
	db_account = models.Account(id=account.id, name=account.name, broker=account.broker, pdt=account.pdt)
	session.add(db_account)
	session.commit()
	return db_account

def update_account(session: Session, account: models.Account) -> models.Account:
	""" Updates the account in the database
	"""
	session.merge(account)
	session.commit()
	return account

def get_account(session: Session, id: str) -> models.Account:
	""" Fetches the data of the given account based on the ID.
	"""
	statement = select(models.Account).filter_by(id=id)
	account = session.scalars(statement).first()
	return account

def get_accounts(session: Session, skip: int = 0, limit: int = 100):
	stmnt = select(models.Account)
	accounts = session.scalars(stmnt).all()
	
	return accounts

#########################################
#### Trade							 ####
#########################################
def create_trade(session: Session, newTrade: schemas.TradeCreate) -> models.Trade:
	""" Create a new trade in the database
	"""
	dbTrade = models.Trade(
		account=newTrade.account, 
		symbol=newTrade.symbol, 
		strategy=newTrade.strategy,
		template_name=newTrade.template_name  # OTB-253: Store template name for recovery
	)
	session.add(dbTrade)
	session.commit()
	session.flush()
	logger.debug('Created new trade: {}', dbTrade)
	return dbTrade

def getTrade(session: Session, tradeId: int) -> models.Trade:
	""" Get a trade by it's id
	"""
	return session.get(models.Trade, tradeId)

def update_trade(session: Session, trade: models.Trade) -> models.Trade:
	""" Updates the trade in the database
	"""
	session.merge(trade)
	session.commit()
	session.flush()
	logger.debug('Updated trade: {}', trade)
	return trade

def delete_trade(session: Session, deleteTrade: models.Trade):
	""" Deletes the trade from the database
	"""
	session.delete(deleteTrade)
	session.commit()
	session.flush()
	logger.debug('Deleted trade: {}', deleteTrade)
	return

#########################################
#### Transaction					 ####
#########################################
def getMaxTransactionId(session: Session, tradeId: int) -> int:
	statement = select(func.max(models.Transaction.id)).filter_by(tradeid=tradeId)
	maxId = session.scalar(statement)
	if maxId == None:
		maxId = 0
	return maxId

def getTransactionById(session: Session, tradeId: int, transactionId: int) -> models.Transaction:
	""" Fetches the transaction based on the Trade ID and Transaction ID
	"""
	statement = select(models.Transaction).filter_by(tradeid=tradeId, id=transactionId)
	transaction = session.scalars(statement).first()
	return transaction

def get_transaction_by_execution_id(session: Session, trade_id: int, execution_id: str) -> models.Transaction:
	""" Fetches the transaction based on the execution ID
	"""
	statement = select(models.Transaction).filter_by(tradeid=trade_id, exec_id=execution_id)
	transaction = session.scalars(statement).first()
	return transaction

def createTransaction(session: Session, newTransaction: schemas.TransactionCreate) -> models.Transaction:
	""" Creates a new transaction record for the given trade
	"""
	db_transaction = models.Transaction(tradeid=newTransaction.tradeid, id=newTransaction.id,
									type=newTransaction.type,
									sectype=newTransaction.sectype,
									timestamp=newTransaction.timestamp,
									expiration=newTransaction.expiration,
									strike=newTransaction.strike,
									contracts=newTransaction.contracts,
									price=newTransaction.price,
									fee=newTransaction.fee,
									commission=newTransaction.commission,
									notes=newTransaction.notes,
									exec_id=newTransaction.exec_id)
	session.add(db_transaction)
	session.commit()
	return db_transaction


#########################################
#### Settings						 ####
#########################################
def get_setting(session: Session, key: str) -> models.Setting:
	"""Get a setting by its key"""
	statement = select(models.Setting).filter_by(key=key)
	return session.scalars(statement).first()

def get_setting_value(session: Session, key: str, default: str = None) -> str:
	"""Get a setting value by its key, return default if not found"""
	setting = get_setting(session, key)
	return setting.value if setting else default

def set_setting(session: Session, key: str, value: str, description: str = None) -> models.Setting:
	"""Set a setting value (create or update)"""
	from datetime import datetime

	import pytz
	
	setting = get_setting(session, key)
	if setting:
		setting.value = value
		setting.updated_at = datetime.now(pytz.UTC)
		if description:
			setting.description = description
	else:
		setting = models.Setting(
			key=key,
			value=value,
			description=description,
			updated_at=datetime.now(pytz.UTC)
		)
		session.add(setting)
	
	session.commit()
	return setting

def delete_setting(session: Session, key: str) -> bool:
	"""Delete a setting by its key"""
	setting = get_setting(session, key)
	if setting:
		session.delete(setting)
		session.commit()
		return True
	return False
