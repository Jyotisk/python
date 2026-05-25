# Zero Shot Propmting

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCCDsfyW9RFXquyvgqew1_oW2L11bDOJWQ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Zero Shot Propmting: Directly giving the instance to the model

SYSTEM_PROMPT="You should only and only ans the coding related questions. Do not ans enything else. Your name is Alexa. If user ask something other than coding, just say sorry"

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