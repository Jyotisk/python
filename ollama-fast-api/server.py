from fastapi import FastAPI
from pydantic import BaseModel
from ollama import chat

app = FastAPI()

# Request body schema
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def ai_chat(request: ChatRequest):

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return {
        "response": response["message"]["content"]
    }