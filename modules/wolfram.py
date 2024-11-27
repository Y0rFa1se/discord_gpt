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

    if res["@success"] == "false":
        return "No results found."
    
    ret = ""
    for pod in res['pod']:
        ret += f"## {pod['@title']}\n"
        ret += f"{pod['subpod']['plaintext']}\n"
        ret += f"![]({pod['subpod']['img']['@src']})"

    return ret