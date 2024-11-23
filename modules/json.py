import os
import json

os.mkdir("chat_history")

def load_json(dir: str, name: str) -> dict:
    try:
        os.mkdir(f"chat_history/{dir}")
    
    except FileExistsError:
        pass

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