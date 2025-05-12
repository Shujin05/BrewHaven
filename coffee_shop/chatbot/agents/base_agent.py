from typing import Dict, Any
import json 
from openai import OpenAI

class BaseAgent:
    def __init__(self, name: str, instructions: str):
        self.name = name 
        self.instructions = instructions 
        self.client = OpenAI(
            base_url = "http://localhost:11434/v1", 
            api_key = "ollama"
        )
        self.model = "llama3.2"
    

    def run(self, messages: list) -> Dict[str, Any]:
        """Default method to be overridden by child classes"""
        raise NotImplementedError("Subclasses must implement run()")
    
    def get_chatbot_response(self, prompt: str) -> str: 
        """Query Ollama model with the given prompt"""
        try: 
            response=self.client.chat.completions.create(
                model=self.model, 
                messages=[
                    {"role": "system", "content":self.instructions},
                    {"role": "user", "content": prompt}, 
                ], 
                temperature=0.7, 
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error querying Ollama: {str(e)}")
    
    def postprocess(self, text: str) -> Dict[str, Any]:
        """parse JSON from text while handling potential errors"""
        try: 
            #find JSON-like content between curly braces
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                json_str = text[start: end +1]
                return json.loads(json_str)
            return {"error": "No JSON content found"}
        
        except json.JSONDecodeError: 
            return {"error": "Invalid JSON content"}

