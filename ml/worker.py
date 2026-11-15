import json
import os
import time
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

def run():
    while True:
        try:
            conn=connect(); ch=conn.channel()
            ch.queue_declare(queue=QUEUE,durable=True)
            ch.queue_declare(queue=RESULTS,durable=True)
            ch.basic_qos(prefetch_count=1)
            ch.confirm_delivery()
            def on_message(channel,method,properties,body):
                job=json.loads(body)
                jid=job['job_id']
                import uuid
                uuid.UUID(jid)  # IDs externos não podem formar caminhos arbitrários.
                previous=JOBS/(jid+'.json')
                status=json.loads(previous.read_text(encoding='utf-8')) if previous.exists() else {}
                if status.get('status') not in ('completed','failed'):
                    status={'job_id':jid,'status':'running'}
                    save(jid,status)
                    channel.basic_publish(exchange='',routing_key=RESULTS,body=json.dumps(status),mandatory=True,properties=pika.BasicProperties(delivery_mode=2))
                    try:
                        result=train(job_id=jid,seed=int(job.get('seed',42)))
                        status={'job_id':jid,'status':'completed','metrics':result}
                    except Exception as e:
                        status={'job_id':jid,'status':'failed','error':type(e).__name__}
                    save(jid,status)
                # Em reentrega de job já terminado, publica o resultado salvo sem treinar de novo.
                channel.basic_publish(exchange='',routing_key=RESULTS,body=json.dumps(status),mandatory=True,properties=pika.BasicProperties(delivery_mode=2))
                channel.basic_ack(delivery_tag=method.delivery_tag)
            ch.basic_consume(queue=QUEUE,on_message_callback=on_message)
            print('ML worker pronto',flush=True)
            ch.start_consuming()
        except Exception as e:
            print('Reconectando worker:',e,flush=True)
            time.sleep(5)

if __name__=='__main__':run()
