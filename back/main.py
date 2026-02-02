#from fastapi import FastAPI
from key import key # import the key variable from key.py
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




#app = FastAPI()