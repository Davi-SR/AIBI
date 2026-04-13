from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/query")
async def query(query: Query):
    return agent.run(query.query)