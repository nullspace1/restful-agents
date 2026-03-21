import datetime

from model.agent import Agent
from model.parameter import ParameterTemplate
from providers.huggingface import HuggingFaceAgentProvider
from resources.skill import skill



agent : Agent = Agent(
    name="Test Agent", 
    description="An agent for testing the API and resource system.",
    provider=HuggingFaceAgentProvider(
        model_name="openai/gpt-oss-120b:groq",
        api_key="hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ))

book_date = skill(
    owner=agent,
    name="skills/book",
    description="Creating a booking on a specific date",
    param_templates=[
        ParameterTemplate("title", "The title of the booking",  converter=str, required=True),
        ParameterTemplate("date", "The date of the booking in ISO format",  converter=lambda str_date: datetime.datetime.fromisoformat(str_date), required=True),
        ],
    func=lambda params: {"result": "Booking completed: " + params["title"]}
)

agent.add_to_local_api(book_date)

response = agent.message("Hello, I need you to book a meeting on 2023-01-01.")

print(response)