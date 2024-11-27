import openai
import tiktoken

def count_token(messages, model):
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

def gpt_request(history: dict, model) -> str:
    completion = openai.chat.completions.create(
        model=model,
        messages=history,
        stream=True
    )

    return completion