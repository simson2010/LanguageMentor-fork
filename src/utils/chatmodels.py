from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI

class ChatModel:
    def __init__(self, model_name, model_type, api_key, base_url):
        self.model_name = model_name
        self.model_type = model_type
        self.api_key = api_key
        self.base_url = base_url
        self.model = None

    def get_model(self):
        if self.model_type == "ollama":
            self.model = ChatOllama(model=self.model_name, max_tokens=8192, temperature=0.8)
        elif self.model_type == "openai":
            self.model = ChatOpenAI(model=self.model_name, max_tokens=8192, temperature=0.8, api_key=self.api_key)
        return self.model



if __name__ == "__main__":
    model = ChatModel(model_name="llama3.1:8b-instruct-q8_0", model_type="ollama", api_key="", base_url="")
    print(model.get_model())



