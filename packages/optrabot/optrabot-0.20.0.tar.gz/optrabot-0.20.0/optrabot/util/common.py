from datetime import datetime
from loguru import logger
import pytz
import re

class Common:

	@staticmethod
	def parse_with_timezone(timeStr: str) -> datetime.time:
		""" 
		Parses a time string like 11:00 EST to a datetime.time object
		"""
		if timeStr == None:
			return None
		
		parts = timeStr.split(' ')
		try:
			now = datetime.now()
			naive_time = datetime.strptime(parts[0], '%H:%M').replace(year=now.year, month=now.month, day=now.day)
			if len(parts) > 1:
				tzstr = parts[1]
			else:
				tzstr = 'EST'
			tzstr = "US/Eastern" if tzstr == 'EST' else tzstr
			tz = pytz.timezone(tzstr)
			localized_time = tz.localize(naive_time)
			return localized_time
		except ValueError and AttributeError as error:
			logger.error(f'Invalid time format: {timeStr} - Expecting HH:MM <Timezone>')
			return None
	
	# Markdown v1 regex patterns to detect syntax elements
	# Note: We only detect Bold, URLs and Code blocks to avoid false matches
	# For example, _text_ could be italic OR just underscores in variable names
	_MARKDOWN_PATTERNS = [
		r'\*[^*\n]+\*',                  # Bold (single line only)
		r'\[([^\]]+)\]\(([^)]+)\)',      # Inline URL
		r'`[^`]+`',                      # Inline code
	]
	_COMBINED_PATTERN = re.compile('|'.join(_MARKDOWN_PATTERNS))
	
	# Special characters that need to be escaped in Telegram Markdown v1
	# Only these characters need escaping: _ * ` [
	_SPECIAL_CHARS = r'_*`['
	
	@staticmethod
	def escape_markdown(text: str) -> str:
		"""
		Escape special characters for Telegram Markdown formatting.
		
		This method intelligently detects Markdown syntax elements and escapes
		only the special characters outside these elements. This preserves
		intentional formatting while making literal text safe for Telegram.
		
		Supports Telegram Markdown v1 which requires escaping: _ * ` [
		
		Args:
			text: The text to escape
			
		Returns:
			str: The escaped text safe for Telegram Markdown
		"""
		if text is None or text == "":
			return ""
		
		text = str(text)
		
		# Find all MarkdownV2 syntax matches
		matches = list(Common._COMBINED_PATTERN.finditer(text))
		
		# Initialize variables
		escaped_parts = []
		last_end = 0
		
		for match in matches:
			start, end = match.start(), match.end()
			
			# Escape non-Markdown text before the current match
			if last_end < start:
				non_markdown_part = text[last_end:start]
				escaped_non_markdown = Common._escape_non_markdown(non_markdown_part)
				escaped_parts.append(escaped_non_markdown)
			
			# Append the Markdown syntax without escaping
			escaped_parts.append(match.group())
			last_end = end
		
		# Escape any remaining non-Markdown text after the last match
		if last_end < len(text):
			remaining_text = text[last_end:]
			escaped_remaining = Common._escape_non_markdown(remaining_text)
			escaped_parts.append(escaped_remaining)
		
		return ''.join(escaped_parts)
	
	@staticmethod
	def _escape_non_markdown(text: str) -> str:
		"""
		Escape special characters in non-Markdown text.
		
		Args:
			text: Text outside of Markdown syntax
			
		Returns:
			str: Escaped text
		"""
		escaped = ''
		for char in text:
			if char in Common._SPECIAL_CHARS:
				escaped += '\\' + char
			else:
				escaped += char
		return escaped