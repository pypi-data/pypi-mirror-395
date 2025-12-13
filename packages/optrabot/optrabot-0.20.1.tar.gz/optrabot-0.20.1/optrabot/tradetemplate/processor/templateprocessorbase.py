from datetime import datetime
from typing import List

from loguru import logger

import optrabot.config as optrabotcfg
from optrabot.broker.brokerconnector import BrokerConnector
from optrabot.broker.brokerfactory import BrokerFactory
from optrabot.broker.order import Leg, OptionRight, Order, OrderAction
from optrabot.config import Config
from optrabot.managedtrade import ManagedTrade
from optrabot.optionhelper import OptionHelper
from optrabot.signaldata import SignalData
from optrabot.symbolinfo import symbol_infos
from optrabot.tradetemplate.templatefactory import Template

"""
Base class for all template processors
"""
class TemplateProcessorBase:
	broker_connector: BrokerConnector

	def __init__(self, template: Template):
		"""
		Initializes the template processor with the given template
		
		Raises:
			ValueError: If no broker connector is available for the template's account
		"""
		self._template = template
		self.broker_connector = BrokerFactory().getBrokerConnectorByAccount(self._template.account)
		if self.broker_connector is None:
			raise ValueError(f'No active broker connection found for account {self._template.account}')
		self._config: Config = optrabotcfg.appConfig
		self._determined_expiration_date: datetime.date = None

	def composeEntryOrder(self, signalData: SignalData = None) -> Order:
		"""
		Composes the entry order based on the template and the optional signal data
		"""
		logger.debug('Creating entry order for template {}', self._template.name)
		
		# Check if explicit expiration_date is set (has priority over dte)
		if self._template.expiration_date is not None:
			self._determined_expiration_date = self._template.expiration_date
			logger.debug(f'Using explicit expiration date from template: {self._determined_expiration_date}')
		else:
			# Fall back to dte-based calculation
			self._determined_expiration_date = self.broker_connector.determine_expiration_date_by_dte(self._template.symbol, self._template.dte)
			if self._determined_expiration_date == None:
				raise ValueError(f'Unable to determine expiration date for template {self._template.name} with {self._template.dte} DTE !')
			logger.debug(f'Determined expiration date from DTE: {self._determined_expiration_date}')


	def composeTakeProfitOrder(self, managedTrade: ManagedTrade, fillPrice: float) -> Order:
		"""
		Composes the take profit order based on the template and the given fill price
		"""
		logger.debug('Creating take profit order for trade {}', managedTrade.trade.id)

	def composeStopLossOrder(self, managedTrade: ManagedTrade, fillPrice: float) -> Order:
		"""
		Composes the stop loss order based on the template and the given fill price
		"""
		logger.debug('Creating stop loss order for trade {}', managedTrade.trade.id)

	def hasTakeProfit(self) -> bool:
		"""
		Returns True if the template has a take profit defined
		"""
		return self._template.hasTakeProfit()
	
	def get_short_strike_from_delta(self, symbol: str, right: OptionRight, delta: int) -> float:
		"""
		Returns the short strike based on the given delta via the associated broker
		connector and the buffered price data
		"""
		return self.broker_connector.get_strike_by_delta(symbol, right, delta)
	
	def get_strike_by_price(self, symbol: str, right: OptionRight, price: float) -> float:
		"""
		Determines the strike based on a given premium price via the associated broker
		connector and the buffered price data
		"""
		return self.broker_connector.get_strike_by_price(symbol, right, price)

	def get_valid_strike(self, strike: float, expiration_date: datetime.date, higher: bool) -> float:
		"""
		Returns a valid strike price around the given strike. If the strike is not available,
		it will return the nearest higher or lower strike based on the 'higher' parameter.
		"""
		data = self.broker_connector.get_option_strike_data(self._template.symbol, expiration_date)
		try:
			strike_data = data.strikeData[strike]
			return strike
		except KeyError:
			strikes = data.strikeData.keys()
			return OptionHelper.get_next_strike(strike, strikes, higher)
		
	def determine_expiration_by_dte(self) -> datetime.date:
		"""
		Determines the expiration date based on the DTE of the processed template via the associated broker
		connector and the buffered price data
		"""
		expiration_date = self.broker_connector.determine_expiration_date_by_dte(self._template.symbol, self._template.dte)
		if expiration_date == None:
			raise ValueError(f'Unable to determine expiration date for template {self._template.name} with {self._template.dte} DTE !')
		return expiration_date

	def _has_active_trade_in_group(self) -> bool:
		"""
		Checks if there is an active trade from any template in the same template group (including self)
		"""
		from optrabot.trademanager import TradeManager

		# Get all templates in the same group (including self!)
		all_templates = self._config.getTemplates()
		templates_in_group = [t.name for t in all_templates 
							if t.template_group == self._template.template_group]
		
		# Check if any of these templates have active trades
		trade_manager = TradeManager()
		active_trades = trade_manager.getManagedTrades()
		
		for trade in active_trades:
			if trade.isActive() and trade.template.name in templates_in_group:
				logger.info(f'Template "{trade.template.name}" in group "{self._template.template_group}" has an active trade')
				return True
		
		return False

	def check_conditions(self) -> bool:
		"""
		Checks the conditions of the template against the given 
		"""
		# Check template group exclusivity first (before expensive VIX checks)
		if self._template.template_group is not None:
			if self._has_active_trade_in_group():
				logger.info(f'Template group "{self._template.template_group}" has active trade in another template. Blocking new trade.')
				return False
		
		if self._template.vix_max or self._template.vix_min:
			logger.debug('Checking VIX conditions')
			broker = BrokerFactory().getBrokerConnectorByAccount(self._template.account)
			if broker == None:
				logger.error('No broker connection available for account {}', self._template.account)
				return False
			
			try:
				vixPrice = broker.getLastPrice(symbol_infos['VIX'].symbol)
			except Exception as e:
				logger.warning('No price data for VIX available!')
				return False
			logger.debug('VIX Price: {}', vixPrice)
			if vixPrice:
				if self._template.vix_max:
					if vixPrice > self._template.vix_max:
						logger.info(f'Max VIX condition (max: {self._template.vix_max} current: {vixPrice}) not met. Ignoring signal.')
						return False
				if self._template.vix_min:
					if vixPrice < self._template.vix_min:
						logger.info(f'Min VIX condition (min: {self._template.vix_min} current: {vixPrice}) not met. Ignoring signal.')
						return False
		return True
	
	def invert_leg_actions(self, legs: List[Leg]):
		"""
		Inverts the actions of the given legs (BUY <-> SELL)
		"""
		for leg in legs:
			if leg.action == OrderAction.BUY:
				leg.action = OrderAction.SELL
			elif leg.action == OrderAction.SELL:
				leg.action = OrderAction.BUY