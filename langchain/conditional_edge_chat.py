from dotenv import load_dotenv
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from typing import Optional,Literal
from langgraph.graph import StateGraph,START,END
from openai import OpenAI
load_dotenv()

client=OpenAI()

class State(TypedDict):
    user_query:str
    llm_output:Optional[str]
    is_good:Optional[bool]
 
def chatbot(state: State):
    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user","content":state.get("user_query")}
        ]
    )
    state["llm_output"]=response.choices[0].message.content
    return state
def evaluate_response(state:State)->Literal["chatbot_gemini","end_node"]:
    if True:
        return "end_node"
    return "chatbot_gemini"

def chatbot_gemini(state: State):
    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user","content":state.get("user_query")}
        ]
    )
    state["llm_output"]=response.choices[0].message.content
    return state    
def end_node(state:State):
   return state

graph_builder=StateGraph(State)    

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("end_node",end_node)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("chatbot_gemini","end_node")
graph_builder.add_edge("end_node",END)

graph=graph_builder.compile()
updated_state=graph.invoke(State({"user_query":"what is 2+2?"}))
print(updated_state)