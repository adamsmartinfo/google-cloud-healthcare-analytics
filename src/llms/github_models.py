from langchain_openai import ChatOpenAI

from config.settings import (
    GITHUB_TOKEN,
)

llm = ChatOpenAI(
    model="openai/gpt-4.1-mini",
    api_key=GITHUB_TOKEN,
    base_url="https://models.github.ai/inference",
    temperature=0,
)