from typing import Dict, Any
from base_agent import BaseAgent
import asyncio
import json
from copy import deepcopy

class ClassificationAgent(BaseAgent):
    def __init__(self): 
        super().__init__(
            name="Classification_Agent", 
            instructions="""You are a helpful AI assistant for a coffee shop application.
            Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
            1. details_agent: This agent is responsible for answering questions about the coffee shop, like location, delivery places, working hours, details about menue items. Or listing items in the menu items. Or by asking what we have.
            2. order_taking_agent: This agent is responsible for taking orders from the user. It's responsible to have a conversation with the user about the order untill it's complete.
            3. recommendation_agent: This agent is responsible for giving recommendations to the user about what to buy. If the user asks for a recommendation, this agent should be used.

            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "decision": "details_agent" or "order_taking_agent" or "recommendation_agent". Pick one of those. and only write the word.
            "message": leave the message empty.
            }""", 
        )
    
    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant", 
            "content": output["message"], 
            "memory": {
                "agent": "classification_agent", 
                "classification_decision": output['decision']
            }
        }

        return dict_output

    def run(self, messages):
        messages = deepcopy(messages)

        input_messages = [{'role': "system", "content":self.instructions}] + messages
        output = self.get_chatbot_response(str(input_messages))
        output = self.postprocess(output)
        return output 