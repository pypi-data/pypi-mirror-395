from typing import List, OrderedDict

from loguru import logger

#from optrabot.tradetemplate.putspread import PutSpread
#from optrabot.tradetemplate.template import Template, TemplateType
from optrabot.deltaadjuster import DeltaAdjuster
from optrabot.optionhelper import OptionHelper
from optrabot.stoplossadjuster import StopLossAdjuster
from optrabot.tradetemplate.earlyexittrigger import EarlyExitTrigger
from optrabot.tradetemplate.templatedata import LongStrikeData, ShortStrikeData
from optrabot.tradetemplate.templatetrigger import TemplateTrigger
from optrabot.util.common import Common


class TemplateType:
	IronCondor = "Iron Condor"
	IronFly = "Iron Fly"
	PutSpread = "Put Spread"
	LongCall = "Long Call"
	LongPut = "Long Put"

class Template:
	def __init__(self, name: str) -> None:
		self._type = None
		self.name = name
		self._trigger = None
		self._early_exit = None
		self.account = None
		self.takeProfit = None
		self.soft_takeprofit = False
		self.stopLoss = None
		self.amount = 1
		self.minPremium = None
		self.max_premium = None
		self.premium = None
		self.adjustmentStep = 0.05
		self.maxEntryAdjustments = None  # Maximum number of entry order price adjustments (None = unlimited)
		self.stoploss_adjusters: List[StopLossAdjuster] = []
		self.strategy = ''
		self.wing = None
		self.symbol = 'SPX'
		self.maxOpenTrades = 0
		self.single_leg = False
		self._enabled = True
		self._shortStrikeData: ShortStrikeData = None
		self.vix_max = None
		self.vix_min = None
		self.soft_take_profit = False
		self.delta_adjusters: List[DeltaAdjuster] = []
		self.dte = 0  # Days to expiration
		self.expiration_date = None  # Explicit expiration date (has priority over dte)
		self.template_group = None  # Template group for mutual exclusivity
		self.trade_group_id = None  # Trade group ID (set by Flow Engine for rollovers)

	def getType(self) -> str:
		""" Returns the type of the template
		"""
		return self._type
	
	def get_stoploss_adjusters(self) -> List[StopLossAdjuster]:
		""" Returns the list of Stop Loss Adjusters for this template
		"""
		return self.stoploss_adjusters

	def setTrigger(self, trigger: TemplateTrigger):
		""" Defines the trigger for this template
		"""
		self._trigger = trigger

	def getTrigger(self) -> TemplateTrigger:
		""" Returns the trigger of the template
		"""
		return self._trigger
	
	def set_early_exit(self, early_exit: EarlyExitTrigger):
		""" Sets the early exit trigger for this template
		"""
		self._early_exit = early_exit

	def get_early_exit(self) -> EarlyExitTrigger:
		""" Returns the early exit trigger of the template
		"""
		return self._early_exit

	def setAccount(self, account: str):
		""" Sets the account which the template is traded on 
		"""
		self.account = account
	
	def setTakeProfit(self, takeprofit: int):
		""" Sets the take profit level in % of the template
		"""
		self.takeProfit = takeprofit

	def set_soft_take_profit(self, soft_take_profit: bool):
		""" Sets the soft take profit flag
		"""
		self.soft_take_profit = soft_take_profit

	def setStopLoss(self, stoploss: int):
		""" Sets the stop loss level in % of the template
		"""
		self.stopLoss = stoploss

	def setAmount(self, amount: int):
		""" Sets the amount of contracts to be traded with this template
		"""
		self.amount = amount
	
	def setMinPremium(self, minPremium: float):
		""" Sets the minimum premium which must be received from broker in order to execute a trade
		of this template.
		"""
		self.minPremium = minPremium

	def set_max_premium(self, max_premium: float) -> None:
		""" Sets the maximum premium allowed for executing a trade of this template.
		For credit trades: maximum credit to receive.
		For debit trades: maximum debit to pay.
		"""
		self.max_premium = max_premium

	def set_premium(self, premium: float):
		""" Sets the premium of this template
		"""
		self.premium = premium

	def get_premium(self) -> float | None:
		""" Returns the premium of this template
		"""
		return self.premium

	def setAdjustmentStep(self, adjustmentStep: float):
		""" Sets the price adjustment step size for the entry order adjustment
		"""
		self.adjustmentStep = adjustmentStep

	def get_adjustment_step(self) -> float:
		""" Returns the price adjustment step size for entry order adjustment
		"""
		return self.adjustmentStep

	def setMaxEntryAdjustments(self, maxEntryAdjustments: int):
		""" Sets the maximum number of entry order price adjustments.
		If None, unlimited adjustments are allowed.
		"""
		self.maxEntryAdjustments = maxEntryAdjustments

	def get_max_entry_adjustments(self) -> int:
		""" Returns the maximum number of entry order price adjustments.
		Returns None if unlimited adjustments are allowed.
		"""
		return self.maxEntryAdjustments

	def set_stoploss_adjusters(self, stoploss_adjusters: List[StopLossAdjuster]):
		""" Sets the list of Stop Loss Adjusters for this template, if configured
		"""
		self.stoploss_adjusters = stoploss_adjusters
	
	def setStrategy(self, strategy: str):
		""" Sets the strategy name of this template
		"""
		self.strategy = strategy
	
	def setWing(self, wing: int):
		""" Set the wing size for Iron Fly and Iron Condor strategies
		"""
		self.wing = wing

	def set_dte(self, dte: int):
		""" Sets the days to expiration for this template
		"""
		self.dte = dte

	def set_expiration_date(self, expiration_date):
		""" Sets the explicit expiration date for this template.
		This has priority over the dte value.
		
		Args:
			expiration_date: datetime.date object representing the expiration date
		"""
		self.expiration_date = expiration_date

	def get_wing(self) -> int | None:
		""" Returns the wing size for Iron Fly and Iron Condor strategies
		"""
		return self.wing

	def toDict(self):
		""" Returns a dictionary representation of the Template which is used for
		the config file.
		"""
		returnDict = {}
		returnDict['enabled'] = self._enabled
		returnDict['type'] = self._type
		returnDict['strategy'] = self.strategy
		returnDict['adjustmentstep'] = self.adjustmentStep
		if self.maxEntryAdjustments is not None:
			returnDict['maxentryadjustments'] = self.maxEntryAdjustments
		returnDict['account'] = self.account
		if self.takeProfit != None and self.takeProfit > 0:
			returnDict['takeprofit'] = self.takeProfit
		if self.stopLoss != None and self.stopLoss > 0:
			returnDict['stoploss'] = self.stopLoss
		returnDict['amount'] = self.amount
		returnDict['maxopentrades'] = self.maxOpenTrades
		if self.premium != None and self.premium > 0:
			returnDict['premium'] = self.premium
		if self.wing != None and self.wing > 0:
			returnDict['wing'] = self.wing
		if self._early_exit != None:
			returnDict['earlyexit'] = self._early_exit.toDict()
		if self._type == TemplateType.PutSpread:
			returnDict.update({'shortstrike':self._shortStrikeData.toDict()})
			returnDict.update({'longstrike':self._longStrikeData.toDict()})
		returnDict.update({'trigger':self._trigger.toDict()})
		if self.vix_max != None and self.vix_max > 0:
			returnDict['condition'] = {'vix_max': self.vix_max}
		return returnDict
	
	def setShortStikeData(self, shortStrikeData: ShortStrikeData):
		"""
		This is just a dummy method which is implemented in the derived classes
		"""
		raise NotImplementedError('Method setShortStikeData not implemented in this class')
	
	def setLongStikeData(self, longStrikeData: LongStrikeData):
		"""
		This is just a dummy method which is implemented in the derived classes
		"""
		raise NotImplementedError('Method setLongStikeData not implemented in this class')
	
	def setMaxOpenTrades(self, maxOpenTrades: int):
		""" Sets the maximum number of open trades for this template
		"""
		self.maxOpenTrades = maxOpenTrades

	def __str__(self) -> str:
		""" Returns a string representation of the strategy
		"""
		templateString = ('Name: ' + self.name + ' Type: ' + self._type + ' Trigger: (' + self._trigger.type + ', ' + str(self._trigger.value) + ')' +
		' Account: ' + self.account + ' Amount: ' + str(self.amount) + ' Take Profit (%): ' + str(self.takeProfit) + ' Stop Loss (%): ' + str(self.stopLoss) +
		' Min. Premium: ' + str(self.minPremium) + ' Max. Premium: ' + str(self.max_premium) + ' Entry Adjustment Step: ' + str(self.adjustmentStep) + ' Wing size: ' + str(self.wing) + ')' ) 
		return templateString
	
	def set_delta_adjusters(self, delta_adjusters: List[DeltaAdjuster]):
		""" Sets the list of Delta Adjusters for this template, if configured
		"""
		self.delta_adjusters = delta_adjusters

	def get_delta_adjusters(self) -> List[DeltaAdjuster]:
		""" Returns the list of Delta Adjusters for this template
		"""
		return self.delta_adjusters

	def meetsMinimumPremium(self, premium: float) -> bool:
		""" Returns True if the given premium meets the minimum premium requirement
		"""
		if self.minPremium == None:
			return True
		if premium > (self.minPremium * -1):
			return False
		return True

	def meets_maximum_premium(self, premium: float) -> bool:
		""" Returns True if the given premium meets the maximum premium requirement.
		For credit trades (negative premium): abs(premium) must not exceed max_premium.
		For debit trades (positive premium): premium must not exceed max_premium.
		"""
		if self.max_premium is None:
			return True
		# Premium is negative for credit trades, positive for debit trades
		# We check the absolute value against max_premium
		if abs(premium) > self.max_premium:
			return False
		return True
	
	def calculateTakeProfitPrice(self, fillPrice: float) -> float:
		""" Calculates the take profit price based on the fill price of the entry order
		"""
		logger.debug('Calculating take profit price for fill price {} and take profit {}%', fillPrice, self.takeProfit)
		roundBase = 5
		if self.single_leg == True:
			roundBase = 10
		if self.is_credit_trade():
			target = fillPrice - (abs(fillPrice) * (self.takeProfit / 100))
		else:
			target = fillPrice + (abs(fillPrice) * (self.takeProfit / 100))
		return OptionHelper.roundToTickSize(target, roundBase)
	
	def calculateStopLossPrice(self, fillPrice: float) -> float:
		""" Calculates the stop loss price based on the fill price of the entry order
		"""
		logger.debug('Calculating stop loss price for fill price {} and stop loss {}%', fillPrice, self.stopLoss)
		roundBase = 5	
		if self.single_leg == True:
			roundBase = 10
		if self.is_credit_trade():
			stop = fillPrice + (abs(fillPrice) * (self.stopLoss / 100))
		else:
			stop = fillPrice - (abs(fillPrice) * (self.stopLoss / 100))
			stop = 0 if stop < 0 else stop
		return OptionHelper.roundToTickSize(stop, roundBase)
	
	def hasStopLoss(self) -> bool:
		""" Returns True if the template has a stop loss defined
		"""
		return self.stopLoss != None

	def hasTakeProfit(self) -> bool:
		""" Returns True if the template has a take profit defined
		"""
		return self.takeProfit != None
	
	def set_enabled(self, enabled: bool):
		""" Sets the enabled state of the Template
		"""
		self._enabled = enabled

	def is_credit_trade(self) -> bool:
		""" Returns True if the trade is a credit trade.
		This is relevant for the stop loss adjuster, because lower prices mean profit if it is a credit trade.
		"""
		raise NotImplementedError('Method is_credit_trade not implemented in this class')

	def is_enabled(self) -> bool:
		""" Returns True if the Template is enabled
		"""
		return self._enabled
	
	def has_soft_take_profit(self) -> bool:
		""" Returns True if the Template has a soft take profit
		"""
		return self.soft_take_profit
	
	def validate(self) -> bool:
		"""
		Validates the template configuration
		"""
		# Stop Loss Adjuster only if a stop loss is defined
		if len(self.get_stoploss_adjusters()) > 0 and not self.hasStopLoss():
			logger.error('Stop Loss Adjusters are defined but no initial stop loss is defined!')
			return False
		
		# Validate max_premium > min_premium when both are set
		if self.max_premium is not None and self.minPremium is not None:
			if self.max_premium <= self.minPremium:
				logger.error(f'Template {self.name}: maxpremium ({self.max_premium}) must be greater than minpremium ({self.minPremium})')
				return False
		
		return True

	def validate_for_broker(self, broker_connector) -> bool:
		"""
		Validates the template configuration for a specific broker connector.
		Checks if the broker supports the template's order types (multileg, stop loss, take profit).
		
		Args:
			broker_connector: The BrokerConnector instance to validate against
			
		Returns:
			True if the template is compatible with the broker, False otherwise
		"""
		# Check multileg templates with brokers that don't support native multileg orders
		if not broker_connector.supports_multileg_orders():
			if not self.single_leg:  # This is a multileg template
				if self.hasStopLoss():
					logger.error(f'Template {self.name}: StopLoss is not supported for multileg templates '
								f'with broker {broker_connector.id} (broker does not support native multileg orders)')
					return False
				if self.hasTakeProfit():
					logger.error(f'Template {self.name}: TakeProfit is not supported for multileg templates '
								f'with broker {broker_connector.id} (broker does not support native multileg orders)')
					return False
		return True

