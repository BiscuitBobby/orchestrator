import dotenv
import os
import wolframalpha
import google.generativeai as palm

dotenv.load_dotenv()
palm_key = os.getenv("PALM_KEY")
#palm_key = os.environ('PALM_KEY')
palm.configure(api_key=palm_key)
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

appid = 'XW8475-92QUW2TKUU'
# App id obtained by the above steps
app_id = appid
client = wolframalpha.Client(app_id)


def search_wolfram(query):
    try:
        res = client.query(query)
        answer = next(res.results).text
        print(f"{answer}\n\n")
    except:
        answer = None
    return answer


def palm_prompt(query, context=None):
    if context:
        prompt = f"""
                Here is my query: {query},
                answer while keeping in account the following information:{context.replace(':', '')}
                """

    else:
        prompt = f"""
                {query}
                """

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=800,
    )

    #print(completion.result)
    return completion.result


def wolfram_search():
    query = input("input: ")
    context = search_wolfram(query)
    response = palm_prompt(query, context)
    return response
