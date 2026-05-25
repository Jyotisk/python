# Chain of thought promting

from openai import OpenAI
import json
import time
import requests
from pydantic import BaseModel, Field
from typing import Optional
import os

def run_commnand(cmd:str):
    result=os.system(cmd)
    return result

def get_weather(city:str):
    url=f"https://wttr.in/{city}?format=3"
    response=requests.get(url)
    if response.status_code==200:
        return f"The weather in {city} is: {response.text}"
    return "Sorry, I couldn't fetch the weather information at the moment."

available_tools={
    "get_weather":get_weather,
    "run_commnand":run_commnand
}

client = OpenAI(
    api_key="AIzaSyBnSORFsPt_888C8kgCl8QPLvBmXjQBrZg",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
# Few shot prompting: Directly giving the instance to the model with some examples
# ALso bind the output quality in which format output is required
# can you solve 2 + 3 / 10 * 6 * 4 /1 -50
SYSTEM_PROMPT="""
   You're an expert AI Assistant in resolving user queries using  chain of thought.
   You work on START,PLAN and OUTPUT steps. 
   You need to first PLAN wjat meeds to be done. The PLAN can be multiple steps.
   Once you think enough PLAN has been done, finally you can give an OUTPUT.
   You can also call a tool if required from the list of avaialble tools.
   for every tool call wait for the observ step which is the output from the called tool.
   
   Rules:
   - Strictly Follow the given JSON output format
   -  Only run one step at a time.
   - The sequence of the steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT 
   (which is going to display to the user).
   
   Output JSON Format:
   {"step": "START" | "PLAN" | "OUTPUT", "content": "string "tool": "string", "input": "string}
   
   Available Tools:
   -get_weather(city: str) : Takes city name as an input and returns the current weather information of the city.
   -run_commnand(cmd: str) : Takes a linux command as string and execute the command on users system and returns output from that command.

   Example 1:
   START: Hey, Can you solve 2+3 * 5 /10
   PLAN:  {"step": "PLAN" "content": "Seems like use is interested in math problem"}
   PLAN:  {"step" : "PLAN" : "content" :"looking at the proble, we wull solve using BODMAS method"}
   PLAN:  {"step" : "PLAN" : "content" :"first we will multiply 3*5 which is 15"}
   PLAN:  {"step" : "PLAN" : "content" :"Now the new equation is 2+15/10"}
   PLAN:  {"step" : "PLAN" : "content" :"we must perform devide that is 15/10=1.5"}
   PLAN:  {"step" : "PLAN" : "content" :"Now the equation is 2+1.5"}
   PLAN:  {"step" : "PLAN" : "content" :"Now finally perform the add which is 3.5"}
   PLAN:  {"step" : "OUTPUT" : "content" :"3.5"}

   Example 2:
   START: Hey, Can you solve 2+3 * 5 /10
   PLAN:  {"step": "PLAN" "content": "Seems like use is interested in weather of guwahati in India"}
   PLAN:  {"step" : "PLAN" : "content" :"Lets see if we have a tool to get weather information"}
   PLAN:  {"step" : "PLAN" : "content" :"Great, we have a tool called get_weather which can fetch weather information for us"}
   PLAN:  {"step" : "TOOL" : "tool" :"get_weather", "input" : "guwahati"}}
   PLAN:  {"step" : "OBSERVE" : "tool" :"get_weather", "output" : "The weather in Guwahati is: Sunny, 25°C"}
   PLAN:  {"step" : "PLAN" : "content" :"Great, I got the weather info of Guwahati"}
   PLAN:  {"step" : "OUTPUT" : "content" :"The current weather in Guwahati is Sunny with a temperature of 25°C"}

"""

print("\n\n\n")

class MyOutputFornmat(BaseModel):
    step: str= Field(..., description="The ID of the steps. example: PLAN, OUTPUT, TOOL"),
    content:Optional[str]=Field(None, description="The optional content field which will be there in case of PLAN and OUTPUT steps"),
    tool: Optional[str]=Field(None, description="The tool field is required only when the step is TOOL. It contains the name of the tool to be called"),
    input: Optional[str]=Field(None, description="The input field is required only when the step is TOOL. It contains the input to be given to the tool")

message_history=[
    {"role": "system", "content": SYSTEM_PROMPT},
]

while True:
    user_query=input("✅")
    message_history.append({"role": "user", "content": user_query})
    while True:
        try:
            response=client.chat.completions.create(
                model="gemini-3.5-flash",
                response_format={"type":"json_object"},
                messages=message_history
            )
            raw_result=(response.choices[0].message.content)
            message_history.append({"role": "assistant", "content": raw_result})
            parsed_result=json.loads(raw_result)

            if parsed_result.get("step")=="START":
                print("User Query: ", parsed_result.get("content"))
                continue

            if parsed_result.get('step')=="TOOL":
                tool_to_call=parsed_result.get("tool")
                tool_input=parsed_result.get("input")
                print(f"Calling tool: {tool_to_call} with input: {tool_input}")

                tool_response=available_tools[tool_to_call](tool_input)
                message_history.append({"role" : "developer", "content":json.dumps({"step":"OBSERVE", "tool":tool_to_call, "output":tool_response}) })
                continue

            if parsed_result.get("step")=="PLAN":
                print("Assistant Plan: ", parsed_result.get("content"))
                continue 
            if parsed_result.get("step")=="OUTPUT":
                print("Assistant Output: ", parsed_result.get("content")) 
                break 
        except Exception as e:
            print("Rate limit hit. Waiting 20 seconds...")
            time.sleep(20)
    
print("\n\n\n")
           