import json

def load_json(name: str) -> dict:
    try:
        with open(f"chat_history/{name}.json", "r") as f:
            return json.load(f)
        
    except FileNotFoundError:
        with open(f"chat_history/{name}.json", "w") as f:
            json.dump([], f, indent=4)

        return []
    
def save_json(name: str, data: dict) -> None:
    with open(f"chat_history/{name}.json", "w") as f:
        json.dump(data, f, indent=4)