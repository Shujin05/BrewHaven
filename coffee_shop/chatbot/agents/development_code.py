from guard_agent import GuardAgent
from classification_agent import ClassificationAgent
from details_agent import DetailsAgent
import os 

if __name__ == "__main__":
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    details_agent = DetailsAgent()

    while True: 
        prompt = input("User: ")
        messages = [{"role": "user", "content": str(prompt)}]
        guard_agent_response = guard_agent.run(messages)
    
        #Guard Agent's response
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            continue

        # Classification Agent's response 
        classification_agent_response = classification_agent.run(messages)
        chosen_agent = classification_agent_response["memory"]["classification_decision"]
        print("chosen agent: " + chosen_agent)

        # get chosen agent's response 
        if chosen_agent == "details_agent": 
            details_agent_response = details_agent.run(messages)
            print(details_agent_response)