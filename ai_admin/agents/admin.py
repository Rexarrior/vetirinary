import json
from .base import BaseAgent
from ..llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from .agent_tools.admin.tools import (
    get_all_model_names, get_model_schema, list_objects, 
    get_object, create_object, update_object, delete_object
)

class AdminAgent(BaseAgent):
    """
    Executes administrative tasks on the database.
    """
    def run(self):
        self.log("Executing admin task...")
        
        # Load system prompt
        system_prompt = self.read_prompt('admin', 'prompt')

        # Initialize LLM and Tools
        llm = get_llm(temperature=0.0)
        tools = [
            get_all_model_names, get_model_schema, list_objects, 
            get_object, create_object, update_object, delete_object
        ]
        
        # Create Agent
        agent = create_react_agent(llm, tools, prompt=system_prompt)

        # Prepare input
        # The task description comes from the AnalysisAgent's result_summary or the original user request
        # But AnalysisAgent updates result_summary with task_description.
        task_description = self.task_log.result_summary or self.task_log.user_request
        
        messages = [
            HumanMessage(content=f"Task: {task_description}")
        ]

        try:
            # Invoke Agent
            result = agent.invoke({"messages": messages})
            
            # Extract final response from the last message
            if result and "messages" in result:
                last_message = result["messages"][-1]
                return self.process_admin_response(last_message.content)
            else:
                 raise ValueError("No messages returned from agent")

        except Exception as e:
            self.log(f"Error during execution: {str(e)}")
            self.update_task_log(status='failed', error_message=str(e))
            return "failed"

    def process_admin_response(self, content):
        """
        Process the response from the Admin Agent.
        """
        self.log(f"Admin Agent finished. Response: {content[:100]}...")
        
        # We assume if the agent finished without error, it's ready for verification
        # The content is the summary of what was done.
        
        # We append the admin's summary to the result_summary
        current_summary = self.task_log.result_summary
        new_summary = f"{current_summary}\n\nExecution Report:\n{content}"
        
        self.update_task_log(
            status='verifying',
            current_agent='ControlAgent',
            result_summary=new_summary
        )
        return "executed"
