from transformers import AutoModelForCausalLM, AutoTokenizer
from openai import OpenAI
#from key import key # import the key variable from key.py
from dotenv import dotenv_values

config = dotenv_values(".env")

TOKEN_OPENROUTER = str(config["TOKEN_OPENROUTER"])


model_name = "Qwen/Qwen3-0.6B"

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)


    #prompt = "Give me a short introduction to large language model."
    #messages = [         {"role": "user", "content": prompt}     ]

def get_ai_response(messages):
    # prepare the model input
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=327 #6  #8
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    # parsing thinking content
    try:
        # rindex finding 151668 (</think>)
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    #print("thinking content:", thinking_content)
    #print("content:", content)
    if thinking_content != "":
        newmessages = messages + [{"role": "thinking_assistant", "content": thinking_content}, {"role": "assistant", "content": content}]
    else:
        newmessages = messages + [{"role": "assistant", "content": content}]
    return newmessages


def get_ai_response_distant(messages):
        
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=TOKEN_OPENROUTER , #key 
    )
    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    model="z-ai/glm-4.5-air:free",
    messages=messages
    )
    newmessages = messages + [{"role": "assistant", "content": completion.choices[0].message.content}]
    return newmessages
    """[
        {
        "role": "user",
        "content": "5+13?"
        }
    ]"""