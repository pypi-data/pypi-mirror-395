import array
import asyncio
import datetime as dt
import json
import logging
import webbrowser
from collections import OrderedDict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import SchedulerNotRunningError
from fastapi import FastAPI
from ib_async import *
from loguru import logger
from sqlalchemy.orm import Session

import optrabot.config as optrabotcfg
import optrabot.symbolinfo as symbolInfo
from optrabot import schemas
from optrabot.broker.brokerconnector import BrokerConnector
from optrabot.broker.brokerfactory import BrokerFactory
from optrabot.marketdatatype import MarketDataType
from optrabot.optionhelper import OptionHelper
from optrabot.signaldata import SignalData
from optrabot.trademanager import TradeManager
from optrabot.tradetemplate.processor.templateprocessor import \
    TemplateProcessor
from optrabot.tradetemplate.templatefactory import Template
from optrabot.tradetemplate.templatetrigger import TriggerType

from . import crud
from .database import *
from .timesync import TimeSync
from .tradinghubclient import TradinghubClient


def _get_version_from_pyproject() -> str:
	"""Read version from pyproject.toml for DEV mode"""
	try:
		pyproject_path = Path(__file__).parent.parent / 'pyproject.toml'
		if pyproject_path.exists():
			content = pyproject_path.read_text()
			for line in content.splitlines():
				if line.startswith('version'):
					# Extract version from: version = "x.y.z"
					return line.split('=')[1].strip().strip('"\'')
	except Exception:  # noqa: S110
		pass  # Return fallback version below
	return 'unknown-dev'


def get_version() -> str:
	"""
	Returns the version of the package
	"""
	environment = os.environ.get('OPTRABOT_ENV', 'PROD')
	if environment != 'DEV':
		try:
			return version('optrabot')
		except PackageNotFoundError:
			return _get_version_from_pyproject()
	else:
		return _get_version_from_pyproject()