class LongCall(Template):
	def __init__(self, name: str) -> None:
		super().__init__(name=name)
		self._type = TemplateType.LongCall
		self._longStrikeData = None
		self.single_leg = True

	def setLongStikeData(self, longStrikeData: LongStrikeData):
		self._longStrikeData = longStrikeData

	def getLongStrikeData(self) -> LongStrikeData:
		return self._longStrikeData
	
	def is_credit_trade(self) -> bool:
		""" Long Call is a debit trade
		"""
		return False
	
class LongPut(Template):
	def __init__(self, name: str) -> None:
		super().__init__(name=name)
		self._type = TemplateType.LongPut
		self._longStrikeData = None
		self.single_leg = True

	def setLongStikeData(self, longStrikeData: LongStrikeData):
		self._longStrikeData = longStrikeData

	def getLongStrikeData(self) -> LongStrikeData:
		return self._longStrikeData
	
	def is_credit_trade(self) -> bool:
		""" Long Call is a debit trade
		"""
		return False

class PutSpread(Template):
	def __init__(self, name: str) -> None:
		super().__init__(name=name)
		self._type = TemplateType.PutSpread
		self._shortStrikeData = None
		self._longStrikeData = None

	def setShortStikeData(self, shortStrikeData: ShortStrikeData):
		self._shortStrikeData = shortStrikeData

	def setLongStikeData(self, longStrikeData: LongStrikeData):
		self._longStrikeData = longStrikeData

	def getShortStrikeData(self) -> ShortStrikeData:
		return self._shortStrikeData
	
	def getLongStrikeData(self) -> LongStrikeData:
		return self._longStrikeData
	
	def is_credit_trade(self) -> bool:
		""" Put Spread is a credit trade
		"""
		return True

