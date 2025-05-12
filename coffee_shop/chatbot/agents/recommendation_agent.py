from typing import Dict, Any
from base_agent import BaseAgent
import asyncio
import json
from copy import deepcopy

class RecommendationAgent(BaseAgent):
    def __init__(self): 
        super().__init__(
            name="Recommendation_Agent", 
            instructions="""
        You are a helpful AI assistant for a coffee shop application which serves drinks and pastries. We have 3 types of recommendations:

        1. Apriori Recommendations: These are recommendations based on the user's order history. We recommend items that are frequently bought together with the items in the user's order.
        2. Popular Recommendations: These are recommendations based on the popularity of items in the coffee shop. We recommend items that are popular among customers.
        3. Popular Recommendations by Category: Here the user asks to recommend them product in a category. Like what coffee do you recommend me to get?. We recommend items that are popular in the category of the user's requested category.
        
        Here is the list of items in the coffee shop:
        """+ ",".join(self.products) + """
        Here is the list of Categories we have in the coffee shop:
        """ + ",".join(self.product_categories) + """

        Your task is to determine which type of recommendation to provide based on the user's message.

        Your output should be in a structured json format like so. Each key is a string and each value is a string. Make sure to follow the format exactly:
        {
        "chain of thought": Write down your critical thinking about what type of recommendation is this input relevant to.
        "recommendation_type": "apriori" or "popular" or "popular by category". Pick one of those and only write the word.
        "parameters": This is a  python list. It's either a list of of items for apriori recommendations or a list of categories for popular by category recommendations. Leave it empty for popular recommendations. Make sure to use the exact strings from the list of items and categories above.
        }
        """, 
    )

    with open("..\datasets\apriori_recommendations.json", 'r') as file:
        self.apriori_recommendations = json.load(file)
    
    self.popular_recommendations = pd.read_csv("..\datasets\popularity.csv")
    self.products = self.popular_recommendations['product'].tolist()
    self.product_categories = self.popular_recommendations['product_category'].tolist()
    
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

    def get_popular_recommendations(self, product_categories=None, top_k=5):
        recommendation_df = self.popular_recommendations 

        if type(product_categories) == str: 
            product_categories = [product_categories]
        
        if product_categories is not None: 
            recommendation_df = self.popular_recommendations[self.popular_recommendations['product_category'].isin(product_categories)]