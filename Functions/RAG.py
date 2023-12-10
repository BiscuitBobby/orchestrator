import dotenv
from langchain.document_loaders import PyPDFDirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import google.generativeai as palm
import textwrap
import pandas as pd

# Configure the PaLM API
dotenv.load_dotenv()
google_api_key = os.getenv('PALM_KEY')

palm.configure(api_key=google_api_key)
models = [m for m in palm.list_models() if 'embedText' in m.supported_generation_methods]
model = models[0]

# Load the document and split it into chunks
loader = TextLoader("Functions/data.txt")
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
text_chunks = text_splitter.split_documents(documents)

# Create DataFrame
df = pd.DataFrame(text_chunks)

'''for col_header in df.columns:
    print(f"\nValues under Column Header '{col_header}':")
    for index, value in enumerate(df[col_header], start=1):
        print(f"  Row {index}: {value}")'''

df = df.drop(columns=[1,
                      2])  # dropping headers 1 and 2 -> metadata ('metadata', {'source': 'Functions/data.txt'}) and type ('type', 'Document')
df.columns = ['Text']


def embed_fn(text):
    print(text)
    return palm.generate_embeddings(model=model, text=text)['embedding']

print('creating embeddings...')
df['Embeddings'] = df['Text'].apply(embed_fn)
print('created embeddings')

print(df.columns)
print(df.info())

