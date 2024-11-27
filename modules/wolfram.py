import wolframalpha

async def get_wolfram(query, app_id):
    app_id = app_id
    client = wolframalpha.Client(app_id)
    res = await client.query(query)

    return next(res.results).text