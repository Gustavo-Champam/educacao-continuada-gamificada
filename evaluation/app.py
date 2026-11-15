"""Serviço didático de avaliação offline de execuções RAG. Não inventa métricas.
As métricas de contexto com referência só são executadas quando o professor a fornece.
"""
import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Gamification RAGAS Evaluation", version="4.1")
STORE = Path("/data/experiments")
STORE.mkdir(parents=True, exist_ok=True)
lock = threading.Lock()

class EvaluateRequest(BaseModel):
    trace_id: int
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    contexts: List[str] = Field(min_length=1)
    reference: str = ""

def save(job):
    with lock:
        target = STORE / (job["id"] + ".json")
        tmp = target.with_suffix(".tmp")
        tmp.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(target)

def read(job_id):
    try: uuid.UUID(job_id)
    except ValueError: raise HTTPException(400, "ID inválido")
    path = STORE / (job_id + ".json")
    if not path.exists(): raise HTTPException(404, "Avaliação não encontrada")
    return json.loads(path.read_text(encoding="utf-8"))

def evaluate_async(job, req):
    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from ragas.llms import LangchainLLMWrapper
        from ragas.embeddings import LangchainEmbeddingsWrapper
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY ausente")
        metrics = [faithfulness, answer_relevancy]
        record = {"question":req.question,"answer":req.answer,"contexts":req.contexts}
        if req.reference.strip():
            record["ground_truth"] = req.reference.strip()
            metrics.extend([context_precision, context_recall])
        dataset = Dataset.from_list([record])
        result = evaluate(
            dataset=dataset, metrics=metrics,
            llm=LangchainLLMWrapper(ChatOpenAI(model=os.getenv("RAGAS_JUDGE_MODEL","gpt-4o-mini"),temperature=0)),
            embeddings=LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small")),
            raise_exceptions=True,
        )
        scores = result.to_pandas().iloc[0].to_dict()
        selected = {m.name: (None if scores.get(m.name) is None else float(scores[m.name])) for m in metrics}
        job.update(status="completed", scores=selected)
    except Exception as exc:
        job.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    finally:
        job["finished_at"] = datetime.now(timezone.utc).isoformat()
        save(job)

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/experiments/run", status_code=202)
def run(req: EvaluateRequest):
    job = {"id":str(uuid.uuid4()),"trace_id":req.trace_id,"status":"running",
           "created_at":datetime.now(timezone.utc).isoformat(),
           "metrics_requested":["faithfulness","answer_relevancy"] +
           (["context_precision","context_recall"] if req.reference.strip() else []),
           "reference_supplied":bool(req.reference.strip())}
    save(job)
    threading.Thread(target=evaluate_async,args=(job,req),daemon=True).start()
    return {"id":job["id"],"status":job["status"]}

@app.get("/experiments/{job_id}")
def get(job_id: str): return read(job_id)

@app.get("/experiments")
def list_jobs():
    return sorted([json.loads(p.read_text(encoding="utf-8")) for p in STORE.glob("*.json")],
                  key=lambda x:x["created_at"],reverse=True)[:50]
