"""
Module to define the config of the application
"""
import os
from collections import UserDict
from typing import List, OrderedDict

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator, NumberValidator
from loguru import logger
from ruyaml import YAML
from ruyaml.scanner import ScannerError

from optrabot.flowengine.flowconfig import (Flow, FlowAction, FlowActionType,
                                            FlowEventConfig,
                                            ProcessTemplateAction,
                                            SendNotificationAction)
from optrabot.flowengine.flowevent import FlowEventType
from optrabot.tradetemplate.earlyexittrigger import EarlyExitTrigger
from optrabot.tradetemplate.templatedata import LongStrikeData, ShortStrikeData
from optrabot.tradetemplate.templatefactory import (IronCondor, IronFly,
                                                    PutSpread, Template,
                                                    TemplateFactory,
                                                    TemplateType)
from optrabot.tradetemplate.templatetrigger import TemplateTrigger

configFileName = "config.yaml"
defaultHubHost = 'wss://app.optrabot.io'

# Global variable to store the current configuration
appConfig = None

class Config(UserDict):
	def __init__(self, config_path=configFileName):
		self.config_path = os.path.expanduser(config_path)
		self._templates = []
		self._flows = []
		self.loaded = False
		self.load()

	def load(self):
		"""
        Loads configuration from configuration YAML file.
        """
		logger.debug("Try loading config file...")
		try:
			# Open with UTF-8 encoding explicitly to support emojis and special characters on Windows
			with open(os.path.expanduser(self.config_path), 'r', encoding='utf-8') as f:
				try:
					self.data = YAML().load(f)
					logger.debug("Config loaded successfully.")
					self.loaded = True
				except ScannerError as e:
					logger.error("Error parsing yaml of configuration file '{}' :{}", e.problem_mark, e.problem)
				except UnicodeDecodeError as e:
					logger.error("Error decoding configuration file '{}': {}. Make sure the file is saved as UTF-8.", self.config_path, str(e))
				except Exception as e:
					logger.error("Error loading configuration file '{}': {}", self.config_path, str(e))
		except FileNotFoundError:
			logger.error(
				 "Error opening configuration file {}".format(self.config_path)
			)
			self.createDefaultConfig()

	def createDefaultConfig(self):
		""" Create a default configuration 
		"""
		logger.info('Using a default configuration.')
		defaultDoc = 'general:\n'
		defaultDoc += '  instanceid: testagent\n'
		self.data = YAML().load(defaultDoc)

	def get(self, key):
		"""
		Fetch the configuration value for the specified key. If there are nested dictionaries, a dot
		notation can be used.

		So if the configuration contents are:

		self.data = {
			'first': {
				'second': 'value'
			},
		}

        self.data.get('first.second') == 'value'

		Arguments:
        	key(str): Configuration key to fetch
		"""
		keys = key.split('.')
		value = self.data.copy()

		for key in keys:
			value = value[key]
			if value == None:
				raise KeyError

		return value
	
	def save(self):
		"""
		Saves configuration in the configuration YAML file.
		"""
		with open(os.path.expanduser(self.config_path), 'w+') as f:
			yaml = YAML()
			yaml.default_flow_style = False
			yaml.dump(self.data, f)

	def logConfigurationData(self):
		"""
		Write Configuration data into the optrabot log file in Debug Mode
		"""
		logger.debug('Using following configuration data...')
		for key, value in self.data.items():
			logger.debug('Category {}:', key)
			if value == None:
				continue
			children = OrderedDict(value)
			for subkey, subvalue in children.items():
				if isinstance(subvalue, dict):
					logger.debug('Sub Category {}:', subkey)
					try:
						subChildren = OrderedDict(subvalue)
						for subsubkey, subsubvalue in subChildren.items():
							if isinstance(subsubvalue, dict):
								logger.debug('	{}', subsubkey)
								try:
									subsubChildren = OrderedDict(subsubvalue)
									for subsubsubkey, subsubsubvalue in subsubChildren.items():
										logger.debug('       	{}: {}', subsubsubkey, subsubsubvalue)
								except ValueError:
									continue
							else:
								logger.debug('       {}: {}', subsubkey, subsubvalue)
					except ValueError:
						continue
				else:
					logger.debug('   {}: {}', subkey, subvalue)

	def readTemplates(self):
		self._templates = []
		try:
			for key, data in self.get('templates').items():
				logger.debug('Reading Template: {}', key)
				template = TemplateFactory.createTemplate(name=key,data=data)
				if template != None:
					if template.validate():
						template_state = '' if template.is_enabled() else '(disabled)'
						logger.info(f'Loaded Trade Template: {template.name} {template_state}')
						self._templates.append(template)
					else:
						logger.error(f'Template {template.name} is not valid. Please check the configuration!')
		except KeyError as exc:
			logger.error('Missing key: {} --> No templates are configured!', exc)

	def getTemplates(self) -> List[Template]:
		""" Returns the configured templates
		"""
		return self._templates
	
	def get_template_by_name(self, template_name: str) -> Template | None:
		"""
		Find a template by its name.
		
		Args:
			template_name: Name of the template to find
			
		Returns:
			Template object if found, None otherwise
			
		Example:
			template = config.get_template_by_name("IC_SPX_0DTE")
		"""
		if not template_name:
			return None
		
		for template in self._templates:
			if template.name == template_name:
				return template
		
		return None
	
	def readFlows(self):
		"""
		Read flow configurations from the config file
		"""
		self._flows = []
		try:
			flows_config = self.get('flows')
			if flows_config is None:
				logger.debug('No flows configured')
				return
			
			# Handle both list and dict format
			if isinstance(flows_config, list):
				# List format: flows: - flow_id: {...}
				for flow_item in flows_config:
					if not isinstance(flow_item, dict):
						logger.warning(f'Invalid flow configuration item: {flow_item}')
						continue
					for flow_id, flow_data in flow_item.items():
						flow = self._parse_flow(flow_id, flow_data)
						if flow:
							self._flows.append(flow)
			elif isinstance(flows_config, dict):
				# Dict format: flows: flow_id: {...}
				for flow_id, flow_data in flows_config.items():
					flow = self._parse_flow(flow_id, flow_data)
					if flow:
						self._flows.append(flow)
			else:
				logger.error(f'Invalid flows configuration format: {type(flows_config)}')
				return
			
			logger.info(f'Loaded {len(self._flows)} flow configuration(s)')
			
		except KeyError:
			logger.debug('No flows section in configuration file')
	
	def _parse_flow(self, flow_id: str, flow_data: dict) -> Flow:
		"""
		Parse a single flow configuration
		
		Args:
			flow_id: Flow identifier
			flow_data: Flow configuration data
			
		Returns:
			Flow object or None if parsing fails
		"""
		try:
			# Extract basic flow properties
			name = flow_data.get('name')
			enabled = flow_data.get('enabled', True)
			
			# Parse event configuration
			event_config = None
			event_data = flow_data.get('event')
			if event_data:
				try:
					event_type = FlowEventType(event_data.get('type'))
					template_name = event_data.get('template')
					if not template_name:
						logger.error(f'Flow "{flow_id}": Missing required "template" in event configuration')
						return None
					
					# Validate that the template exists and is enabled
					template_found = False
					template_enabled = False
					for template in self._templates:
						if template.name == template_name:
							template_found = True
							template_enabled = template.is_enabled()
							break
					
					if not template_found:
						logger.warning(f'Flow "{flow_id}": Referenced template "{template_name}" does not exist - Flow will be disabled')
						enabled = False
					elif not template_enabled:
						logger.warning(f'Flow "{flow_id}": Referenced template "{template_name}" is disabled - Flow will be disabled')
						enabled = False
					
					event_config = FlowEventConfig(type=event_type, template=template_name)
				except ValueError as e:
					logger.error(f'Flow "{flow_id}": Invalid event type "{event_data.get("type")}"')
					return None
			else:
				logger.error(f'Flow "{flow_id}": Missing event configuration')
				return None
			
			# Parse actions
			actions = []
			actions_data = flow_data.get('actions', [])
			for action_item in actions_data:
				if not isinstance(action_item, dict):
					logger.warning(f'Flow "{flow_id}": Invalid action item: {action_item}')
					continue
				
				for action_type, action_config in action_item.items():
					if action_type == 'send_notification':
						message = action_config.get('message', '')
						notification_type = action_config.get('type', 'INFO')
						action = FlowAction(
							action_type=FlowActionType.SEND_NOTIFICATION,
							action_config=SendNotificationAction(message=message, type=notification_type)
						)
						actions.append(action)
					elif action_type == 'process_template':
						template_name = action_config.get('template')
						amount = action_config.get('amount')
						premium = action_config.get('premium')
						expiration = action_config.get('expiration')  # Optional
						time = action_config.get('time')  # Optional
						
						if not template_name:
							logger.error(f'Flow "{flow_id}": Missing template in process_template action')
							continue
						if amount is None:
							logger.error(f'Flow "{flow_id}": Missing amount in process_template action')
							continue
						if premium is None:
							logger.error(f'Flow "{flow_id}": Missing premium in process_template action')
							continue
						
						# Parse and validate time format if provided
						parsed_time = None
						if time is not None:
							from optrabot.tradetemplate.templatetrigger import TemplateTrigger
							try:
								# Parse the time using the same logic as TemplateTrigger
								trigger = TemplateTrigger({'type': 'time', 'value': time})
								parsed_time = trigger.parseTimeWithTimezone(time)
								if parsed_time is None:
									logger.error(f'Flow "{flow_id}": Invalid time format "{time}" - Expected format: HH:MM <Timezone> (e.g. "15:00 EST")')
									logger.error(f'Flow "{flow_id}": Flow will be disabled due to invalid time configuration')
									enabled = False
									continue
								logger.debug(f'Flow "{flow_id}": Successfully parsed time parameter: {time} -> {parsed_time}')
							except Exception as e:
								logger.error(f'Flow "{flow_id}": Error parsing time "{time}": {str(e)}')
								logger.error(f'Flow "{flow_id}": Flow will be disabled due to invalid time configuration')
								enabled = False
								continue
						
						# Validate that the template exists and is enabled
						template_found = False
						template_enabled = False
						for template in self._templates:
							if template.name == template_name:
								template_found = True
								template_enabled = template.is_enabled()
								break
						
						if not template_found:
							logger.warning(f'Flow "{flow_id}": Action references template "{template_name}" that does not exist - Flow will be disabled')
							enabled = False
							continue
						elif not template_enabled:
							logger.warning(f'Flow "{flow_id}": Action references template "{template_name}" that is disabled - Flow will be disabled')
							enabled = False
							continue
						
						action = FlowAction(
							action_type=FlowActionType.PROCESS_TEMPLATE,
							action_config=ProcessTemplateAction(
								template=template_name,
								amount=amount,
								premium=premium,
								expiration=expiration,
								time=parsed_time  # Store the parsed datetime object
							)
						)
						actions.append(action)
					else:
						logger.warning(f'Flow "{flow_id}": Unknown action type "{action_type}"')
			
			if not actions:
				logger.warning(f'Flow "{flow_id}": No valid actions configured')
			
			# Create flow object
			flow = Flow(
				id=flow_id,
				name=name,
				enabled=enabled,
				event=event_config,
				actions=actions
			)
			
			# Log flow loading with name or ID and enabled status
			state = 'enabled' if enabled else 'disabled'
			display_name = name if name else flow_id
			logger.info(f'Loaded Flow: {display_name} ({state})')
			return flow
			
		except Exception as e:
			logger.error(f'Error parsing flow "{flow_id}": {e}')
			return None
	
	def getFlows(self) -> List[Flow]:
		"""
		Returns the configured flows
		"""
		return self._flows
	
	def getInstanceId(self) -> str:
		""" Returns the configured OptraBot Agent Id / Instance Id
		"""
		instanceId = ''
		try:
			instanceId = self.get('general.instanceid')
		except KeyError as exc:
			instanceId = self.get('general.agentid')
		return instanceId

