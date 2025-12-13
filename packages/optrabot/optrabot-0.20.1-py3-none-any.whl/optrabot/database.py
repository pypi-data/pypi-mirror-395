import inspect
import os
from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from loguru import logger

from optrabot.config import Config
from optrabot.tradestatus import TradeStatus

SQLALCHEMY_DATABASE_URL = "sqlite:///./optrabot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def updateDatabase():
	logger.debug('Enter updateDatabase()')
	packageDirectory = os.path.dirname(inspect.getfile(Config))
	alembicConfigFile = packageDirectory + os.sep + 'alembic.ini'
	logger.debug('Package directory: {}  -> Alembic config: {}', packageDirectory, alembicConfigFile)
	scriptLocation = packageDirectory + os.sep + 'alembic'
	alembic_config = AlembicConfig(alembicConfigFile)
	alembic_config.set_main_option('script_location', scriptLocation)
	command.upgrade(alembic_config, "head")
	
	# One-time data corrections
	_run_data_corrections()

def _run_data_corrections():
	"""
	Runs one-time data correction tasks.
	Each correction checks a flag in the settings table to ensure it only runs once.
	"""
	from optrabot import crud, models
	from optrabot.tradehelper import TradeHelper
	from sqlalchemy import select
	
	with SessionLocal() as session:
		# Correction 1: Fix PNL for EXPIRED trades
		correction_flag = 'pnl_correction_expired_trades_done'
		if not crud.get_setting_value(session, correction_flag):
			logger.debug('Running one-time correction: Fixing PNL for EXPIRED trades...')
			
			# Get all EXPIRED trades
			statement = select(models.Trade).where(models.Trade.status == TradeStatus.EXPIRED)
			expired_trades = session.scalars(statement).all()
			
			corrected_count = 0
			for trade in expired_trades:
				if len(trade.transactions) > 0:
					old_pnl = trade.realizedPNL
					TradeHelper.updateTrade(trade, session)
					
					if old_pnl != trade.realizedPNL:
						corrected_count += 1
						logger.debug(f'Trade {trade.id}: PNL corrected from {old_pnl} to {trade.realizedPNL}')
				
					crud.update_trade(session, trade)
			
			# Set the flag to prevent running again
			crud.set_setting(
				session, 
				correction_flag, 
				'true', 
				f'PNL correction completed. Corrected {corrected_count} EXPIRED trades.'
			)
			logger.debug(f'PNL correction completed for EXPIRED trades. Corrected {corrected_count} trades.')
		else:
			logger.debug(f'PNL correction for EXPIRED trades already done (flag: {correction_flag})')
		
		# Correction 2: Fix PNL for all trades (multiplier bug fix)
		correction_flag_2 = 'pnl_correction_multiplier_fix_done'
		if not crud.get_setting_value(session, correction_flag_2):
			logger.debug('Running one-time correction: Fixing PNL with correct multiplier for all trades...')
			
			# Get all trades with transactions
			statement = select(models.Trade)
			all_trades = session.scalars(statement).all()
			
			corrected_count = 0
			for trade in all_trades:
				if len(trade.transactions) > 0:
					old_pnl = trade.realizedPNL
					old_status = trade.status
					TradeHelper.updateTrade(trade, session)
					
					if old_pnl != trade.realizedPNL:
						corrected_count += 1
						logger.debug(f'Trade {trade.id}: PNL corrected from {old_pnl} to {trade.realizedPNL}')
				
					crud.update_trade(session, trade)
			
			# Set the flag to prevent running again
			crud.set_setting(
				session, 
				correction_flag_2, 
				'true', 
				f'PNL multiplier correction completed. Corrected {corrected_count} trades.'
			)
			logger.debug(f'PNL multiplier correction completed. Corrected {corrected_count} trades.')
		else:
			logger.debug(f'PNL multiplier correction already done (flag: {correction_flag_2})')




def get_db_engine():
	return engine
