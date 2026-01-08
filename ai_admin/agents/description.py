from .base import BaseAgent
from ..models import TaskReport
from django.utils.text import slugify
from django.utils import timezone

class DescriptionAgent(BaseAgent):
    """
    Generates an HTML report of the task.
    """
    def run(self):
        self.log("Generating report...")
        # TODO: Generate real HTML report
        
        report_content = "<h1>Task Report</h1><p>Task completed successfully.</p>"
        slug = slugify(f"task-{self.task_log.id}-{timezone.now().strftime('%Y%m%d-%H%M%S')}")
        
        TaskReport.objects.create(
            task=self.task_log,
            slug=slug,
            html_content=report_content
        )
        
        self.task_log.status = 'completed'
        self.task_log.current_agent = 'ResponseAgent'
        self.task_log.save()
        
        return "reported"
