from openai import OpenAI
import os
import pandas as pd
import time

class ChatBot:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def make_request(self, msg_content, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": msg_content}]
        response = self.client .chat.completions.create(
            model=model,
            messages=messages,
            temperature=0)
        response_msg = response.choices[0].message.content
        return response_msg

# chatbot = ChatBot()
# chatbot.make_request("Say this is a test!")


