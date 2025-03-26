import os
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
from incidentQueryService import IncidentQueryService

# **Child Agent 1: Script Execution Agent**
script_executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=os.getcwd(),  # Use the current working directory to store the code files.
)

script_execution_agent = ConversableAgent(
    "script_execution_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": script_executor},  # Use the local command line code executor.
    human_input_mode="NEVER",  # Never take human input for this agent for safety.
)

# **Child Agent 2: RAG Query Agent**
class QueryAPI:
    def __init__(self):
        self.query_Service = IncidentQueryService("chatBot")

    def handle_query(self, query):
        return self.query_Service.rag_chain.invoke(query)

queryAPI = QueryAPI()

class RagQueryAgent(ConversableAgent):
    def __init__(self, name):
        super().__init__(name, llm_config=False, code_execution_config={"use_docker": False}, human_input_mode="NEVER")

    def handle_query(self, query):
        return queryAPI.handle_query(query)

rag_query_agent = RagQueryAgent("rag_query_agent")

# **Master Agent: Decides which Child Agent to Call**
class MasterAgent(ConversableAgent):
    def __init__(self, name):
        super().__init__(name, llm_config=False, code_execution_config={"use_docker": False}, human_input_mode="NEVER")

    def route_query(self, user_query):
        if user_query.lower().startswith("run script"):
            script_name = user_query[len("run script"):].strip()
            if not script_name.endswith(".py"):
                script_name += ".py"
                script_path = os.path.join(os.getcwd(), script_name)
                if not os.path.isfile(script_path):
                    return f"Script {script_name} not found."
            script = open(script_path, "r").read()  # command to run
            message_with_code_block = f"""This is a message with code block.
            The code block is below:
            ```python
            {script}
            ```
            This is the end of the message.
            """
            print(message_with_code_block)
            # Generate a reply for the given code.
            reply = script_execution_agent.generate_reply(messages=[{"role": "user", "content": message_with_code_block}])
            return reply
            script = open("HealthCheck.py", "r").read()# command to run
            #message_with_code_block= "Execute a python script HealthCheck.py"
            message_with_code_block = f"""This is a message with code block.
            The code block is below:
            ```python
            {script}
            ```
            This is the end of the message.
            """

            print(message_with_code_block)
            # Generate a reply for the given code.
            reply = script_execution_agent.generate_reply(messages=[{"role": "user", "content": message_with_code_block}])
            return reply
        elif "fix this issue" in user_query.lower():
            query = user_query
            print("query", query)
            response = rag_query_agent.handle_query(query)
            print("response", response)
            return response
        else:
            query = user_query
            print("query", query)
            response = rag_query_agent.handle_query(query)
            print("response", response)
            return response

master_agent = MasterAgent("master_agent")

# **Define Tasks and Routing Logic**
def get_agent_response(user_query):
    try:
        response = master_agent.route_query(user_query)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    user_query = "run script"
    response = get_agent_response(user_query)
    print(response)

    user_query = "fix this issue"
    response = get_agent_response(user_query)
    print(response)