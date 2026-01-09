import json
from .base import BaseAgent
from ..llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage

class ResponseAgent(BaseAgent):
    """
    Generates the final response to the user.
    """
    def run(self):
        self.log("Generating user response...")
        
        system_prompt = self.read_prompt('response', 'prompt')
        llm = get_llm(temperature=0.7) 
        
        context = f"User Request: {self.task_log.user_request}\n\nLog:\n{self.task_log.result_summary}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=context)
        ]
        
        try:
            response = llm.invoke(messages)
            final_response = response.content
            
            self.task_log.result_summary = final_response
            self.task_log.save()
            
            return "responded"

        except Exception as e:
            self.log(f"Error generating response: {str(e)}")
            self.update_task_log(status='failed', error_message=str(e))
            return "failed"
