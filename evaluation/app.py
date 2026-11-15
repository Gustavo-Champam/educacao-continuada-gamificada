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
STORE = Path(os.getenv("EVALUATION_DATA_DIR","./runtime/evaluation"))
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
        from langchain_openai import ChatOpenAI
        from langchain_core.embeddings import Embeddings
        from fastembed import TextEmbedding
        from ragas.run_config import RunConfig
        from ragas.llms import LangchainLLMWrapper
        from ragas.embeddings import LangchainEmbeddingsWrapper
        base=os.environ.get("LOCAL_AI_BASE_URL","")
        key=os.environ.get("LOCAL_AI_KEY","")
        if not base or not key:raise RuntimeError("Inicie a avaliacao pelo launcher de IA local")
        class LocalEmbeddings(Embeddings):
            def __init__(self):
                self.model=TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",cache_dir=os.getenv("EMBEDDINGS_CACHE","./runtime/embeddings"),threads=2)
            def embed_documents(self,texts):return [v.tolist() for v in self.model.embed(texts)]
            def embed_query(self,text):return self.embed_documents([text])[0]
        metrics = [faithfulness, answer_relevancy]
        record = {"question":req.question,"answer":req.answer,"contexts":req.contexts}
        if req.reference.strip():
            record["ground_truth"] = req.reference.strip()
            metrics.extend([context_precision, context_recall])
        dataset = Dataset.from_list([record])
        result = evaluate(
            dataset=dataset, metrics=metrics,
            llm=LangchainLLMWrapper(ChatOpenAI(model=os.getenv("LOCAL_AI_MODEL","Qwen3-4B-GGUF"),base_url=base,api_key=key,timeout=120,max_retries=0,max_tokens=2500,temperature=0,extra_body={"ctx_size":8192,"chat_template_kwargs":{"enable_thinking":False}})),
            embeddings=LangchainEmbeddingsWrapper(LocalEmbeddings()),
            raise_exceptions=True,
            run_config=RunConfig(timeout=180,max_retries=1,max_workers=1),
        )
        scores = result.to_pandas().iloc[0].to_dict()
        selected = {m.name: (None if scores.get(m.name) is None else float(scores[m.name])) for m in metrics}
        job.update(status="completed", scores=selected,judge="Qwen3-4B-GGUF local",embeddings="paraphrase-multilingual-MiniLM-L12-v2 local")
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


@app.middleware("http")
async def service_auth(request,call_next):
    import secrets
    from starlette.responses import JSONResponse
    expected=os.environ.get("AF_SERVICE_TOKEN","")
    if expected and not secrets.compare_digest(request.headers.get("X-AF-Service",""),expected):
        return JSONResponse({"detail":"Acesso de servico nao autorizado"},status_code=401)
    return await call_next(request)
