import json
from agno.agent import Agent
from agno.tools.sql import SQLTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os

load_dotenv()


with open("knowledge.JSON", "r", encoding="utf-8") as f:
    db_context = f.read()

with open("prompt.md", "r", encoding="utf-8") as f:
    instructions_prompt = f.read()


def get_agent():
    return Agent(
        tools=[SQLTools(db_url=os.getenv("DB_URL"))],
        model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
        instructions=[
            instructions_prompt,
            "\n### DICIONÁRIO DE DADOS (CONTEXTO DO BANCO):",
            db_context
        ],
        markdown=True,
        add_history_to_messages=True, 
        num_history_responses=5 
    )

agent = get_agent()

# Executando a pergunta localmente apenas se executado diretamente
if __name__ == "__main__":
    agent.print_response("")
