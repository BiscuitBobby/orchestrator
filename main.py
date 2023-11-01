from langchain.llms.base import LLM
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class CustomLLM(LLM):
    def __init__(self, model_name: str, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, "tokenizer", AutoTokenizer.from_pretrained(model_name, use_fast=False, add_bos_token=False))
        object.__setattr__(self, "model", AutoDistributedModelForCausalLM.from_pretrained(model_name))
        #self.model.cuda()  # Ensure the model is on GPU

    def _call(self, text: str, stop=None, **kwargs) -> str:
        inputs = tokenizer(text, return_tensors="pt")["input_ids"].cuda()
        outputs = self.model.generate(inputs, max_new_tokens=150)
        decoded_output = (tokenizer.decode(outputs[0]))
        return decoded_output

    @property
    def _llm_type(self) -> str:
        return "CustomLLM"


# Initialize the custom LLM
llm = CustomLLM(model_name="petals-team/StableBeluga2")

# Define the prompt template
template = """
Question: {question}
Answer: Let's think step by step.
"""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Create the LLMChain
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Generate a response
question = "What is the capital of France?"
response = llm_chain.run(question)
print(response)
