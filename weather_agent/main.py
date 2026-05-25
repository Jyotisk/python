from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

def get_weather(city:str):
    url=f"https://wttr.in/{city}?format=3"
    response=requests.get(url)
    if response.status_code==200:
        return f"The weather in {city} is: {response.text}"
    return "Sorry, I couldn't fetch the weather information at the moment."

def main():
    user_query=input(">")
    response=client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides weather information."},
            {"role": "user", "content": user_query}
        ]
    )
    print(response.choices[0].message.content)

print(get_weather("guwahati"))    