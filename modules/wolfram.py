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
    res = next(res.results).text

    image_url = next(res.pods).subpods[0].img['src']
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    img.save("files/wolfram.png")

    return res