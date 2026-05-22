
from google import genai
client=genai.Client(
    api_key="AIzaSyCCDsfyW9RFXquyvgqew1_oW2L11bDOJWQ"
) 

response=client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how ai works"
)

print(response.text)