from transformers import AutoModelForCausalLM, AutoTokenizer
from openai import OpenAI
from datetime import datetime
from model.message import Message


#from key import key # import the key variable from key.py
from dotenv import dotenv_values

config = dotenv_values(".env")

TOKEN_OPENROUTER = str(config["TOKEN_OPENROUTER"])


def get_max_id(messages):
    max_id = 0
    for message in messages:
        if message["id"] > max_id:
            max_id = message["id"]
    return max_id

def get_ai_response_distant(messages):
        
    max_id = get_max_id(messages)
    sendingmessages = []
    for message in messages:
        sendingmessages.append({
            "role": message["role"],
            "content": message["content"]
        })

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=TOKEN_OPENROUTER , #key 
    )

    completion = client.chat.completions.create(
        extra_headers = {
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
        },
        model="z-ai/glm-4.5-air:free",
        messages=sendingmessages
    )

    return Message(
        id = max_id + 1,
        role = "assistant",
        content = completion.choices[0].message.content,
        timestamp = datetime.now().isoformat()
    )