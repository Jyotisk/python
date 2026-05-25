from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCCDsfyW9RFXquyvgqew1_oW2L11bDOJWQ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[
        {
            "role": "system",
            "content": "you are expert in mathematics and only and only answer related to mathematics. That if the query is notrelated to maths just say sorry "
        },
        {
            "role": "user",
            "content": "what is 2+2"
        }
    ]
)

print(response.choices[0].message)