import os
import openai
import time
import pandas as pd
import sys
from chatbot import ChatBot

class CopilotClient:
    def __init__(self):
        pass

    def make_request_to_bot(self, tf_output, command, question=None):
        chatbot = ChatBot()
        if command == "explain":
            msg_content = "Given the following terraform plan: \n";
            msg_content += tf_output
            msg_content += "\n"
            msg_content += "Explain what it does"
            chatbot.make_request(msg_content)

        elif command == "cost":
            msg_content = "Given the following terraform plan: \n";
            msg_content += tf_output
            msg_content += "\n"
            msg_content += "Estimate how much it woulld cost"
            chatbot.make_request(msg_content)

        elif command == "question":
            msg_content = "Given the following terraform plan: \n";
            msg_content += tf_output
            msg_content += "\n"
            msg_content += question
            chatbot.make_request(msg_content)

        else:
            print(f"Invalid command option: {e}")
            return None

# Script that takes command and option and then execute and returns results back to the users. 
if __name__ == "__main__":
    # base_url = "https://api.example.com"  # Replace with the actual API base URL
    client = CopilotClient()
    print(len(sys.argv))

    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python script.py <command> <command_content> <option_content>")
        sys.exit(1)

    command = sys.argv[1]
    command_result = sys.argv[2]
    option_content = sys.argv[3]
    question = None
    if len(sys.argv) == 5:
        question = sys.argv[4]
    print(command, command_result, option_content)

    # This is a test and here is the test instruction
    # execute python capy_api.py "tf plan" "test" "explain"
    # execute python capy_api.py "tf plan" "test" "cost"
    # execute python capy_api.py "tf plan" "test" "question" "what does this tf plan do?"
    test_tf_output = """
    Terraform will perform the following actions:

      # azurerm_resource_group.tf-plan will be created
      + resource "azurerm_resource_group" "tf-plan" {
          + id       = (known after apply)
          + location = "centralus"
          + name     = "rg-tf-plan-example-centralus"
          + tags     = {
              + "name" = "test"
            }
        }

    Plan: 1 to add, 0 to change, 0 to destroy.
    """
    
    client.make_request_to_bot(test_tf_output, option_content, question)
    
    
    
    
    