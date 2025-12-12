import argparse
import inspect
import logging
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
import warnings
from contextlib import asynccontextmanager
from pathlib import Path

# Suppress GTK warnings from InquirerPy on Linux systems
os.environ['NO_AT_BRIDGE'] = '1'
os.environ['GTK_MODULES'] = ''
# Also suppress GTK-related warnings in stderr
warnings.filterwarnings('ignore', category=Warning, module='.*gtk.*')

import certifi
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from InquirerPy import inquirer
from loguru import logger
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from ruyaml import YAML

import optrabot.api.auth
import optrabot.api.template
import optrabot.config as optrabotcfg

from .optrabot import OptraBot, get_version

ValidLogLevels = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']

@asynccontextmanager
async def lifespan(app: FastAPI):
	app.optraBot = OptraBot(app)
	await app.optraBot.startup()
	yield
	await app.optraBot.shutdown()

"""fix yelling at me error"""
from asyncio.proactor_events import _ProactorBasePipeTransport
from functools import wraps


def silence_event_loop_closed(func) -> callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper
 
_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
"""fix yelling at me error end"""

def	get_frontend_dir() -> str:
	"""Returns the path to the frontend directory (optrabot/ui)"""
	current_file_path = os.path.abspath(__file__)
	current_dir = os.path.dirname(current_file_path)
	frontend_dist_dir = os.path.join(current_dir, 'ui')
	return frontend_dist_dir

_frontend_dir = get_frontend_dir()

app = FastAPI(lifespan=lifespan)

# CORS-Konfiguration
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Erlaube spezifische Ursprünge
    allow_origins=["*"],  # Erlaube alle Ursprünge
	allow_credentials=True,
    allow_methods=["*"],  # Erlaube alle HTTP-Methoden
    allow_headers=["*"],  # Erlaube alle Header
)

import optrabot.api.auth
import optrabot.api.status
import optrabot.api.template
import optrabot.api.trades

app.include_router(optrabot.api.template.router)
app.include_router(optrabot.api.auth.router)
app.include_router(optrabot.api.status.router)
app.include_router(optrabot.api.trades.router)

# Serve static assets (JS, CSS, images) for the React frontend
app.mount("/ui/assets", StaticFiles(directory=os.path.join(_frontend_dir, "assets")), name="frontend-assets")

# Serve React frontend index.html for root /ui/ path
@app.get("/ui/")
@app.get("/ui")
async def serve_frontend_root():
	"""Serve React frontend index.html"""
	return FileResponse(os.path.join(_frontend_dir, "index.html"))

# Serve other static files in /ui (favicon, logo, etc.) with SPA fallback
@app.get("/ui/{filename:path}")
async def serve_frontend(filename: str):
	"""Serve React frontend files with SPA fallback"""
	file_path = os.path.join(_frontend_dir, filename)
	# If the file exists, serve it
	if os.path.isfile(file_path):
		return FileResponse(file_path)
	# Otherwise, serve index.html for SPA routing
	return FileResponse(os.path.join(_frontend_dir, "index.html"))

class InterceptHandler(logging.Handler):
	def emit(self, record: logging.LogRecord) -> None:
		if not record.name.startswith('apscheduler'):
			return
			#logger.debug(record.getMessage())
		# Get corresponding Loguru level if it exists.
		level: str | int
		try:
			level = logger.level(record.levelname).name
		except ValueError:
			level = record.levelno

		# Find caller from where originated the logged message.
		frame, depth = inspect.currentframe(), 0
		while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
			frame = frame.f_back
			depth += 1
		level = 'DEBUG' if level == 'INFO' else level
		logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def configureLogging(requestedLogLevel, logScheduler):
	loglevel = 'INFO'
	if requestedLogLevel not in ValidLogLevels and requestedLogLevel != None:
		print(f'Log Level {requestedLogLevel} is not valid!')
	elif requestedLogLevel != None:
		loglevel = requestedLogLevel
	
	logFormat = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> |"
	if loglevel == 'DEBUG':
		logFormat += "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
	logFormat += "<level>{message}</level>"

	log_directory = "logs"
	if not os.path.exists(log_directory):
		os.makedirs(log_directory)
	log_file_name = os.path.join(log_directory, "optrabot_{time:YYYY-MM-DD}.log")

	logger.remove()
	logger.add(sys.stderr, level=loglevel, format = logFormat)
	#logger.add("optrabot.log", level='DEBUG', format = logFormat, rotation="5 MB", retention="10 days")
	logger.add(
        log_file_name,
        level='DEBUG',
        format=logFormat,
        rotation="00:00",  # Täglich um Mitternacht rotieren
        retention="10 days"  # Log-Dateien für 10 Tage aufbewahren
    )

	if logScheduler:
		logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
	#logging.basicConfig(level=logging.ERROR)  # Stummschalten aller Standard-Logger
		apscheduler_logger = logging.getLogger('apscheduler')
		apscheduler_logger.setLevel(loglevel)
	#handler = logging.StreamHandler(sys.stdout)
	#handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
	#apscheduler_logger.addHandler(handler)

