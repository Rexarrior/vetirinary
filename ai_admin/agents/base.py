from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the AI Admin workflow.
    """
    def __init__(self, task_log):
        self.task_log = task_log

    @abstractmethod
    def run(self):
        """
        Execute the agent's logic.
        """
        pass

    def log(self, message):
        """
        Log a message to the task log (or standard logger).
        """
        logger.info(f"[Task {self.task_log.id}] {self.__class__.__name__}: {message}")

    def read_prompt(self, agent_name, prompt_name):
        """
        Read a prompt file from the agents/prompts directory.
        """
        from django.conf import settings
        import os
        prompt_path = os.path.join(settings.BASE_DIR, 'ai_admin', 'agents', 'prompts', agent_name, f'{prompt_name}.md')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_json_from_agent_response(self, content):
        """
        Extract JSON from a markdown code block in the agent's response.
        """
        import json
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            self.log(f"Failed to parse JSON from content: {content[:100]}...")
            raise

    def update_task_log(self, status=None, current_agent=None, result_summary=None, error_message=None):
        """
        Update the task log with the provided fields.
        """
        if status:
            self.task_log.status = status
        if current_agent:
            self.task_log.current_agent = current_agent
        if result_summary is not None:
            self.task_log.result_summary = result_summary
        if error_message is not None:
            self.task_log.error_message = error_message
        self.task_log.save()
