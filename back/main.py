#from fastapi import FastAPI

# import TinyDB from tinydb


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
messages = [         {"role": "user", "content": prompt}     ]


response = get_ai_response(messages)
print("Final response:", response)

response = get_ai_response_distant(messages)
print("Final response:", response)

#app = FastAPI()