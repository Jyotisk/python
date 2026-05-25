from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = r"C:\Users\HP\Desktop\projects\AI\rag\nodejs.pdf"

# load this file in python program
loader=PyPDFLoader(file_path=pdf_path)
docs=loader.load()

# split docs to smaller chunk
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)

chunks = text_splitter.split_documents(documents=docs)

# vecotr embedding

embedding_model=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_stor=QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333/",
    collection_name="pdf_reader"
)
print("Indexing of document done ...")