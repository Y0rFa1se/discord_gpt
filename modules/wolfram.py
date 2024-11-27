import wolframalpha
import asyncio
import matplotlib.pyplot as plt
import os

import requests
from PIL import Image
from io import BytesIO

os.makedirs("files", exist_ok=True)

async def get_wolfram(query, app_id):
    app_id = app_id
    client = wolframalpha.Client(app_id)
    res = await asyncio.to_thread(client.query, query)

    pod = next(res.pods, None)
    if pod is None:
        return "No results found"
    
    result_text = pod.subpods[0].plaintext if pod.subpods else "No text result"
    
    image_pod = next((p for p in res.pods if p.title == "Plot" or p.title == "Image"), None)
    if image_pod and image_pod.subpods:
        image_url = image_pod.subpods[0].img['src']
        
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                img_data = await response.read()
                img = Image.open(BytesIO(img_data))
                img.save("files/wolfram.png")

    return result_text