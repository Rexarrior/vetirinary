from .base import BaseAgent

class ResponseAgent(BaseAgent):
    """
    Generates the final response to the user.
    """
    def run(self):
        self.log("Generating user response...")
        # TODO: Generate response
        
        self.task_log.result_summary = "Task completed. See report for details."
        self.task_log.save()
        
        return "responded"