def captureTemplateData(template: Template):
	template.strategy = inquirer.text(message="Strategy:", default=template.strategy).execute()
	template.adjustmentStep = float(inquirer.number(message="Increment for limit price adjustments ($):",default=template.adjustmentStep, float_allowed=True, validate=EmptyInputValidator()).execute())
	#if template._type == TemplateType.IronFly:
	#	template.wing = int(inquirer.number(message="Wing Size (points):", default=template.wing, min_allowed=10).execute())
	if template._type == TemplateType.PutSpread:
		short_strike_data = template.getShortStrikeData()
		short_strike_data.offset = int(inquirer.number(message="Offset for the short strike ($):", default=short_strike_data.offset).execute())
		template.setShortStikeData(short_strike_data)
		long_strike_data = template.getLongStrikeData()
		long_strike_data.width = int(inquirer.number(message="Width of the Spread (points):", default=long_strike_data.width, min_allowed=1).execute())
		template.setLongStikeData(long_strike_data)
	template.account = inquirer.text(message="Account number to be used for trading:",default=template.account, validate=EmptyInputValidator()).execute()
	template.amount = int(inquirer.number(message="Number of contracts to be traded:", default=template.amount, min_allowed=1).execute())
	if template.takeProfit is not None:
		try:
			template.takeProfit = int(inquirer.number(message="Percentage of captured premium as profit target (%):", default=template.takeProfit, min_allowed=1, max_allowed=100).execute())
		except ValueError:
			template.takeProfit = None
	if template.stopLoss is not None:
		template.stopLoss = int(inquirer.number(message="Percentage of captured premium as stop loss level (%):", default=template.stopLoss, min_allowed=1).execute())
	if template._type == TemplateType.IronCondor:
		if template.wing is not None:
			template.wing = int(inquirer.number(message="Wing Size (points):", default=template.wing, min_allowed=5).execute())
		if template.premium is not None:
			template.premium = float(inquirer.number(message="Expected premium for an Iron Condor trade ($):",default=template.premium, float_allowed=True, validate=EmptyInputValidator()).execute())
	
	if template._type == TemplateType.IronFly:
		template.minPremium = float(inquirer.number(message="Minimum premium for an Iron Fly trade ($):",default=template.minPremium, float_allowed=True, validate=EmptyInputValidator()).execute())
	try:
		template.maxOpenTrades = int(inquirer.number(message="Maximum number of parallel open positions:", default=template.maxOpenTrades, min_allowed=1).execute())
	except ValueError:
		template.maxOpenTrades = 0