def perform_update():
	"""
	Performs the update of the OptraBot package
	"""
	logger.info('Updating OptraBot')
	
	# Prüfen ob OptraBot mit UV gestartet wurde (sys.executable enthält 'uv' im Pfad)
	is_uv_environment = 'uv' in sys.executable.lower()
	logger.debug(f'Running in UV environment: {is_uv_environment}')
	
	if is_uv_environment:
		import tempfile

		# On Windows, create a batch script to update after exit
		if sys.platform == 'win32':
			
			# Create temporary batch file
			batch_content = '@echo off\n'
			batch_content += 'echo Updating OptraBot...\n'
			batch_content += 'timeout /t 2 /nobreak >nul\n'
			batch_content += 'echo Clearing UV cache for OptraBot...\n'
			batch_content += 'uv cache clean optrabot\n'
			batch_content += 'timeout /t 1 /nobreak >nul\n'
			batch_content += 'echo Starting update...\n'
			# Use --force to reinstall even if same version, ensures fresh install from test.pypi
			#batch_content += 'uv tool install --force --index-url https://pypi.org/simple/ --extra-index-url https://test.pypi.org/simple/ --prerelease=allow --index-strategy unsafe-best-match optrabot\n'
			batch_content += 'uv tool upgrade optrabot\n'
			batch_content += 'if errorlevel 1 (\n'
			batch_content += '    echo Update failed!\n'
			batch_content += '    pause\n'
			batch_content += '    exit /b 1\n'
			batch_content += ')\n'
			batch_content += 'echo Update complete! Restarting OptraBot...\n'
			# Add --yes flag to skip update prompt after restart
			arguments = sys.argv[1:]
			if '--yes' not in arguments:
				arguments.insert(0, '--yes')
			# Use /D to set working directory to current directory
			# This ensures config.yaml is found after restart
			batch_content += f'optrabot {" ".join(arguments)}\n'
			batch_content += 'del "%~f0"\n'
			
			batch_file = tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False)
			batch_file.write(batch_content)
			batch_file.close()
			
			logger.info('OptraBot will update after closing...')
			# Start batch file and exit immediately	
			os.startfile(batch_file.name)
			exit(0)
		else:
			# On macOS/Linux, create a shell script to update after exit
			# Create temporary shell script
			shell_content = '#!/bin/bash\n'
			shell_content += 'echo "Updating OptraBot..."\n'
			shell_content += 'sleep 2\n'
			shell_content += 'echo "Clearing UV cache for OptraBot..."\n'
			shell_content += 'uv cache clean optrabot\n'
			shell_content += 'sleep 1\n'
			shell_content += 'echo "Starting update..."\n'
			# Use --force to reinstall even if same version, ensures fresh install from test.pypi
			#shell_content += 'uv tool install --force --index-url https://pypi.org/simple/ --extra-index-url https://test.pypi.org/simple/ --prerelease=allow --index-strategy unsafe-best-match optrabot\n'
			shell_content += 'uv tool upgrade optrabot\n'
			shell_content += 'if [ $? -ne 0 ]; then\n'
			shell_content += '    echo "Update failed!"\n'
			shell_content += '    read -p "Press Enter to exit..."\n'
			shell_content += '    exit 1\n'
			shell_content += 'fi\n'
			shell_content += 'echo "Update complete! Restarting OptraBot..."\n'
			# Add --yes flag to skip update prompt after restart
			arguments = sys.argv[1:]
			if '--yes' not in arguments:
				arguments.insert(0, '--yes')
			shell_content += f'optrabot {" ".join(arguments)} &\n'
			shell_content += 'rm -- "$0"\n'
			
			shell_file = tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False)
			shell_file.write(shell_content)
			shell_file.close()
			
			# Make script executable
			os.chmod(shell_file.name, 0o755)
			
			logger.info('OptraBot will update after closing...')
			# Start shell script and exit immediately
			subprocess.Popen([shell_file.name])
			exit(0)
	else:
		python_executable = sys.executable
		cmd = [python_executable, '-m', 'pip', 'install', '--no-cache-dir', '-U', 'optrabot']
		logger.debug(f'Executing update command: {' '.join(cmd)}')
		subprocess.run(cmd, check=True)
		args = [python_executable, '-m', 'optrabot.main'] + sys.argv[1:]
		logger.info('Restarting OptraBot')
		logger.debug(f'Executing restart command: {args[0]}')
		logger.debug(f'With arguments: {args}')
		os.execvp(args[0], args)

