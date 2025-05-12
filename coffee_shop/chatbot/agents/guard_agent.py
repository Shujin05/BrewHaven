from typing import Dict, Any
from base_agent import BaseAgent
import asyncio
import json
from copy import deepcopy

class GuardAgent(BaseAgent):
    def __init__(self): 
        super().__init__(
            name="Guard_Agent", 
            instructions="""You are a helpful AI assistant for an online coffee shop called Brew Haven, which sells drinks and pastries.
Your task is to determine if the user is asking something relevant to the coffee shop or not. 
The user is allowed to:
1. ask questions about the coffee shop (for example: location, working hours, menu items, any questions related to Brew Haven)
2. ask questions about menu items, they can ask for the ingredients in an item and more details such as the price 
3. ask for recommendations of what to buy 
4. make an order 

The user is not allowed to:
1. ask questions about anything else other than Brew Haven or any Brew Haven-related information 
2. ask questions about the staff or how to make a certain menu item 

Your output should be in a structured json format like so: each key is a string, and each value is a string. 
Make sure to follow the format exactly. 
{
"decision": "allowed" or "not allowed". Pick one of those and only write the word with no punctuation. 
""", 
    )
    def postprocess(self, output):
        output = json.loads(output)

        dict_output = {
            "role": "assistant", 
            "memory": {
                "agent": "guard_agent", 
                "guard_decision": output['decision']
            }
        }

        return dict_output

    def run(self, messages):
        messages = deepcopy(messages)
        input_messages = [{'role': "system", "content":self.instructions}] + messages
        output = self.get_chatbot_response(str(input_messages))
        print(output)
        output = self.postprocess(output)
        return output 