class IronFly(Template):
	def __init__(self, name: str) -> None:
		super().__init__(name=name)
		self._type = TemplateType.IronFly

class IronCondor(Template):
	def __init__(self, name: str) -> None:
		super().__init__(name=name)
		self._type = TemplateType.IronCondor
		self.single_leg = False

	def is_credit_trade(self) -> bool:
		""" Iron Condor is a credit trade
		"""
		return True
	
	def getShortStrikeData(self) -> ShortStrikeData:
		return self._shortStrikeData
	
	def setShortStikeData(self, shortStrikeData: ShortStrikeData):
		self._shortStrikeData = shortStrikeData

class TemplateFactory:

	@staticmethod
	def createTemplate(name: str, data) -> Template:
		""" Creates a template object from the given template configuration of config.yaml
		"""
		template = None
		templateType = data['type']
		match templateType:
			case TemplateType.IronCondor:
				logger.debug('Creating Iron Condor template from config')
				template = IronCondor(name)
			case TemplateType.IronFly:
				logger.debug('Creating Iron Fly template from config')
				template = IronFly(name)
			case TemplateType.PutSpread:
				logger.debug('Creating Put Spread template from config')
				template = PutSpread(name)
			case TemplateType.LongCall:
				logger.debug('Creating Long Call template from config')
				template = LongCall(name)
			case TemplateType.LongPut:
				logger.debug('Creating Long Put template from config')
				template = LongPut(name)
			case _:
				logger.error('Template type {} is unknown!', templateType)
				return None

		# Enabled
		try:
			enabled = data['enabled']
			template.set_enabled(enabled)
		except KeyError:
			template.set_enabled(True)

		# Strategy
		try:
			strategy = data['strategy']
			template.setStrategy(strategy)
		except KeyError:
			pass

		# Max Open Trades
		try:
			maxOpenTrades = data['maxopentrades']
			template.setMaxOpenTrades(maxOpenTrades)
		except KeyError:
			pass

		# Trigger configuration
		try:
			triggerinfo = data['trigger']
			trigger = TemplateTrigger(triggerinfo)
			template.setTrigger(trigger)
		except KeyError:
			pass

		# Early Exit
		try:
			early_exit_config = data['earlyexit']
			early_exit = EarlyExitTrigger(early_exit_config)
			template.set_early_exit(early_exit)
		except KeyError:
			pass

		try:
			account = str(data['account'])
			template.setAccount(account)
		except KeyError:
			pass

		try:
			takeProfit = data['takeprofit']
			template.setTakeProfit(takeProfit)
		except KeyError:
			pass

		try:
			soft_take_profit = data['soft_takeprofit']
			template.set_soft_take_profit(soft_take_profit)
		except KeyError:
			pass

		try:
			stopLoss = data['stoploss']
			template.setStopLoss(stopLoss)
		except KeyError:
			pass

		try:
			dte = data['dte']
			template.set_dte(dte)
		except KeyError:
			pass

		try:
			amount = data['amount']
			template.setAmount(amount)
		except KeyError:
			pass

		try:
			minPremium = data['minpremium']
			template.setMinPremium(minPremium)
		except KeyError:
			pass

		try:
			max_premium = data['maxpremium']
			template.set_max_premium(max_premium)
		except KeyError:
			pass

		try:
			premium = data['premium']
			template.set_premium(premium)
		except KeyError:
			pass

		try:
			adjustmentStep = data['adjustmentstep']
			template.setAdjustmentStep(adjustmentStep)
		except KeyError:
			pass

		try:
			maxEntryAdjustments = data['maxentryadjustments']
			template.setMaxEntryAdjustments(maxEntryAdjustments)
		except KeyError:
			pass

		try:
			wing = data['wing']
			template.setWing(wing)
		except KeyError:
			pass

		# Short Strike
		try:
			shortstrikeConfig = data['shortstrike']
			shortStrikeData = ShortStrikeData()
			try:
				shortStrikeData.offset = shortstrikeConfig['offset']
			except KeyError:
				pass
			try:
				shortStrikeData.delta = shortstrikeConfig['delta']
			except KeyError:
				pass
			try:
				shortStrikeData.price = shortstrikeConfig['price']
			except KeyError:
				pass
			# Set the short strike data in the template if supported
			try:
				template.setShortStikeData(shortStrikeData)
			except AttributeError:
				pass

		except KeyError:
			pass

		# Long Strike
		try:
			longstrikeConfig = data['longstrike']
			if longstrikeConfig:
				longStrikeData = LongStrikeData()
				try:
					longStrikeData.width = longstrikeConfig['width']
				except KeyError:
					pass
				try:
					longStrikeData.max_width = longstrikeConfig['max_width']
				except KeyError:
					pass
				try:
					longStrikeData.offset = longstrikeConfig['offset']
				except KeyError:
					pass
				try:
					longStrikeData.delta = longstrikeConfig['delta']
				except KeyError:
					pass
				try:
					longStrikeData.price = longstrikeConfig['price']
				except KeyError:
					pass
				
				# Set the long strike data in the template if supported
				try:
					template.setLongStikeData(longStrikeData)
				except AttributeError:
					pass
		except KeyError:
			pass

		# Conditions
		try:
			conditions = data['condition']
			try:
				template.vix_max = conditions['vix_max']
			except KeyError:
				pass

			try:
				template.vix_min = conditions['vix_min']
			except KeyError:
				pass

		except KeyError:
			pass

		# Template Group
		try:
			template_group = data['template_group']
			template.template_group = template_group
		except KeyError:
			pass

		# Stop Loss Adjuster
		adjuster_count = 0
		stoploss_adjusters: List[StopLossAdjuster] = []
		while True:
			adjuster_count += 1
			try:
				stoplossadjustment = OrderedDict(data['adjuststop' + str(adjuster_count)])
				try:
					trigger = stoplossadjustment['trigger']
					stop = stoplossadjustment['stop']
					try:
						offset = float(stoplossadjustment['offset'])
					except KeyError:
						# Offset is optional
						offset = 0.0
						pass

					adjuster = StopLossAdjuster(reverse=template.is_credit_trade(), trigger=trigger, stop=stop, offset=offset)
					stoploss_adjusters.append(adjuster)
				except KeyError as key_err:
					logger.error('Stop Loss Adjuster {} is missing data', adjuster_count)
					break


			except KeyError as keyErr:
				break
		if len(stoploss_adjusters) > 0:
			template.set_stoploss_adjusters(stoploss_adjusters)

		# Delta Adjustment
		try:
			delta_adjustment_data = data['delta_adjustment']
			delta_adjusters: List[DeltaAdjuster] = []
			for value in delta_adjustment_data:
				try:
					from_time_value = value['adjustment']['from_time']
					from_time = Common.parse_with_timezone(from_time_value)
				except KeyError:
					logger.error('Delta Adjuster is missing "from_time" key')
					continue

				try:
					threshold = value['adjustment']['threshold']
				except KeyError:
					logger.error('Delta Adjuster is missing "threshold" key')
					continue

				delta_adjuster = DeltaAdjuster(from_time=from_time, threshold=threshold)
				delta_adjusters.append(delta_adjuster)
			if len(delta_adjusters) > 0:
				delta_adjusters.sort(key=lambda x: x.from_time, reverse=True)
				template.set_delta_adjusters(delta_adjusters)
		except KeyError:
			pass

		return template
			
