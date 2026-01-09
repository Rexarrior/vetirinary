import json
from .base import BaseAgent
from ..llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from ..models import TaskReport
from django.utils.text import slugify
from django.utils import timezone

class DescriptionAgent(BaseAgent):
    """
    Generates an HTML report of the task.
    """
    def run(self):
        self.log("Generating report...")
        
        system_prompt = self.read_prompt('description', 'prompt')
        llm = get_llm(temperature=0.0)
        
        context = f"User Request: {self.task_log.user_request}\n\nLog:\n{self.task_log.result_summary}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=context)
        ]
        
        try:
            response = llm.invoke(messages)
            report_content = response.content
            
            # Clean up markdown code blocks if present
            if "```html" in report_content:
                report_content = report_content.split("```html")[1].split("```")[0].strip()
            elif "```" in report_content:
                report_content = report_content.split("```")[1].split("```")[0].strip()
            
            slug = slugify(f"task-{self.task_log.id}-{timezone.now().strftime('%Y%m%d-%H%M%S')}")
            
            TaskReport.objects.create(
                task=self.task_log,
                slug=slug,
                html_content=report_content
            )
            
            return "reported"

        except Exception as e:
            self.log(f"Error generating report: {str(e)}")
            self.update_task_log(status='failed', error_message=str(e))
            return "failed"
