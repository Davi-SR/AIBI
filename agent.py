from agno.agent import Agent
from agno.tools.sql import SQLTools
from agno.models.groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

db_url = os.getenv("DB_URL")

with open("prompt.md", "r", encoding="utf-8") as f:
    prompt = f.read()

agent = Agent(tools=[SQLTools(db_url=db_url)],
        instructions=[prompt],
        model=Groq(id="llama-3.3-70b-versatile"),
        markdown=True,
        add_history_to_context=True
    )
agent.run()