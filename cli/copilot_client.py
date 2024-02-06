
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
