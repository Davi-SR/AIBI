import os
from agno.agent import Agent
from agno.tools.sql import SQLTools
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_URL")
api_key = os.getenv("OPENAI_API_KEY")
agent_db = SqliteDb(db_file="aibi_storage.db")


with open("knowledge.JSON", "r", encoding="utf-8") as f:
    db_context = f.read()

with open("prompt.md", "r", encoding="utf-8") as f:
    instructions_prompt = f.read()


experience_path = "experience.md"
learned_context = ""
if os.path.exists(experience_path):
    with open(experience_path, "r", encoding="utf-8") as f:
        learned_context = f.read()

def get_agent(session_id: str = "Conversa"):
    return Agent(
        tools=[SQLTools(db_url=db_url)],
        db=agent_db,
        session_id=session_id,
        model=OpenAIChat(id="gpt-4o", api_key=api_key),
        instructions=[
            instructions_prompt,
            "\n### EXPERIÊNCIA E REGRAS DE NEGÓCIO APRENDIDAS:",
            learned_context,
            "\n### DICIONÁRIO DE DADOS (CONTEXTO DO BANCO):",
            db_context
        ],
        markdown=True,
        add_history_to_context=True,
        

    )
        

agent = get_agent()

if __name__ == "__main__":
    agent.print_response("")