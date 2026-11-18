import json
import os
import time
import uuid
from pathlib import Path
import pika
from training import train

QUEUE='ml.training.requests'
RESULTS='ml.training.results'
JOBS=Path(os.getenv('ML_DATA_DIR','/data'))/'jobs'
JOBS.mkdir(parents=True,exist_ok=True)

def save(job_id, payload):
    tmp=JOBS/(job_id+'.tmp')
    tmp.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    tmp.replace(JOBS/(job_id+'.json'))

def connect():
    return pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST','rabbitmq'),credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER','gamification'),os.getenv('RABBITMQ_PASS','gamification')),heartbeat=600,blocked_connection_timeout=300))

def process_message(channel, method, properties, body):
    """Confirma somente após persistir e publicar o resultado; reentrega é idempotente."""
    try:
        job = json.loads(body)
        jid = str(uuid.UUID(job['job_id']))
        seed = job.get('seed', 42)
        if type(seed) is not int or not 0 <= seed <= 100000:
            raise ValueError('Semente inválida')
    except (ValueError, KeyError, TypeError, AttributeError, UnicodeDecodeError):
        # Isola mensagens inválidas sem bloquear indefinidamente os trabalhos válidos.
        channel.basic_publish(exchange='', routing_key='ml.training.invalid', body=body,
                              mandatory=True, properties=pika.BasicProperties(delivery_mode=2))
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return
    previous = JOBS / (jid + '.json')
    status = json.loads(previous.read_text(encoding='utf-8')) if previous.exists() else {}
    if status.get('status') not in ('completed', 'failed'):
        status = {'job_id': jid, 'status': 'running'}
        save(jid, status)
        channel.basic_publish(exchange='', routing_key=RESULTS, body=json.dumps(status),
                              mandatory=True, properties=pika.BasicProperties(delivery_mode=2))
        try:
            status = {'job_id': jid, 'status': 'completed', 'metrics': train(job_id=jid, seed=seed)}
        except Exception as exc:
            status = {'job_id': jid, 'status': 'failed', 'error': type(exc).__name__}
        save(jid, status)
    channel.basic_publish(exchange='', routing_key=RESULTS, body=json.dumps(status),
                          mandatory=True, properties=pika.BasicProperties(delivery_mode=2))
    channel.basic_ack(delivery_tag=method.delivery_tag)

def run():
    while True:
        try:
            conn=connect(); ch=conn.channel()
            ch.queue_declare(queue=QUEUE,durable=True)
            ch.queue_declare(queue=RESULTS,durable=True)
            ch.queue_declare(queue='ml.training.invalid',durable=True)
            ch.basic_qos(prefetch_count=1)
            ch.confirm_delivery()
            ch.basic_consume(queue=QUEUE,on_message_callback=process_message)
            print('ML worker pronto',flush=True)
            ch.start_consuming()
        except Exception as e:
            print('Reconectando worker:',e,flush=True)
            time.sleep(5)

if __name__=='__main__':run()
