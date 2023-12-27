import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool
from langchain_experimental.utilities import PythonREPL
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from Functions.test_embeddings.simple_vector_search import vector_search

dotenv.load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ['GOOGLE_API_KEY']

model = ChatGoogleGenerativeAI(model="gemini-pro")

template = PromptTemplate(
    input_variables=["input"],
    template="""Write some python code to solve the user's problem. 
    Do not use if __name__ == "__main__", run it directly.
    Return only python code in Markdown format, e.g.:
    
    ```python
    ....
    ```
    The user problem is the following: {input}
    """
)


def prompt(query: dict):
    context = vector_search(query['input'])
    if len(context) > 0:
        query['input'] += f"\nyou may use the following information {str(context)}"
        prompt = template.invoke(query)
    else:
        prompt = template.invoke(query)
    return prompt


def _sanitize_output(text: str):
    _, after = text.split("```python")
    code = after.split("```")[0]
    print(f"code:{code}")
    return code


def output(x) -> str:
    if len(x) > 0:
        out = f"completed task with output:\n{x}"
        print(out)
        return str(out)
    else:
        out = "completed task successfully"
        print(out)
        return str(out)


def code_execution(code):
    x = PythonREPL().run(code)
    if len(x) > 0:
        out = f"executed the following code:{code}\n with output:\n{x}"
        print(out)
        return (out)
    else:
        out = f"executed the following code:{code}\ncompleted task successfully"
        print(out)
        return out

class ArbitraryCode(BaseTool):
    name = "arbitrary_code"
    description = ("Useful to accomplish a specific task that cannot be done by a language model, such as code "
                   "execution, opening programs, drawing, etc.")

    master_prompt = 'Lemon'

    def _run(self, tool_input: str, **kwargs) -> str:
        chain = prompt | model | StrOutputParser() | _sanitize_output | code_execution | output

        #return chain.invoke({"input": tool_input})
        out = chain.invoke({"input": self.master_prompt})
        print("\n\n\n\n\n\n")
        print(out)
        print("\n\n\n\n\n\n")
        return str(out)


arbitrary_code = ArbitraryCode()
