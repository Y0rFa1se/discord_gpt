import wolframalpha
import asyncio
import os

import requests
from PIL import Image
from io import BytesIO

os.makedirs("files", exist_ok=True)

async def get_wolfram(query, app_id):
    app_id = app_id
    client = wolframalpha.Client(app_id)
    res = await asyncio.to_thread(client.query, query)

    result_text = None
    for pod in res.pods:
        if pod.title == "Result":
            result_text = pod.subpods[0].plaintext if pod.subpods else "No text result"
            break
    
    image_url = next(res.pods).subpods[0].img['src']
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    img.save("files/wolfram.png")

    return result_text