def check_for_update(skip_prompt: bool = False):
	"""
	Check for an updated version of the OptraBot package
	"""
	# Skip update check if --yes flag was passed (e.g., after auto-update)
	if skip_prompt:
		return
		
	try:
		installed_version = get_version()
		ssl_context = ssl.create_default_context(cafile=certifi.where())
		content = str(urllib.request.urlopen('{}/simple/{}/'.format('https://pypi.org', 'optrabot'), context=ssl_context).read())
		# Versionen mit Vorabversionen Pattern: '([^-<>]+).tar.gz'
		# versions = re.findall(r'([^-<>]+).tar.gz', content)
		# Versionen ohne Vorabversionen Pattern: r'(\d+\.\d+\.\d+)\.tar\.gz'
		versions = re.findall(r'(\d+\.\d+\.\d+)\.tar\.gz', content) 
		latest_version = versions[-1]
		if Version(latest_version) > Version(installed_version):
			logger.info(f"You're running OptraBot version {installed_version}. New version of OptraBot is available: {latest_version}")
			try:
				if inquirer.confirm(message="Do you want to Update now?", default=True).execute():
					perform_update()
			except KeyboardInterrupt as excp:
				exit(0)

	except Exception as excp:
		logger.error("Problem checking for updates: {}", excp)

def check_python_version() -> None:
	"""
	Check if the Python version is supported based on pyproject.toml requirements.
	Warns if the current Python version is outside the specified range.
	"""
	major = sys.version_info.major
	minor = sys.version_info.minor
	micro = sys.version_info.micro
	current_version = f'{major}.{minor}.{micro}'
	
	logger.debug(f'Running on Python {current_version}')
	
	try:
		# Read pyproject.toml to get the required Python version
		current_file_path = Path(__file__).resolve()
		project_root = current_file_path.parent.parent
		pyproject_path = project_root / 'pyproject.toml'
		
		if not pyproject_path.exists():
			logger.debug('pyproject.toml not found, skipping version check')
			return
		
		yaml = YAML()
		with open(pyproject_path, encoding='utf-8') as f:
			pyproject_data = yaml.load(f)
		
		requires_python = pyproject_data.get('project', {}).get('requires-python', '')
		
		if not requires_python:
			logger.debug('No requires-python specified in pyproject.toml')
			return
		
		# Parse the version specifier
		spec = SpecifierSet(requires_python)
		
		# Check if current version is in the allowed range
		if current_version not in spec:
			logger.warning(
				f'OptraBot is running on Python {major}.{minor}, which is outside the supported range {requires_python}. '
				f'You may experience unexpected behavior.'
			)
		else:
			logger.debug(f'Python version {current_version} is within supported range {requires_python}')
			
	except Exception as excp:
		logger.debug(f'Error checking Python version requirements: {excp}')


def run():
	"""Entry point for the optrabot CLI command"""
	parser = argparse.ArgumentParser()
	parser.add_argument("--loglevel", help="Log Level", choices=ValidLogLevels)
	parser.add_argument("--logscheduler", help="Log Job Scheduler", action="store_true")
	parser.add_argument("--yes", "-y", help="Skip update prompt (used after auto-update)", action="store_true")
	args = parser.parse_args()
	configureLogging(args.loglevel, args.logscheduler)
	check_python_version()
	check_for_update(skip_prompt=args.yes)
	if optrabotcfg.ensureInitialConfig()	== True:
		# Get web port from config
		configuration = optrabotcfg.Config("config.yaml")
		if configuration.loaded == False:
			print("Configuration error. Unable to run OptraBot!")
			sys.exit(1)
		webPort: int
		try:
			webPort = configuration.get('general.port')
		except KeyError as keyErr:
			webPort = 8080
		uvicorn_log_level = args.loglevel.lower() if args.loglevel else 'error'
		# Show access logs only in debug/trace mode
		show_access_log = uvicorn_log_level in ('debug', 'trace')
		uvicorn.run('optrabot.main:app', port=int(webPort), host='0.0.0.0', log_level=uvicorn_log_level, access_log=show_access_log)
	else:
		print("Configuration error. Unable to run OptraBot!")

if __name__ == '__main__':
	run()