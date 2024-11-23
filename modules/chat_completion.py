import os
import pandas as pd

from langchain.chat_models import ChatOpenAI
from llama_index import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    ServiceContext
)

def api_init(api_key):
    os.environ["OPENAI_API_KEY"] = api_key