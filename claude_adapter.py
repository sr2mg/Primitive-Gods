import os
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()

class ClaudeAdapter:
    def __init__(self):
        if os.environ.get("ANTHROPIC_API_KEY") is None:
            raise ValueError("ANTHROPIC_API_KEY is not set")
        self.client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
        
    def generate(self,prompt:str,max_new_tokens:int=100) ->str:
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_new_tokens
        )
        return response.content[0].text


if __name__ == "__main__":
    adapter = ClaudeAdapter()
    print(adapter.generate("こんにちは"))


