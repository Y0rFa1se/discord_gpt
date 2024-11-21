import openai
import tiktoken

def openai_init(api_key):
    openai.api_key = api_key

def count_token(messages, model="gpt-4o-mini"):
    tokenizer = tiktoken.encoding_for_model(model)
    tokens = 0

    for message in messages:
        try:
            tokens += len(tokenizer.encode(message['content']))
            tokens += 4
        
        except:
            tokens += len(tokenizer.encode(message['content'][0]['image_url']['url']))

    tokens += 2

    return tokens

def cut_message(message_json):
    return message_json[-20:]

def render_requests(history: dict, requests: str) -> dict:
    history.append({
        "role": "user",
        "content": requests
    })

    return history

def render_image(history: dict, image_url: str) -> dict:
    history.append({
        "role": "user",
        "content": [{
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        }]
    })

    return history

def render_responses(history: dict, responses: str) -> dict:
    history.append({
        "role": "assistant",
        "content": responses
    })

    return history

def openai_request(history: dict, model="gpt-4o-mini") -> str:
    completion = openai.chat.completions.create(
        model=model,
        messages=history
    )

    return completion.choices[0].message.content