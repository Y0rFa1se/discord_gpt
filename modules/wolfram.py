import wolframalpha
import asyncio
import matplotlib.pyplot as plt
import os

os.mkdir("files", exist_ok=True)

async def get_wolfram(query, app_id):
    app_id = app_id
    client = wolframalpha.Client(app_id)
    res = await asyncio.to_thread(client.query, query)
    res = next(res.results).text

    plt.text(0.5, 0.5, res, ha='center', va='center')
    plt.axis('off')
    plt.savefig("files/wolfram.png")
    plt.close()

    return res