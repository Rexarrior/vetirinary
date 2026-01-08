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
