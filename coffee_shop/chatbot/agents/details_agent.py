from typing import Dict, Any
from base_agent import BaseAgent
import json
from copy import deepcopy
from pymongo import MongoClient

class DetailsAgent(BaseAgent):
    def __init__(self): 
        super().__init__(
            name="Details_Agent", 
            instructions="""
            You are a customer support agent for a coffee shop called Brew Haven
            You should answer every question as if you are a knowledgeable employee of the shop
            and provide the necessary information to the user regarding their orders. 

            Please refer strictly to the context given. Do NOT provide information that is made up. 
            Be concise in your answer. 
            """
    )
        self.mongo_client = MongoClient('mongodb+srv://limshujin:Shujin2005@cluster0.251xl.mongodb.net/coffee_shop')
        self.db = self.mongo_client["food"]

    def fetch_data(self):
        # fetches all data on menu items
        try: 
            data = list(self.db.find({}))
            return data 
        except Exception as e: 
            print(f"error fetching data: {e}")
        
    def postprocess(self, output):
        dict_output = {
            "role": "assistant", 
            "content": output, 
            "memory": {
                "agent": "details_agent", 
            }
        }

        return dict_output

    def run(self, messages):
        messages = deepcopy(messages)
        menu_items = self.fetch_data

        prompt = [f"""Using the context below, answer the query: 
        context: {menu_items}
        query: {messages}
        """, ]
        input_messages = [{'role': "system", "content":self.instructions}] + prompt

        output = self.get_chatbot_response(str(input_messages))
        output = self.postprocess(output)
        return output 