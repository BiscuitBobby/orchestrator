import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_experimental.utilities import PythonREPL
import os

from langchain_google_genai import ChatGoogleGenerativeAI

dotenv.load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ['GOOGLE_API_KEY']

template = PromptTemplate(
    input_variables=["input"],
    template="""Write some python code to solve the user's problem. 

    Return only python code in Markdown format, e.g.:
    
    ```python
    ....
    ```
    The user problem is the following: {input}
    """
)

model = ChatGoogleGenerativeAI(model="gemini-pro")

def prompt(query: dict):
    prompt = template.invoke(query)
    return prompt
def _sanitize_output(text: str):
    _, after = text.split("```python")
    code = after.split("```")[0]
    print(f"code:{code}")
    return code

def output(x) -> str:
    print(f"output:\n{x}")
    return x

chain = prompt | model | StrOutputParser() | _sanitize_output | PythonREPL().run | output

chain.invoke({"input": input("enter query: ")})
