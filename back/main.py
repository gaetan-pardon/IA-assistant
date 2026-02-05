#from fastapi import FastAPI

# import TinyDB from tinydb
import datetime


#qwen/qwen3-4b:free

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help you today?"},
    {"role": "user", "content": "What's the weather?"},
]


itemexample = {
    "user": "12345",
    "conversation_name": "My Conversation",
    "conversation": messages
}

userexample = {
    "user": "12345",
    "mdp": "hashed_password",
}

#from llama_index.llms.openrouter import OpenRouter #marche pas
#from openai import OpenAI #marche pas
#import requests #marche pas

from utils.AIModelresponse import get_ai_response, get_ai_response_distant


prompt = "Give me a very short introduction to large language model."
messages2 = [         {"role": "user", "content": prompt}     ]

messagestime = [
    {"id": 1, "role": "system", "content": "You are a helpful assistant.", "timestamp": datetime.datetime.now()},
    {"id": 2, "role": "user", "content": "Hello!",  "timestamp": datetime.datetime.now()},
    {"id": 3, "role": "assistant", "content": "Hi! How can I help you today?",  "timestamp": datetime.datetime.now()},
    {"id": 4, "role": "user", "content": "What's the weather in france ?",  "timestamp": datetime.datetime.now()},
]


response = get_ai_response(messagestime)
print("Final response:", response)

print("/n/n/n response distant /n/n/n")

response = get_ai_response_distant(messagestime)
print("Final response:", response)

#app = FastAPI()