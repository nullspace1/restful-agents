from model.agent_provider import AgentProvider
from model.message import Message
from huggingface_hub import InferenceClient
from typing import Any


class HuggingFaceAgentProvider(AgentProvider):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key
        # create client once and reuse
        self.client = InferenceClient(api_key=self.api_key)

    def send_message(self, messages: list[Message]) -> str:
        """Send a list of `Message` to the Hugging Face chat completion endpoint and
        return the agent's textual response.
        """
        # print the current messages for debugging
        print("Sending messages to Hugging Face API:")
        for m in messages:
            print(f"  {m.role}: {m.content}")
        
        # Convert internal Message objects to HF chat message dicts
        hf_messages: list[dict[str,str]] = []
        for m in messages:
            # keep roles as-is (system/user/assistant/agent)
            hf_messages.append({"role": self.get_role(m), "content": str(m.content)})

        # Call the Hugging Face chat/completions API
        completion: Any = self.client.chat.completions.create( # pyright: ignore[reportUnknownMemberType]
            model=self.model_name,
            messages=hf_messages,
        ) # 

        # Try to extract the textual content in common response shapes
        try:
            choice: Any = completion.choices[0]
            # HF SDK may return the message as `choice.message.content` or `choice.text`
            if hasattr(choice, "message") and getattr(choice.message, "content", None) is not None:
                response = str(choice.message.content)
            if hasattr(choice, "text"):
                response = str(choice.text)
            # Fallback to stringifying the choice
            response = str(choice)
            print(f"Received response from Hugging Face API: {response}")
            return response
        except Exception:
            # Fallback: stringify full completion
            return str(completion)

    def count_tokens(self, messages: list[Message]) -> int:
        """A simple token estimator: count whitespace-separated tokens across messages.
        This is intentionally lightweight; replace with a model-specific tokenizer
        if more accurate accounting is needed.
        """
        total = 0
        for m in messages:
            if not m or not m.content:
                continue
            total += len(m.content.split())
        return total
    
    def get_role(self, message: Message) -> str:
        if message.role == "agent":
            return "assistant"
        return message.role
            