class OptraBot():
	def __init__(self, app: FastAPI):
		self.app = app
		self._apiKey = None
		self.thc : TradinghubClient = None
		self._marketDataType : MarketDataType = None
		self.Version = get_version()
		self._backgroundScheduler = AsyncIOScheduler()
		self._backgroundScheduler.start()
		self._timeSync : TimeSync = None
		self._shutdown_complete = False  # Flag to prevent double shutdown
			
	def __setitem__(self, key, value):
		setattr(self, key, value)

	def __getitem__(self, key):
		return getattr(self, key)
	
	async def startup(self):
		logger.info('OptraBot {version}', version=self.Version)
		# Read Config
		conf = optrabotcfg.Config("config.yaml")
		optrabotcfg.appConfig = conf
		self['config'] = conf
		conf.logConfigurationData()
		conf.readTemplates()
		conf.readFlows()
		updateDatabase()
		self.thc = TradinghubClient(self)
		if self.thc._apiKey == None:
			return

		try:
			additional_data = {
				'instance_id': conf.getInstanceId(),
				'accounts': self._getConfiguredAccounts()
			}
			await self.thc.connect(additional_data)
		except Exception as excp:
			logger.error('Problem on Startup: {}', excp)
			logger.error('OptraBot halted!')
			return
		
		logger.info('Sucessfully connected to OptraBot Hub')
		
		# OTB-253: createBrokerConnectors() now handles Trade Recovery
		# Trade Recovery runs after first broker connection (see BrokerFactory._onBrokerConnected)
		await BrokerFactory().createBrokerConnectors()
		
		self.thc.start_polling(self._backgroundScheduler)
		TradeManager()

		# Initialize FlowEngine
		from optrabot.flowengine import FlowEngine
		flow_engine = FlowEngine()
		flow_engine.initialize(conf.getFlows(), self._backgroundScheduler)

		self._backgroundScheduler.add_job(self._statusInfo, 'interval', minutes=5, id='statusInfo', misfire_grace_time=None)
		# (Tastytrade DXLink streamer closes the connection at midnight for session reset)
		self._backgroundScheduler.add_job(self._new_day_start, 'cron', hour=0, minute=0, second=10, timezone=pytz.timezone('US/Eastern'), id='day_change', misfire_grace_time=None)
		self._backgroundScheduler.add_job(self._check_price_data, 'interval', seconds=30, id='check_price_data', misfire_grace_time=None)
		
		# OTB-258: Initialize time synchronization
		self._timeSync = TimeSync(self.thc)
		# Run immediately at startup
		self._backgroundScheduler.add_job(
			self._timeSync.check_and_sync_time,
			'date',
			run_date=dt.datetime.now() + dt.timedelta(seconds=5),
			id='time_sync_startup',
			misfire_grace_time=None
		)
		# Run daily at 6:00 AM Eastern Time
		self._backgroundScheduler.add_job(
			self._timeSync.check_and_sync_time,
			'cron',
			hour=6,
			minute=0,
			second=0,
			timezone=pytz.timezone('US/Eastern'),
			id='time_sync_daily',
			misfire_grace_time=None
		)
		
		self._scheduleTimeTriggers()

		environment = os.environ.get('OPTRABOT_ENV', 'PROD')
		if environment == 'DEV':
			logger.warning('Run the UI by command: npm start')
		else:
			webPort = conf.get('general.port')
			url = f"http://localhost:{webPort}/ui/"
			self._backgroundScheduler.add_job(self._open_browser, 'date', run_date=dt.datetime.now() + dt.timedelta(seconds=2), args=[url], id='open_browser', misfire_grace_time=None)
	
	async def _open_browser(self, url: str):
		"""
		Opens the default web browser to the specified URL
		"""
		try:
			webbrowser.open(url)
		except Exception as e:
			logger.warning(f'Error opening web browser: {e}')

	async def shutdown(self):
		# Prevent double shutdown (can happen when API endpoint triggers shutdown
		# and then lifespan event also calls shutdown)
		if self._shutdown_complete:
			logger.debug('OptraBot shutdown already completed, skipping')
			return
		
		logger.info('Shutting down OptraBot')
		
		# Shutdown Background Scheduler FIRST to stop all running jobs
		# This prevents jobs from running while other components are shutting down
		try:
			if hasattr(self, '_backgroundScheduler') and self._backgroundScheduler is not None:
				try:
					if hasattr(self._backgroundScheduler, 'running') and self._backgroundScheduler.running:
						self._backgroundScheduler.shutdown(wait=False)
						logger.debug('OptraBot background scheduler shutdown completed')
					else:
						logger.debug('OptraBot background scheduler is not running, skipping shutdown')
				except SchedulerNotRunningError:
					logger.debug('OptraBot background scheduler already stopped')
				except Exception as e:
					logger.warning(f'Error shutting down OptraBot background scheduler: {e}')
		except Exception as e:
			logger.warning(f'Error during OptraBot background scheduler shutdown: {e}')
		
		# Shutdown FlowEngine
		try:
			from optrabot.flowengine import FlowEngine
			FlowEngine().shutdown()
		except Exception as e:
			logger.warning(f'Error shutting down FlowEngine: {e}')
		
		# Shutdown TradeManager first (cancels pending entry orders and sends notifications)
		# Must be before BrokerFactory shutdown to allow order cancellations
		# Must be before TradinghubClient shutdown to allow notifications to be sent
		try:
			await TradeManager().shutdown()
		except Exception as e:
			logger.warning(f'Error shutting down TradeManager: {e}')
		
		# Shutdown BrokerFactory (disconnect from brokers)
		# After TradeManager so pending orders can be cancelled
		# Before TradinghubClient so hub connection stays active for final notifications
		try:
			await BrokerFactory().shutdownBrokerConnectors()
		except Exception as e:
			logger.warning(f'Error shutting down BrokerConnectors: {e}')
		
		# Shutdown TradinghubClient last (disconnect from hub)
		# After all other components so final notifications can still be sent
		try:
			await self.thc.shutdown()
		except Exception as e:
			logger.warning(f'Error shutting down TradinghubClient: {e}')
		
		self._shutdown_complete = True
		logger.info('OptraBot shutdown completed')

	async def _check_price_data(self):
		"""
		Checks if the connected brokers are still delivering price data during the trading session
		"""
		await BrokerFactory().check_price_data()

	async def _new_day_start(self):
		"""
		Perform operations on start of a new day
		"""
		logger.debug('Performing Day Change operations')
		await BrokerFactory().new_day_start()
		self._scheduleTimeTriggers()

	def _statusInfo(self):
		siHubConnection = 'OK' if self.thc.isHubConnectionOK() == True else 'Problem!'

		managedTrades = TradeManager().getManagedTrades()
		activeTrades = 0
		for managedTrade in managedTrades:
			if managedTrade.isActive():
				activeTrades += 1

		status_message, all_enabled = BrokerFactory().get_trading_satus_info()
		if all_enabled:
			logger.info(f'Broker Trading enabled: {status_message}')
		else:
			logger.warning(f'⚠️ Broker Trading enabled: {status_message}')
		logger.info(f'Status Info: Hub Connection: {siHubConnection} - Active Trades: {activeTrades}')

	def _scheduleTimeTriggers(self):
		"""
		Schedules the time triggers for the relevant templates with the time trigger
		"""
		conf: Config = self['config']
		now = dt.datetime.now().astimezone(pytz.UTC)
		for item in conf.getTemplates():
			template : Template = item
			trigger = template.getTrigger()
			if trigger is None:
				continue
			if trigger.type == TriggerType.Time:
				if template.is_enabled() == False:
					logger.debug(f'Template {template.name} is disabled. Not scheduling time trigger.')
					continue
				if trigger._weekdays:
					if now.weekday() not in trigger._weekdays:
						logger.debug(f'Template {template.name} is not scheduled for today')
						continue
				if trigger._blackout_days:
					if now.date() in trigger._blackout_days:
						logger.debug(f'Template {template.name} is in blackout days for today')
						continue
				if not BrokerFactory().is_trading_day():
					logger.debug(f'Market is not open. Not scheduling time trigger for template {template.name}')
					continue
				if trigger._trigger_time.time() < now.time():
					logger.debug(f'Trigger time {trigger._trigger_time} for template {template.name} is in the past. Not scheduling it.')
					continue

				trigger_time_today = dt.datetime.combine(now.date(), trigger._trigger_time.time(), tzinfo=trigger._trigger_time.tzinfo)
				logger.debug(f'Scheduling one-time trigger for template {template.name} at {trigger_time_today}')
				self._backgroundScheduler.add_job(
					self._triggerTemplate,
					'date',
					run_date=trigger_time_today,
					timezone=trigger._trigger_time.tzinfo,
					args=[template],
					id=f'time_trigger_{template.name}',
					misfire_grace_time=None
				)

	async def _triggerTemplate(self, template: Template):
		logger.info(f'Executing Time Trigger for template {template.name}')
		job_id = 'processtemplate' + str(template.name)
		signal_data = SignalData(timestamp=dt.datetime.now().astimezone(pytz.UTC), close=0, strike=0 )
		templateProcessor = TemplateProcessor()
		# Wrap processTemplate call to handle exceptions and send notifications
		self._backgroundScheduler.add_job(
			self._processTemplateWithErrorHandling, 
			args=[templateProcessor, template, signal_data], 
			id=job_id, 
			max_instances=10, 
			misfire_grace_time=None
		)
	
	async def _processTemplateWithErrorHandling(self, templateProcessor, template, signalData):
		"""
		Wrapper for processTemplate that catches exceptions and sends user notifications
		"""
		try:
			await templateProcessor.processTemplate(template, signalData)
		except Exception as e:
			logger.error(f'Template processing failed for {template.name}: {e}')
			from optrabot.tradinghubclient import NotificationType, TradinghubClient
			try:
				await TradinghubClient().send_notification(
					NotificationType.ERROR,
					f'❌ *Template Processing failed*\n'
					f'*Template:* {template.name}\n'
					f'*Strategy:* {template.strategy}\n'
					f'*Account:* {template.account}\n'
					f'*Error:* {str(e)}'
				)
			except Exception as notify_error:
				logger.error(f'Failed to send error notification: {notify_error}')

	def getMarketDataType(self) -> MarketDataType:
		""" Return the configured Market Data Type
		"""
		if self._marketDataType is None:
			config: Config = self['config']
			try:
				confMarketData = config.get('tws.marketdata')
			except KeyError as keyError:
				confMarketData = 'Delayed'
			self._marketDataType = MarketDataType()
			self._marketDataType.byString(confMarketData)
		return self._marketDataType

	def _getConfiguredAccounts(self) -> list:
		""" 
		Returns a list of configured accounts
		"""
		#conf: Config = self['config']
		conf: Config = optrabotcfg.appConfig
		configuredAccounts = None
		for item in conf.getTemplates():
			template : Template = item
			if configuredAccounts == None:
				configuredAccounts = [template.account]
			else:
				if not template.account in configuredAccounts:
					configuredAccounts.append(template.account)
		return configuredAccounts

	@logger.catch
	def handleTaskDone(self, task: asyncio.Task):
		if not task.cancelled():
			taskException = task.exception()
			if taskException != None:
				logger.error('Task Exception occured!')
				raise taskException