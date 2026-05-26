from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langchain.chat_models import init_chat_model

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
        
def samplenode(state:State):
    print(f"\n\n\nsamplenode node state",state)
    return {"messages":["Hi this is a message from sample Node"]}
        
graph_builder = StateGraph(State)   
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

graph=graph_builder.compile()

updated_state=graph.invoke(State({"messages":"Hello"}))
print(f"\n\n\nupdated_state",updated_state)

#(START)->chatbot->samplenode->(END)
# state ={messages:["hey there"]}
#node runs:chatbot(state:["hey There"]) ->["Hi this is a message from chatbot Node"]
# state ={messages: ["hey there",Hi this is a message from chatbot Node]}
