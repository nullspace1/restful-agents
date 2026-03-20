from model.agent import Agent
from providers.huggingface import HuggingFaceAgentProvider


agent : Agent = Agent(
    name="Test Agent", 
    description="An agent for testing the API and resource system.",
    provider=HuggingFaceAgentProvider(
        model_name="openai/gpt-oss-120b:groq",
        api_key="yeah my dumbass totally didn't try to push with the api key still here"
    ))

response = agent.message("Hello. This is a test message. Please let me know if you have been able to receive it, along with your name and toolset.")

response_2 = agent.message("Good!. Please try to write something to the preloaded text file")

response_3 = agent.message("Now, please read the content of the text file and tell me what it says.")

print("Agent response:")
print(response)
print(response_2)
print(response_3)