from openai import OpenAI
import os
import pandas as pd
import time

class ChatBot:
    def __init__(self):
        self.client = OpenAI(api_key='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')
    
    def make_request(self, msg_content, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": msg_content}]
        print(msg_content)
        # response = self.client .chat.completions.create(
        #     model=model,
        #     messages=messages,
        #     temperature=0)
        # response_msg = response.choices[0].message.content
        # print(response_msg)

# chatbot = ChatBot()
# chatbot.make_request("Say this is a test!")


