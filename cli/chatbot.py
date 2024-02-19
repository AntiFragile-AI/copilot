import constants as C
from dotenv import load_dotenv
from openai import OpenAI
import os
import pandas as pd
import redis
from spencer.spencer import Spencer
from spencer import Embedder
import time

def read_f(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"


class ChatBot:
    def __init__(self):
        # self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.redis_client = None
        self.embedder = None
        self.spencer_client = None
        
    
    def make_request(self, msg_content, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": msg_content}]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0)
        response_msg = response.choices[0].message.content
        return response_ms
        
    
    def setup(self, local_path):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.embedder = Embedder(
            self.redis_client,
            self.openai_client,
            "text-embedding-3-small",
            local_path,
            key_prefix=C.REDIS_KEY_PREFIX,
            max_tokens=2000,
        )
        print(f"Embedding success? {self.embedder()}")
    
    
    def make_spencer_request(self, question):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.spencer_client = Spencer(
            self.redis_client,
            self.openai_client,
            read_f(C.SYSTEM_INSTRUCT_PATH),
            C.GPT_MODEL,
            "text-embedding-3-small",
            C.MAX_CONTEXT_LEN,
            C.MAX_TOKENS,
            key_prefix=C.REDIS_KEY_PREFIX,
            knn=50,
        )
        if self.redis_client == None:
            raise Exception("haven't done setup yet")
        
        print(question)
        resp = self.spencer_client.answer(question)
        print(resp)
        
        

# chatbot = ChatBot()
# chatbot.setup()

# question = "Can you explain what this terraform do?\n\n" 
# print(question)
# resp = chatbot.spencer_client.answer(question)
# print(resp)
# markdown2html = markdown2.markdown(resp)
# print(jsonify(markdown2html))


# sample input terraform data.
# https://github.com/futurice/terraform-examples/tree/master/aws/aws_domain_redirect
