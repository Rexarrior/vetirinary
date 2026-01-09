from celery import shared_task
from .models import TaskLog
from .agents.analysis import AnalysisAgent
from .agents.admin import AdminAgent
from .agents.control import ControlAgent
from .agents.description import DescriptionAgent
from .agents.response import ResponseAgent
import logging

logger = logging.getLogger(__name__)

@shared_task
def start_admin_task(task_log_id):
    """
    Entry point for the AI Admin Agent workflow.
    """
    try:
        task_log = TaskLog.objects.get(id=task_log_id)
        logger.info(f"Starting admin task {task_log_id}")
        
        # 1. Analysis Agent
        task_log.status = 'analyzing'
        task_log.current_agent = 'AnalysisAgent'
        task_log.save()
        
        analysis_agent = AnalysisAgent(task_log)
        result = analysis_agent.run()
        
        if result == "dialog_only":
            task_log.status = 'completed' # Or 'dialog_only' if we want to distinguish
            task_log.current_agent = 'Completed'
            task_log.save()
            logger.info(f"Task {task_log_id} completed as dialog only")
            return
        elif result != "proceed":
            logger.info(f"Task {task_log_id} halted by AnalysisAgent: {result}")
            return

        # 2. Admin Agent
        # Status update is handled by AnalysisAgent or previous step, but we ensure it here
        if task_log.status != 'executing':
             task_log.status = 'executing'
             task_log.current_agent = 'AdminAgent'
             task_log.save()
        
        admin_agent = AdminAgent(task_log)
        result = admin_agent.run()
        if result != "executed":
            logger.info(f"Task {task_log_id} halted by AdminAgent: {result}")
            return

        # 3. Control Agent
        # AdminAgent updates status to 'verifying', but we ensure it
        if task_log.status != 'verifying':
             task_log.status = 'verifying'
             task_log.current_agent = 'ControlAgent'
             task_log.save()
        
        control_agent = ControlAgent(task_log)
        result = control_agent.run()
        if result != "verified": # Assuming ControlAgent returns "verified" or "retry"
             logger.info(f"Task {task_log_id} halted by ControlAgent: {result}")
             return

        # 4. Description Agent
        task_log.status = 'reporting'
        task_log.current_agent = 'DescriptionAgent'
        task_log.save()
        
        description_agent = DescriptionAgent(task_log)
        description_agent.run()

        # 5. Response Agent
        task_log.status = 'completed'
        task_log.current_agent = 'ResponseAgent'
        task_log.save()
        
        response_agent = ResponseAgent(task_log)
        response_agent.run()
        
        logger.info(f"Task {task_log_id} completed successfully")
        
    except TaskLog.DoesNotExist:
        logger.error(f"TaskLog {task_log_id} not found")
    except Exception as e:
        logger.error(f"Error in start_admin_task: {e}")
        if 'task_log' in locals():
            task_log.status = 'failed'
            task_log.error_message = str(e)
            task_log.save()
