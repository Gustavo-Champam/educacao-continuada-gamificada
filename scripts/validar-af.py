"""Integração real por HTTP e interrupção de containers. Não usa mocks."""
import os,json,time,subprocess,statistics,concurrent.futures,threading
from pathlib import Path
import httpx
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidencias/af-ci';OUT.mkdir(parents=True,exist_ok=True)
config=dict(line.split('=',1) for line in (ROOT/'.env.af').read_text().splitlines() if '=' in line)
base='http://127.0.0.1:8085';headers={'X-AF-Request':'1'}
client=httpx.Client(base_url=base,auth=('champam',config['AF_ADMIN_PASSWORD']),headers=headers,timeout=15,trust_env=False,limits=httpx.Limits(max_connections=350,max_keepalive_connections=350))
def compose(*args):subprocess.run(['docker','compose','--env-file','.env.af','-f','compose.af.yaml',*args],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
def wait(path,condition=lambda x:True,seconds=180):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  try:
   r=client.get(path)
   if r.is_success and condition(r.json()):return r.json()
  except httpx.HTTPError:pass
  time.sleep(2)
 raise RuntimeError('Tempo excedido: '+path)
def state(v):return v.get('status',v.get('STATUS'))
wait('/actuator/health')
students=[]
for name in ['Ana AF','Bruno AF']:
 r=client.post('/api/alunos',json={'nome':name});r.raise_for_status();students.append(r.json())
assert students[0]['id']==1 and students[1]['id']==2
assert httpx.get(base+'/api/alunos').status_code==401
assert httpx.get(base+'/api/alunos/2',auth=('aluno1',config['AF_ALUNO1_PASSWORD'])).status_code==403
assert httpx.get(base+'/api/alunos/1',auth=('aluno1',config['AF_ALUNO1_PASSWORD'])).status_code==200
assert client.post('/api/af/alunos/1/agente',json={'pergunta':'Java REST','perfil':'iniciante','autorizaConsulta':False}).status_code==403
# Preservar a regra original da AC1 e validar 1203 pontos após promoção.
for i in range(12):
 r=client.post('/api/alunos/1/conclusoes',json={'codigoCurso':f'AF-{i}','media':8});r.raise_for_status()
aluno=client.get('/api/alunos/1').json();assert aluno['plano']=='PREMIUM' and aluno['moedas']==3 and aluno['vouchers']==1
# API ML e worker parados: o Core ainda aceita o pedido e a fila retém a mensagem.
compose('stop','ml-worker-af','ml-af')
r=client.post('/api/af/treinamentos');assert r.status_code==202;job=r.json();time.sleep(8)
queued=wait(job['consulta'],lambda v:state(v)=='queued')
# API retorna, consumidor continua parado: pedido não conclui antecipadamente.
compose('start','ml-af');time.sleep(3);assert state(client.get(job['consulta']).json())=='queued'
compose('start','ml-worker-af');finished=wait(job['consulta'],lambda v:state(v)=='completed',240)
features={'experienciaMeses':12,'nota':80,'horasSemanais':6,'conhecimentoRest':70,'conhecimentoBanco':80}
result=client.post('/api/af/alunos/1/classificacao',json=features);result.raise_for_status()
# Broker parado: o registro persiste sem confirmação de publicação; retoma depois.
compose('stop','rabbitmq-af');r=client.post('/api/af/treinamentos');assert r.status_code==202;job2=r.json();time.sleep(4);assert state(client.get(job2['consulta']).json())=='received'
compose('start','rabbitmq-af');finished2=wait(job2['consulta'],lambda v:state(v)=='completed',240)
report={'aluno_promovido':aluno,'job_ml_offline':job,'estado_em_fila':queued,'conclusao':finished,'job_broker_offline':job2,'conclusao_apos_retomada':finished2,'classificacao':result.json(),'seguranca':'401 anonimo, 403 outro aluno e agente sem consentimento, 200 proprio aluno'}
(OUT/'integracao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
# Carga: 3 ondas, 300 usuários liberados simultaneamente por onda, após 20 aquecimentos.
for _ in range(20):client.post('/api/af/alunos/1/classificacao',json=features).raise_for_status()
latencies=[];errors=[]
for wave in range(3):
 barrier=threading.Barrier(300)
 def request(i):
  barrier.wait(timeout=30);start=time.perf_counter()
  try:
   r=client.post('/api/af/alunos/1/classificacao',json=features)
   return time.perf_counter()-start,r.status_code
  except httpx.HTTPError:return time.perf_counter()-start,0
 with concurrent.futures.ThreadPoolExecutor(max_workers=300) as pool:
  for elapsed,status in pool.map(request,range(300)):
   latencies.append(elapsed)
   if status!=200:errors.append(status)
latencies.sort();p95=latencies[int(len(latencies)*.95)-1]
load={'usuarios_simultaneos':300,'ondas':3,'requisicoes':len(latencies),'aquecimentos':20,'p95_segundos':p95,'erros':len(errors),'status_erros':errors,'criterio_atendido':p95<=2 and not errors,'ambiente':'GitHub Actions ubuntu-24.04, Docker, rede local do runner; teste de rajadas, nao carga sustentada'}
(OUT/'carga.json').write_text(json.dumps(load,indent=2))
print(json.dumps(load))
