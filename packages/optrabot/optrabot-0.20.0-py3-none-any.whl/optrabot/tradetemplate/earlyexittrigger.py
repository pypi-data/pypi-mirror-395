from typing import OrderedDict
from datetime import datetime
from loguru import logger
class EarlyExitTriggerType:
	Breakeven: str = 'breakeven'
	Time: str = 'time'

class EarlyExitTrigger:
	_trigger_time: datetime = None
	type: EarlyExitTriggerType = None

	def __init__(self, triggerdata: OrderedDict) -> None:
		type = triggerdata['type']
		assert type in [EarlyExitTriggerType.Breakeven, EarlyExitTriggerType.Time]
		self.type = type
		try:
			self.value = triggerdata['value']
		except KeyError:
			self.value = None
			pass

	def toDict(self):
		""" Returns a dictionary representation of the EarlyExit Trigger which is used for
		the config file.
		"""
		returnDict = {'type': self.type}
		# eastern = pytz.timezone('US/Eastern')
		# if self.fromTimeUTC != None:
		# 	returnDict['timefrom'] = self.fromTimeUTC.astimezone(eastern).strftime('%H:%M %Z')
		# if self.toTimeUTC != None:
		# 	returnDict['timeto'] = self.toTimeUTC.astimezone(eastern).strftime('%H:%M %Z')
		# if self.excludeFromTimeUTC != None:
		# 	returnDict['excludetimefrom'] = self.excludeFromTimeUTC.astimezone(eastern).strftime('%H:%M %Z')
		# if self.excludeToTimeUTC != None:
		# 	returnDict['excludetimeto'] = self.excludeToTimeUTC.astimezone(eastern).strftime('%H:%M %Z')	
		return returnDict