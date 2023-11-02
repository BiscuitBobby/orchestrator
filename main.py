from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM
from langchain.llms.base import LLM


class CustomLLM(LLM):
    def __init__(self, model_name: str, max_tokens: int = 15, **kwargs):
        super().__init__(**kwargs)
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False, add_bos_token=False)
        model = AutoDistributedModelForCausalLM.from_pretrained(model_name)
        model = model.cuda()  # Move the model to GPU if available
        object.__setattr__(self, "tokenizer", tokenizer)
        object.__setattr__(self, "model", model)
        object.__setattr__(self, "max_tokens", max_tokens)

    def _call(self, text: str, stop=None, **kwargs) -> str:
        inputs = self.tokenizer(text, return_tensors="pt")["input_ids"].cuda()
        outputs = self.model.generate(inputs, max_new_tokens=self.max_tokens)
        decoded_output = (self.tokenizer.decode(outputs[0]))
        return decoded_output

    @property
    def _llm_type(self) -> str:
        return "CustomLLM"


# Initialize the custom LLM
llm = CustomLLM(model_name="petals-team/StableBeluga2")

prompt = PromptTemplate(input_variables=["question"])
# Create the LLMChain
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Generate a response
question = input("query:")
print(...)
response = llm_chain.run(question)
print(response)
