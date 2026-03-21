from model.agent import Agent
from providers.huggingface import HuggingFaceAgentProvider


agent : Agent = Agent(
    name="Test Agent", 
    description="An agent for testing the API and resource system.",
    provider=HuggingFaceAgentProvider(
        model_name="openai/gpt-oss-120b:groq",
        api_key="yeah my dumbass totally didn't try to push with the api key still here"
    ))