def ensureInitialConfig() -> bool:
	configPath = os.path.expanduser(configFileName)
	if os.path.exists(configPath):
		return True
	print("No config.yaml found. Let's answer some questions and generate the required configuration file.")
	configOK = False
	try:
		confAPIKey = inquirer.text(message="What's your OptraBot API Key:").execute()
		confInstanceId = inquirer.text(message="Give your OptraBot Instance an Id:", default="optrabot").execute()
		confWebPort = inquirer.number(message="Port number on which the OptraBot UI will be accessible:", default=8080).execute()
		confTWSHost = inquirer.text(message="Hostname of your TWS/IB Gateway machine:",default="127.0.0.1").execute()
		confTWSPort = inquirer.number(message="Port number of your TWS/IB Gateway:",default=7496, validate=NumberValidator()).execute()
		confTWSClientID = inquirer.number(message="Client ID to be used for TWS/IB Gateway connection:",default=21, validate=NumberValidator()).execute()
		confTWSMarketData = inquirer.select(
			message="Select a market data type:",
			choices=[
	            "Live",
	            "Delayed",
	            #Choice(value=None, name="Exit"),
	        ],
	        default="Live",
		).execute()

		templatesDict = {}
		addTemplate = True
		templCount = 0
		while templCount < 3:
			templCount += 1
			if templCount == 1:
				templateDefault = IronCondor('0DTEIIC')
				templateDefault.strategy = '0DTE Income Iron Condor'
				templateDefault._trigger = TemplateTrigger({'type': 'time', 'value': '09:32 EST'})
				templateDefault.adjustmentStep = 0.05
				templateDefault.wing = 15
				templateDefault.takeProfit = None
				templateDefault.stopLoss = None
				templateDefault.account = ''
				templateDefault.amount = 1
				templateDefault.set_enabled(True)
				templateDefault.premium = 0.6
				templateDefault.vix_max = 25
				templateDefault.set_early_exit(EarlyExitTrigger({'type': 'breakeven'}))
			elif templCount == 2 :
				templateDefault = PutSpread('0DTEMagickTrend10')
				templateDefault.strategy = 'Magick Trend 10'
				templateDefault._trigger = TemplateTrigger({'type': 'external', 'value': '0DTEMagickTrend10', 'excludetimefrom': '11:30 EST', 'excludetimeto': '12:00 EST'})
				templateDefault.adjustmentStep = 0.05
				short_strike_data = ShortStrikeData()
				short_strike_data.offset = -5
				templateDefault.setShortStikeData(short_strike_data)
				long_strike_data = LongStrikeData()
				long_strike_data.width = 70
				templateDefault.setLongStikeData(long_strike_data)
				templateDefault.account = ''
				templateDefault.amount = 1
				templateDefault.takeProfit = 50
				templateDefault.stopLoss = 200
				templateDefault.maxOpenTrades = None
				templateDefault.set_enabled(True)
				# templateDefault.minPremium = 14
			elif templCount == 3:
				templateDefault = PutSpread('0DTEMagickTrend30')
				templateDefault.strategy = 'Magick Trend 30'
				templateDefault._trigger = TemplateTrigger({'type': 'external', 'value': '0DTEMagickTrend30', 'timefrom': '11:00 EST', 'timeto': '15:00 EST'})
				templateDefault.adjustmentStep = 0.05
				short_strike_data = ShortStrikeData()
				short_strike_data.offset = -5
				templateDefault.setShortStikeData(short_strike_data)
				long_strike_data = LongStrikeData()
				long_strike_data.width = 70
				templateDefault.setLongStikeData(long_strike_data)
				templateDefault.account = ''
				templateDefault.amount = 1
				templateDefault.stopLoss = 200
				templateDefault.maxOpenTrades = None
				templateDefault.set_enabled(True)
			# elif templCount == 2:
			# 	templateDefault = IronFly('0DTELunchIF')
			# 	templateDefault.strategy = '0DTE Lunch Iron Fly'
			# 	templateDefault._trigger = TemplateTrigger({'type': 'external', 'value': '0DTELunchIF'})
			# 	templateDefault.adjustmentStep = 0.1
			# 	templateDefault.wing = 70
			# 	templateDefault.account = ''
			# 	templateDefault.amount = 1
			# 	templateDefault.takeProfit = 10
			# 	templateDefault.stopLoss = 20
			# 	templateDefault.minPremium = 0
			# elif templCount == 3:
			# 	templateDefault = IronFly('0DTEFOMCFly')
			# 	templateDefault.strategy = '0DTE FOMC Fly'
			# 	templateDefault._trigger = TemplateTrigger({'type': 'external', 'value': '0DTEFOMCFly'})
			# 	templateDefault.adjustmentStep = 0.1
			# 	templateDefault.wing = 100
			# 	templateDefault.account = ''
			# 	templateDefault.amount = 1
			# 	templateDefault.takeProfit = 10
			# 	templateDefault.stopLoss = 100
			# 	templateDefault.minPremium = 0
			else:
				break
			addTemplate = inquirer.confirm(message="Add a trade template '" +  templateDefault.name + "'", default=True).execute()
			if not addTemplate:
				continue
			captureTemplateData(templateDefault)
			templatesDict.update({templateDefault.name:templateDefault.toDict()})

		# confTradingAccount = inquirer.text(message="Account number to be used for trading:",default="").execute()
		# confTradingContracts = inquirer.number(message="Number of IronFly contracts to be traded:", min_allowed=1).execute()
		# confTradingPriceIncement = inquirer.number(message="Increment for limit price adjustments ($):",default=0.1, float_allowed=True, validate=EmptyInputValidator()).execute()
		# confTradingMinimumPremium = inquirer.number(message="Minimum premium for an Iron Fly trade ($):",default=14, float_allowed=True, validate=EmptyInputValidator()).execute()
		# confTradingTakeProfit = inquirer.number(message="Percentage of captured premium as profit target (%):", default=8, min_allowed=1, max_allowed=100).execute()
		# confTradingStopLoss = inquirer.number(message="Percentage of captured premium as stop loss level (%):", default=16, min_allowed=1).execute()
		# confStopLossAdjust = inquirer.confirm(message="Automatic stop loss adjustment?",default=False).execute()
		# if confStopLossAdjust:
		# 	confSLATrigger = inquirer.number(message="Percentage of profit that triggers the stop loss adjustment (%):", default=10, min_allowed=1, validate=EmptyInputValidator()).execute()
		# 	confSLAStop = inquirer.number(message="Adjusted stop 'postive=below entry; negative=above entry' (%):", default=0, validate=EmptyInputValidator()).execute()
		# 	confSLAOffset = inquirer.number(message="Offset for the adjusted stop 'negtive=away from market; positive=closer to market' ($):", default=-0.2, float_allowed=True,validate=EmptyInputValidator()).execute()
		confirm = inquirer.confirm(message="Confirm?", default=True).execute()
	except KeyboardInterrupt as exc:
		print('Configuration has been aborted!')
		return False

	if not confirm:
		print("Configuration assistant abortet!")
		return

	data = dict(general=dict(port=int(confWebPort), apikey=confAPIKey, instanceid=confInstanceId, hub=defaultHubHost),
				tws=dict(host=confTWSHost, port=int(confTWSPort), clientid=int(confTWSClientID), marketdata=confTWSMarketData),templates=templatesDict)
	#if confStopLossAdjust:
	#	twsItems = dict(data["tws"].items())
	#	twsItems["adjuststop"] = dict(trigger=int(confSLATrigger), stop=int(confSLAStop), offset=float(confSLAOffset))
	#	data["tws"] = twsItems
		  
	configYAML = yaml=YAML()
	try:
		with open(configFileName, 'w') as configFile:
			configYAML.dump(data, configFile )
		print("Config file " + configFileName + " has been generated based on your answers.\nYou may modify the configuration file manually if required.")
		configOK = True
	except IOError as exc:
		print("Error generating the config file:", configFileName)
		print("I/O error({0}): {1}".format(exc.errno, exc.strerror))
		return
	
	return configOK