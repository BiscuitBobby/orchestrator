from langchain.llms import CTransformers
from langchain.llms.ollama import Ollama
from petals import AutoDistributedModelForCausalLM

from Functions.test_embeddings.simple_vector_search import vector_search

# pip install ctransformers
llm = CTransformers(model='../models/dolphin-2.1-mistral-7b.Q6_K.GGUF', model_type='dolphin-2.1-mistral-7b')
#llm = AutoDistributedModelForCausalLM.from_pretrained("petals-team/StableBeluga2").cuda()
#llm = Ollama(model='phi')
query = 'what is the purpose of life'
context = vector_search(query)
print(llm(f"{context}\n query: {query}"))
print('---')

