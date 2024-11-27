import wolframalpha

def get_wolfram(query, app_id):
    app_id = app_id
    client = wolframalpha.Client(app_id)
    res = client.query(query)

    return next(res.results).text