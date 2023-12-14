# https://health.petals.dev/
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM
from langchain.llms.base import LLM
from typing import List, Optional, Any
from dependencies import *
from Functions.discord_message import discord_messaging


class CustomLLM(LLM):
    def __init__(
        self,
        model_name: str,
        temperature: float = 0.7,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        n: int = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False, add_bos_token=False)
        model = AutoDistributedModelForCausalLM.from_pretrained(model_name).cuda()  # Move the model to GPU if available
        temperature = temperature
        top_p = top_p
        top_k = top_k
        max_output_tokens = max_output_tokens or 1500
        n = n

        object.__setattr__(self, "tokenizer", tokenizer)
        object.__setattr__(self, "model", model)
        object.__setattr__(self, "max_output_tokens", max_output_tokens)
        object.__setattr__(self, "temperature", temperature)
        object.__setattr__(self, "top_p", top_p)
        object.__setattr__(self, "top_k", top_k)
        object.__setattr__(self, "top_p", top_p)
        object.__setattr__(self, "n", n)

    def _call(self, text: str, stop=None, **kwargs) -> str:
        # Prepare the input for the model
        inputs = self.tokenizer(text, return_tensors="pt")["input_ids"].cuda()

        # Generate the output using the model
        outputs = self.model.generate(
            inputs,
            max_length=self.max_output_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            num_return_sequences=self.n,
            do_sample=True,  # Enable sampling
            **kwargs
        )

        # Decode the generated tokens to text
        decoded_outputs = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

        return decoded_outputs[0] if decoded_outputs else ""

    @property
    def _llm_type(self) -> str:
        return "CustomLLM"


# Initialize the custom LLM
llm = CustomLLM(model_name="petals-team/StableBeluga2")

prompt = hub.pull("hwchase17/react-chat")

tools = [discord_messaging]

# Partially apply the prompt with the tools description and tool names
prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)


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

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True)

query = "what is a lemon"

try:
    output = agent_executor.invoke({f"input": {query}})["output"]
    print(output)
except ValueError as e:
    print(f"An error occurred while parsing the LLM output: {e}")

