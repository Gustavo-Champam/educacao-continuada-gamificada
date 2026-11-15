import json
import os
from pathlib import Path
from threading import Lock, Thread
from contextlib import asynccontextmanager
import time
import logging
from typing import Literal
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dataset import FEATURES
from training import DATA_DIR, MODEL, METADATA

log = logging.getLogger('ml.v53')

def publish_training(seed=42, automatic=False):
    """Publica uma única solicitação inicial por vez, sem treinar dentro da API."""
    import pika
    jid=str(uuid.uuid4())
    jobs=DATA_DIR/'jobs'
    jobs.mkdir(parents=True,exist_ok=True)
    marker=jobs/'initial-training.json'
    if automatic:
        if MODEL.exists() and METADATA.exists():
            return {'status':'ready'}
        if marker.exists():
            try:
                old=json.loads(marker.read_text(encoding='utf-8'))
                old_path=jobs/f"{old['job_id']}.json"
                if old_path.exists():
                    state=json.loads(old_path.read_text(encoding='utf-8'))
                    if state.get('status') in ('queued','running') and time.time()-old_path.stat().st_mtime < 600:
                        return old
            except (OSError,ValueError,KeyError):
                pass
    path=jobs/f'{jid}.json'
    status={'job_id':jid,'status':'queued','automatic':automatic}
    path.write_text(json.dumps(status),encoding='utf-8')
    try:
        conn=pika.BlockingConnection(pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST','rabbitmq'),
            credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER','gamification'),os.getenv('RABBITMQ_PASS','gamification')),
            socket_timeout=5,blocked_connection_timeout=10))
        try:
            ch=conn.channel()
            ch.queue_declare(queue='ml.training.requests',durable=True)
            ch.basic_publish(exchange='',routing_key='ml.training.requests',
                body=json.dumps({'job_id':jid,'seed':seed}),
                properties=pika.BasicProperties(delivery_mode=2))
        finally:
            conn.close()
    except Exception as e:
        path.write_text(json.dumps({'job_id':jid,'status':'publish_failed','error':str(e)}),encoding='utf-8')
        raise
    if automatic:
        marker.write_text(json.dumps(status),encoding='utf-8')
    return status

def bootstrap_model():
    for attempt in range(12):
        if MODEL.exists() and METADATA.exists():
            return
        try:
            status=publish_training(42,automatic=True)
            log.info('Treinamento inicial: %s',status)
            return
        except Exception as exc:
            log.warning('RabbitMQ ainda indisponível (%s/12): %s',attempt+1,exc)
            time.sleep(5)

@asynccontextmanager
async def lifespan(app):
    if os.getenv('ML_AUTO_TRAIN','true').lower()=='true':
        Thread(target=bootstrap_model,daemon=True,name='ml-initial-training').start()
    yield

app=FastAPI(title='ML — Perfil de Estudante',version='5.3',lifespan=lifespan)
lock=Lock()
_cached=None
_cached_stamp=None

class Features(BaseModel):
    programming_experience_months: float = Field(ge=0,le=120)
    completed_courses: float = Field(ge=0,le=35)
    average_assessment_score: float = Field(ge=0,le=100)
    weekly_study_hours: float = Field(ge=0,le=30)
    rest_knowledge_score: float = Field(ge=0,le=100)
    database_knowledge_score: float = Field(ge=0,le=100)

def model():
    global _cached,_cached_stamp
    if not MODEL.exists():
        raise HTTPException(status_code=503,detail='Modelo não treinado. Execute o treinamento.')
    stamp=MODEL.stat().st_mtime_ns
    with lock:
        if _cached is None or stamp!=_cached_stamp:
            _cached=joblib.load(MODEL)
            _cached_stamp=stamp
        return _cached

@app.get('/health')
def health():
    ready=MODEL.exists() and METADATA.exists()
    return {'status':'ok','model_ready':ready,'model_status':'ready' if ready else 'training_or_pending'}

@app.get('/readiness')
def readiness():
    ready=MODEL.exists() and METADATA.exists()
    return {'service_ready':True,'model_ready':ready}

@app.get('/training/status')
def initial_training_status():
    marker=DATA_DIR/'jobs'/'initial-training.json'
    if MODEL.exists() and METADATA.exists():
        return {'status':'ready','model_ready':True}
    if marker.exists():
        data=json.loads(marker.read_text(encoding='utf-8'))
        path=DATA_DIR/'jobs'/f"{data['job_id']}.json"
        if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
    return {'status':'pending','model_ready':False}


@app.get('/model')
def metadata():
    if not METADATA.exists(): raise HTTPException(404,'Modelo ainda não disponível')
    return json.loads(METADATA.read_text(encoding='utf-8'))

@app.post('/predict')
def predict(features: Features):
    m=model()
    row=[[getattr(features,k) for k in FEATURES]]
    probabilities=m.predict_proba(row)[0]
    return {'profile':str(m.predict(row)[0]),
            'probabilities':{str(k):round(float(v),6) for k,v in zip(m.classes_,probabilities)},
            'model_version':metadata()['version'], 'synthetic_model':True}

import json
import os
import uuid
from pathlib import Path
import pika
from fastapi import HTTPException
from pydantic import BaseModel, Field

class TrainRequest(BaseModel):
    seed: int = Field(default=42,ge=0,le=100000)

@app.post('/training/jobs',status_code=202)
def submit_training(req: TrainRequest):
    try:
        return publish_training(req.seed,automatic=False)
    except Exception as e:
        raise HTTPException(503,'RabbitMQ indisponível. Consulte os logs do serviço ML.') from e

@app.get('/training/jobs/{job_id}')
def training_status(job_id:uuid.UUID):
    path=DATA_DIR/'jobs'/f'{job_id}.json'
    if not path.exists(): raise HTTPException(404,'Treinamento não encontrado')
    return json.loads(path.read_text(encoding='utf-8'))
