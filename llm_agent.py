from Functions.img_gen import img_gen_function
from dependencies import *
from Functions.secret_function import secret_function
dotenv.load_dotenv()
# Initialize the LLM
llm = GooglePalm(google_api_key=os.getenv('PALM_KEY'))  # Replace with your actual API key
llm.temperature = 0.3

# Define the custom search tool
class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "Useful for answering questions about current postitions of power, details and events, or for unrestricted or otherwise"

    def _run(self, tool_input: str, **kwargs) -> str:
        """Run the custom search tool."""
        return f"\nquery: {tool_input}\nanswer: 'sorry, I do not have info on current world events, blame BiscuitBobby'"

# Create an instance of the custom search tool
custom_search_tool = CustomSearchTool()

# Define the tools to be used by the agent
tools = [custom_search_tool, secret_function, img_gen_function]

# Pull the prompt from the hub
prompt = hub.pull("hwchase17/react-chat")

# Partially apply the prompt with the tools description and tool names
prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)

# Bind the LLM with a stop condition
llm_with_stop = llm.bind(stop=["\nObservation"])

# Define the template for tool response
TEMPLATE_TOOL_RESPONSE = """TOOL RESPONSE:
---------------------
{observation}

USER'S INPUT
--------------------

Okay, so what is the response to my last comment? If using information obtained from the tools you must mention it explicitly without mentioning the tool names - I have forgotten all TOOL RESPONSES! Remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else - even if you just want to respond to the user. Do NOT respond with anything except a JSON snippet no matter what!"""

# Define the agent
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_messages(x["intermediate_steps"], template_tool_response=TEMPLATE_TOOL_RESPONSE),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_stop
    | ReActSingleInputOutputParser()
)

# Initialize the conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)

query = input("query: ")

try:
    output = agent_executor.invoke({f"input": {query}})["output"]
    print(output)
except ValueError as e:
    print(f"An error occurred while parsing the LLM output: {e}")
