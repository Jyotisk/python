# Chain of thought promting

from openai import OpenAI
import json
import time

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
   
   Rules:
   - Strictly Folloe the given JSON output format
   -  Only run one step at a time.
   - The sequence of the steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT 
   (which is going to display to the user).
   
   Output JSON Format:
   {"step": "START" | "PLAN" | "OUTPUT", "content": "string}
   
   Exapmple:
   START: Hey, Can you solve 2+3 * 5 /10
   PLAN:  {"step": "PLAN" "content": "Seems like use is interested in math problem"}
   PLAN:  {"step" : "PLAN" : "content" :"looking at the proble, we wull solve using BODMAS method"}
   PLAN:  {"step" : "PLAN" : "content" :"first we will multiply 3*5 which is 15"}
   PLAN:  {"step" : "PLAN" : "content" :"Now the new equation is 2+15/10"}
   PLAN:  {"step" : "PLAN" : "content" :"we must perform devide that is 15/10=1.5"}
   PLAN:  {"step" : "PLAN" : "content" :"Now the equation is 2+1.5"}
   PLAN:  {"step" : "PLAN" : "content" :"Now finally perform the add which is 3.5"}
   PLAN:  {"step" : "OUTPUT" : "content" :"3.5"}

"""

print("\n\n\n")

message_history=[
    {"role": "system", "content": SYSTEM_PROMPT},
]

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
           
# response = client.chat.completions.create(
#     model="gemini-3.5-flash",
#     response_format={"type":"json_object"},
#     messages=[
#         {
#             "role": "system",
#             "content": SYSTEM_PROMPT
#         },
#         {
#             "role": "user",
#             "content": "Hey, write a code to add n number in js"
#         }
#     ]
# )

# print(response.choices[0].message.content) n number in js"
#         }
#     ]
# )

# print(response.choices[0].message.content) n number in js"
#         }
#     ]
# )

# print(response.choices[0].message.content)