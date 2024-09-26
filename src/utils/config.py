import json

class Model:
    
    def __init__(self, name, type, api_key, base_url):
        self.name = name
        self.type = type
        self.api_key = api_key
        self.base_url = base_url

all_models = []

def load_environment_variables():
    global all_models
    # error handling    
    try:
        with open('config.json') as f:
            config = json.load(f)
    
        if "models" in config:
            models = config["models"]
            for model in models:
                all_models.append(Model(model["name"], model["type"], model["api_key"], model["base_url"]))
    except Exception as e:
        print(f"Error loading environment variables: {e}")

load_environment_variables()
# expose all_models for import 
__all__ = ["all_models"]

if __name__ == "__main__":
    load_environment_variables()
    print(all_models)
    for model in all_models:
        print(f"名称: {model.name}")
        print(f"类型: {model.type}")
        print(f"API密钥: {model.api_key}")
        print(f"基础URL: {model.base_url}")
        print("---")

