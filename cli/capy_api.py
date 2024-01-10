import os
import openai
import time
import pandas as pd
import sys
from chatbot import ChatBot

class CopilotClient:
    def __init__(self):
        pass

    def make_request_to_bot(self, sys_command, sys_command_output, capy_command, question=None):
        msg_content = "Given the following " + sys_command + ": \n";
        msg_content += sys_command_output
        msg_content += "\n"

        chatbot = ChatBot()
        if capy_command == "explain":
            msg_content += "Explain what it does"
        elif capy_command == "cost":
            msg_content += "Estimate how much it woulld cost"
        elif capy_command == "question":
            msg_content += question
        else:
            print(f"Invalid command option: {e}")
            return None
        
        print(msg_content)
        response = chatbot.make_request(msg_content)
        print(response)
        return response

# Script that takes command and option and then execute and returns results back to the users. 
if __name__ == "__main__":
    client = CopilotClient()
    print(len(sys.argv))

    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python script.py <sys_command> <sys_command_output> <capy_command> <question (optional)>")
        sys.exit(1)

    sys_command = sys.argv[1]
    sys_command_output = sys.argv[2]
    capy_command = sys.argv[3]
    question = sys.argv[4] if len(sys.argv) == 5 else None
    print(sys_command, sys_command_output, capy_command)

    # This is a test and here is the test instruction
    # execute python capy_api.py "tf plan" "test" "explain"
    # execute python capy_api.py "tf plan" "test" "cost"
    # execute python capy_api.py "tf plan" "test" "question" "what does this tf plan do?"
    sys_output = ""
    if sys_command_output == "test":
        sys_output = """
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
    else:
        sys_output = sys_command_output
    
    
    client.make_request_to_bot(sys_command, sys_output, capy_command, question)
    
    
    
    
    