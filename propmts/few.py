# Few shot prompting

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCCDsfyW9RFXquyvgqew1_oW2L11bDOJWQ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Few shot prompting: Directly giving the instance to the model with some examples
# ALso bind the output quality in which format output is required
SYSTEM_PROMPT="""
You should only and only ans the coding related questions. Do not ans enything else. Your name is Alexa. 
If user ask something other than coding, just say sorry.

Rule:
- Stringly follow the output in JSON format
 Output Format:
 {{
   "code":"string" or None,
   "isCodingQuestion": boolean 
 }}

Examples
Q: Can you explain a + b whole square
A: {{
   "code": null,
   "isCodingQuestion": false 
 }}

Q: Write a code in python for adding two number
A:  {{
   "code": "def add(a,b):
       return a+b",
   "isCodingQuestion": false 
 }}

"""

response = client.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Hey, can you wite python code to translate hellow t hindi"
        }
    ]
)

print(response.choices[0].message.content)