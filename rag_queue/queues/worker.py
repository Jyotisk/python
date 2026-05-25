from functools import lru_cache

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()


@lru_cache
def get_openai_client() -> OpenAI:
    return OpenAI()


@lru_cache
def get_vector_db() -> QdrantVectorStore:
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
    return QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333/",
        collection_name="pdf_reader",
        embedding=embedding_model,
    )


def process_query(query: str) -> str:
    query = query.strip()
    if not query:
        raise ValueError("Query must not be empty.")

    print("Searching chunks...", query)
    search_results = get_vector_db().similarity_search(query=query)
    context = "\n\n\n".join(
        (
            f"Page Content: {result.page_content}\n"
            f"Page Number: {result.metadata.get('page_label', 'Unknown')}\n"
            f"File Location: {result.metadata.get('source', 'Unknown')}"
        )
        for result in search_results
    )

    system_prompt = f"""
    You are a helpful AI Assistant who answers user query based on the available context retrieved from a PDF file along with
    page content and page number.

    You should only answer the user based on the following context and navigate the user to open the right page number to
    know more.

    Context: {context}
    """
    response = get_openai_client().chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
    )
    answer = response.choices[0].message.content or ""
    print("AI Assistant:", answer)
    return answer
