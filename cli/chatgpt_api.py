from openai import OpenAI

client = OpenAI(api_key='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')
import os
import pandas as pd
import time

def get_completion(msg_content, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": msg_content}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0)
    msg = response.choices[0].message.content
    print(msg)
    
get_completion("Say this is a test!")