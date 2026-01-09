import json
from .base import BaseAgent
from ..llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from .agent_tools.admin.tools import list_objects, get_object

class ControlAgent(BaseAgent):
    """
    Verifies the results of the Admin Agent.
    """
    def run(self):
        self.log("Verifying task results...")
        
        system_prompt = self.read_prompt('control', 'prompt')
        llm = get_llm(temperature=0.0)
        tools = [list_objects, get_object]
        
        agent = create_react_agent(llm, tools, prompt=system_prompt)
        
        # The result_summary contains the Admin Agent's report now
        context = f"User Request: {self.task_log.user_request}\n\n{self.task_log.result_summary}"
        
        messages = [
            HumanMessage(content=context)
        ]
        
        try:
            result = agent.invoke({"messages": messages})
            
            if result and "messages" in result:
                last_message = result["messages"][-1]
                return self.process_control_response(last_message.content)
            else:
                 raise ValueError("No messages returned from agent")

        except Exception as e:
            self.log(f"Error during verification: {str(e)}")
            self.update_task_log(status='failed', error_message=str(e))
            return "failed"

    def process_control_response(self, content):
        self.log(f"Control Agent finished. Response: {content[:100]}...")
        
        if "VERDICT: VERIFIED" in content:
            # Append verification report
            current_summary = self.task_log.result_summary
            new_summary = f"{current_summary}\n\nVerification Report:\n{content}"
            
            self.update_task_log(
                status='reporting',
                current_agent='DescriptionAgent',
                result_summary=new_summary
            )
            return "verified"
        elif "VERDICT: RETRY" in content:
            self.log("Verification failed.")
            self.update_task_log(status='failed', error_message=f"Verification failed: {content}")
            return "retry"
        else:
            self.log("Unknown verdict.")
            self.update_task_log(status='failed', error_message="Control Agent did not return a clear verdict.")
            return "failed"
