from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm=init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)

class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:State):
    # print(f"\n\n\nChatbot node state",state)
    response=llm.invoke(state.get("messages"))
    return {"messages":[response]}
        
        
graph_builder = StateGraph(State)   
graph_builder.add_node("chatbot",chatbot)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
   
MONGODB_URI = "mongodb://localhost:27017"
with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
    # graph=graph_builder.compile(checkpointer=checkpointer)
    # return graph

    graph_with_checkpointer=compile_graph_with_checkpointer(checkpointer=checkpointer)
    
    config = {
            "configurable": {
                "thread_id": "jyotiska"
            }
        }

    for chunk in graph_with_checkpointer.stream(State({"messages":"what is my name"}),config,stream_mode="values"):
         chunk["messages"][-1].pretty_print()
         
#(START)->chatbot->(END)
# state ={messages:["hey there"]}
#node runs:chatbot(state:["hey There"]) ->["Hi this is a message from chatbot Node"]
# state ={messages: ["hey there",Hi this is a message from chatbot Node]}
