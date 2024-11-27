import wolframalpha
import asyncio
import os
import json

import requests
from PIL import Image
from io import BytesIO

os.makedirs("files", exist_ok=True)

async def get_wolfram(query, app_id):
    client = wolframalpha.Client(app_id)
    res = await asyncio.to_thread(client.query, query)

    with open("files/result.json", "w") as f:
        json.dump(res, f, indent=4)

    # return result_text