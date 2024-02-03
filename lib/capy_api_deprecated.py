import os
import openai
import time
import pandas as pd
import sys
import requests

REQUEST_TOKEN = "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"

class CopilotApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def option_based_command(self, command, option, command_result):
        endpoint = f"{self.base_url}/capy"
        payload = {
            "request_token": REQUEST_TOKEN,
            "command": command,
            "command_result": command_result,
            "option": option
        }
        response = self._make_post_request(endpoint, payload)
        return response

    def question_based_command(self, command, option_content, change_json):
        endpoint = f"{self.base_url}/capy"
        payload = {
            "request_token": REQUEST_TOKEN,
            "command": command,
            "change_json": change_json,
            "option": "question",
            "option_content": option_content
        }
        response = self._make_post_request(endpoint, payload)
        return response

    def _make_post_request(self, endpoint, payload):
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None


# Script that takes command and option and then execute and returns results back to the users. 
if __name__ == "__main__":
    base_url = "https://api.example.com"  # Replace with the actual API base URL
    client = CopilotApiClient(base_url)
    
    if len(sys.argv) != 4:
        print("Usage: python script.py <command> <command_content> <option_content>")
        sys.exit(1)

    command = sys.argv[1]
    command_result = sys.argv[2]
    option_content = sys.argv[3]
    print(command, command_result, option_content)

    # # Option Based Command - tf plan --Explain
    # explain_response = client.option_based_command("terraform plan", "explain", {"output": "tf plan output"}, {"repo": "content"})
    # print("Explain Response:", explain_response)

    # # Option Based Command - tf plan --Cost
    # cost_response = client.option_based_command("terraform plan", "cost", {"output": "tf plan output"}, {"repo": "content"})
    # print("Cost Response:", cost_response)

    # # Question Based Command
    # question_response = client.question_based_command("terraform plan", "how many cluster will be created", {"output": "tf plan result"}, {"repo": "content"})
    # print("Question Response:", question_response)
    
    
    
    
    
    
    
    