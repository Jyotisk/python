from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI
import json
load_dotenv()

client=OpenAI()

OPEN_AI_KEY=os.getenv("OPENAI_API_KEY")

config={
    "version":"v1.1",
    "embedder":{
        "provider":"openai",
        "config":{"api_key":OPEN_AI_KEY,"model":"text-embedding-3-small"}
    },
    "llm":{
        "provider":"openai",
        "config":{"api_key":OPEN_AI_KEY,"model":"gpt-4.1"}
    },
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host":"localhost",
            "port":6333
            }
    }
    
}
mem_client = Memory.from_config(config)
while True:
    user_query=input("> ")

    # Use filters param per mem0 API (top-level entity params are rejected)
    search_memory=mem_client.search(query=user_query, filters={"user_id":"jyotiska"})

    # Extract results robustly whether search_memory is dict-like or an object
    try:
        results = search_memory.get("results", [])
    except Exception:
        results = getattr(search_memory, "results", []) or []

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in results
    ]

    print("Found Memories: ", memories)

    SYSTEM_PROMPT=f"""
    Here is the context about the user:
    {json.dumps(memories)}
    """
    
    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )
    ai_response=response.choices[0].message.content

    print("AI: ",ai_response)

    mem_client.add(
        user_id="jyotiska",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )
    print("Memory added to the vector store")
