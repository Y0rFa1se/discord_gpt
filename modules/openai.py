import openai

def openai_init(api_key):
    openai.api_key = api_key

def openai_usage():
    start_date = "2024-11-01T00:00:00Z"
    end_date = "2024-11-21T23:59:59Z"

    response = openai.Usage.retrieve(
        start_date=start_date,
        end_date=end_date
    )

    print("사용량 데이터:")
    for daily_usage in response["daily_costs"]:
        print(daily_usage)
