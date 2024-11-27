import os
import json

def load_json(dir: str, name: str) -> dict:
    os.makedirs(f"chat_history/{dir}", exist_ok=True)

    try:
        with open(f"chat_history/{dir}/{name}.json", "r") as f:
            return json.load(f)
        
    except FileNotFoundError:
        with open(f"chat_history/{dir}/{name}.json", "w") as f:
            json.dump([], f, indent=4)

        return []
    
def save_json(dir: str, name: str, data: dict) -> None:
    with open(f"chat_history/{dir}/{name}.json", "w") as f:
        json.dump(data, f, indent=4)