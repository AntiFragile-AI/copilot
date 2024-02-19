import os
import openai
import time
import pandas as pd
import sys
from chatbot import ChatBot
from copilot_client import CopilotClient

# Script that takes command and option and then execute and returns results back to the users. 
if __name__ == "__main__":
    client = CopilotClient()
    chatbot = ChatBot()
    
    # Validate system arguments
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print("Usage: python script.py <sys_command> <sys_command_output> <capy_command> <question (optional)>")
        sys.exit(1)
        
        
    # run capy setup command.  
    if len(sys.argv) == 3:
        if sys.argv[1] == "setup":
            # test local path: C.KNOWLEDGE_DIR
            repo_link = sys.argv[2]
            chatbot.setup(repo_link)
        else:
            print("Usage: python script.py <sys_command> <sys_command_output> <capy_command> <question (optional)>")
            sys.exit(1) 
    
        
    # run capy question command.
    elif len(sys.argv) == 2:
        question = sys.argv[1]
        # TODO[tina]: remove the first setup step.
        # chatbot.setup()
        print("DEBUG: start question")
        chatbot.make_spencer_request(question)  
        print("DEBUG: end question") 
        

    # run command with cli interface.
    elif len(sys.argv) == 4 or len(sys.argv == 5):
        sys_command = sys.argv[1]
        sys_command_output = sys.argv[2]
        capy_command = sys.argv[3]
        question = sys.argv[4] if len(sys.argv) == 5 else None

        # This is a test and here is the test instruction
        # python capy_api.py "tf plan" "test" "explain"
        # python capy_api.py "tf plan" "test" "cost"
        # python capy_api.py "tf plan" "test" "question" "what does this tf plan do?"
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
    
    
    
    
    