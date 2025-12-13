import os
import signal

from fastapi import APIRouter, HTTPException
from loguru import logger

from optrabot import config as optrabotcfg
from optrabot.tradetemplate.templatefactory import Template

router = APIRouter(prefix="/api")

@router.get("/templates/")
def get_templates():
	"""
	Returns 
	"""
	config :optrabotcfg.Config = optrabotcfg.appConfig
	try:
		config :optrabotcfg.Config = optrabotcfg.appConfig
		template_list = []
		template_id = 0
		for item in config.getTemplates():
			template : Template = item
			template_list.append({
                "Id": template_id,
                "Name": template.name,
                "Strategy": template.strategy,
                "Account": template.account,
				"Type": template.getType(),
                "Enabled": template.is_enabled(),
                "Group": template.template_group,
                "DTE": template.dte,
                "Amount": template.amount,
            })
			logger.debug(f"Template {template_id}: {template.name}, Strategy: {template.strategy}, Type: {template.getType()}, Enabled: {template.is_enabled()}")
			template_id += 1
		return template_list
		#return {"templates": ["template1", "template2"]}
		pass
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates/{template_id}")
def get_template(template_id: str) -> dict:
	"""
	Returns details for a specific template
	"""
	try:
		templates = optrabotcfg.appConfig.getTemplates()
		template: Template = templates[int(template_id)]
		return {
			"Id": template_id,
			"Name": template.name,
			"Strategy": template.strategy,
			"Type": template.getType(),
			"Enabled": template.is_enabled(),
			"Group": template.template_group,
			"DTE": template.dte,
		}
	except KeyError:
		raise HTTPException(status_code=404, detail=f"Template {template_id} not found")
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.post("/shutdown")
async def shutdown_optrabot():
	"""
	Shutdown the OptraBot application
	"""
	try:
		# Import app hier, um zirkulären Import zu vermeiden
		from optrabot.main import app

		# Rufe die shutdown-Methode der OptraBot-Instanz auf
		await app.optraBot.shutdown()
		
		# Verzögerung um sicherzustellen, dass die Antwort gesendet wird
		# bevor der Prozess beendet wird
		import asyncio
		asyncio.create_task(delayed_shutdown())
		
		return {
			"message": "OptraBot shutdown successful", 
			"status": "success"
		}
	except Exception as e:
		logger.error(f"Error during shutdown: {e}")
		raise HTTPException(status_code=500, detail=str(e))

async def delayed_shutdown():
	"""Verzögerter Shutdown um sicherzustellen, dass die HTTP-Antwort gesendet wird"""
	import asyncio
	await asyncio.sleep(1)  # 1 Sekunde warten
	os.kill(os.getpid(), signal.SIGTERM)