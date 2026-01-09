import json
from .base import BaseAgent
from ..llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from .agent_tools.analysis.tools import get_chat_history, get_task_list, get_task_details

class AnalysisAgent(BaseAgent):
    """
    Analyzes the user request and determines the next steps.
    """
    def run(self):
        self.log("Analyzing user request...")
        
        # Load system prompt
        system_prompt = self.read_prompt('analysis', 'system')

        # Initialize LLM and Tools
        llm = get_llm(temperature=0.0)
        tools = [get_chat_history, get_task_list, get_task_details]
        
        # Create Agent
        agent = create_react_agent(llm, tools, prompt=system_prompt)

        # Prepare input
        messages = [
            HumanMessage(content=f"User Request: {self.task_log.user_request}")
        ]

        try:
            # Invoke Agent
            result = agent.invoke({"messages": messages})
            
            # Extract final response from the last message
            if result and "messages" in result:
                last_message = result["messages"][-1]
                return self.process_analysis_response(last_message.content)
            else:
                 raise ValueError("No messages returned from agent")

        except Exception as e:
            self.log(f"Error during analysis: {str(e)}")
            self.update_task_log(status='failed', error_message=str(e))
            return "failed"

    def process_analysis_response(self, content):
        """
        Process the JSON response from the Analysis Agent.
        """
        try:
            decision_data = self.extract_json_from_agent_response(content)
            decision = decision_data.get('decision')
            reasoning = decision_data.get('reasoning')
            
            self.log(f"Decision: {decision}. Reasoning: {reasoning}")
            
            if decision == 'proceed':
                self.update_task_log(
                    status='executing',
                    current_agent='AdminAgent',
                    result_summary=decision_data.get('task_description', '')
                )
                return "proceed"
                
            elif decision in ['clarify', 'dialog_only']:
                self.update_task_log(
                    status='dialog_only',
                    current_agent='ResponseAgent',
                    result_summary=decision_data.get('user_response', '')
                )
                return "dialog_only"
            
            else:
                self.log(f"Unknown decision: {decision}")
                self.update_task_log(status='failed', error_message=f"Unknown decision: {decision}")
                return "failed"

        except Exception as e:
            self.log(f"Failed to process analysis response: {str(e)}")
            self.update_task_log(status='failed', error_message=f"Response processing error: {str(e)}")
            return "failed"
