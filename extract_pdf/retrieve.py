## Data extraction using RAG
from PyPDF2 import PdfReader
import os
import openai
import chromadb
from chromadb.utils import embedding_functions
chroma_client = chromadb.Client()

# Read pdf, get text
reader = PdfReader('lease.pdf')
page_ids = []
page_texts = []
for i, p in enumerate(reader.pages):
    page_ids.append(str(i))
    page_texts.append(p.extract_text())

# Create embedding search index
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    model_name='text-embedding-ada-002')
collection = chroma_client.create_collection(
    name='my_lease',
    embedding_function=openai_ef)
collection.add(documents=page_texts, ids=page_ids)

# Retrieve relevant page
results = collection.query(
    query_texts=['Lease termination terms'],
    n_results=1)
page = results['documents'][0][0]

# Create prompt
q = f'''
You are a text processing agent working with lease agreement document.

How many days notice is required for termination of this lease agreement.
Return answer as JSON object with following fields:
- "notice_days" <number>

Do not infer any data based on previous training, strictly use only source text given below as input.
========
{page}
========
'''

# OpenAI call, print result
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[{"role": "user", "content": q}])
c = completion.choices[0].message.content
print(c)
