# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from .simulator import simulate_counter

app = FastAPI()

class SimReq(BaseModel):
    text: str

class SimResp(BaseModel):
    analysis: dict
    sources: list

INDEX_ROOT = Path("rag/index")  # 네가 쓰는 경로로
LLM_PATH   = Path("models/Meta-Llama-3-8B")

@app.post("/simulate", response_model=SimResp)
def simulate(req: SimReq):
    result = simulate_counter(
        opponent_text=req.text,
        index_root=INDEX_ROOT,
        embed_model="BAAI/bge-m3",
        device="cuda",
        pre_k=60,
        final_k=8,
        llm_path=LLM_PATH
    )
    return result