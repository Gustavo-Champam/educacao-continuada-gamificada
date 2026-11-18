"""Integração real por HTTP e interrupção de containers. Não usa mocks."""
import os,json,time,subprocess,asyncio
from pathlib import Path
import httpx,aiohttp,base64
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidencias/af-ci';OUT.mkdir(parents=True,exist_ok=True)
config={key:os.getenv(key,value) for key,value in {'AF_DB_PASSWORD': 'af_demo_database', 'AF_RABBIT_PASSWORD': 'af_demo_rabbit', 'AF_ADMIN_PASSWORD': 'af-demo-champam-2026', 'AF_ALUNO1_PASSWORD': 'af-demo-aluno1-2026', 'AF_ALUNO2_PASSWORD': 'af-demo-aluno2-2026', 'AF_SERVICE_TOKEN': 'af-demo-internal-2026'}.items()}
base='http://127.0.0.1:8085';headers={'X-AF-Request':'1'}
client=httpx.Client(base_url=base,auth=('champam',config['AF_ADMIN_PASSWORD']),headers=headers,timeout=15,trust_env=False,limits=httpx.Limits(max_connections=350,max_keepalive_connections=350))
def compose(*args):subprocess.run(['docker','compose',*args],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
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
wait('/actuator/health',seconds=600)
course={'codigo':'JAVA-01','nome':'Java e APIs REST','descricao':'Trilha didatica de Java e REST'}
assert client.post('/api/af/cursos',json=course).status_code==201
assert client.post('/api/af/cursos',json=course).status_code==409
assert client.get('/api/af/cursos').json()==[course]
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
# Protocolo fixo: 3 rajadas iniciais registradas, 30 s de aquecimento,
# depois 60 s de carga sustentada. Não descartar rajadas lentas do relatório.
async def measure():
 authorization='Basic '+base64.b64encode(('champam:'+config['AF_ADMIN_PASSWORD']).encode()).decode()
 async with aiohttp.ClientSession(headers={**headers,'Authorization':authorization},timeout=aiohttp.ClientTimeout(total=15),connector=aiohttp.TCPConnector(limit=350)) as load_client:
  async def request(user):
   body={**features,'experienciaMeses':user%49,'nota':70+user%30}
   start=time.perf_counter()
   try:
    async with load_client.post(base+'/api/af/alunos/'+str(1+user%2)+'/classificacao',json=body) as r:
     await r.read()
     return time.perf_counter()-start,r.status
   except (aiohttp.ClientError,asyncio.TimeoutError):return time.perf_counter()-start,0
  def summarize(results):
   times=sorted(t for t,status in results);errors=[status for t,status in results if status!=200]
   p95=times[max(0,__import__('math').ceil(len(times)*.95)-1)]
   return {'requisicoes':len(times),'p95_segundos':p95,'erros':len(errors),'status_erros':errors,'criterio_atendido':p95<=2 and not errors}
  waves=[]
  for wave in range(3):
   waves.append({'onda':wave+1,**summarize(await asyncio.gather(*(request(i) for i in range(300))))})
  async def sustained(seconds):
   gate=asyncio.Event();deadline=0
   async def user_loop(user):
    await gate.wait();samples=[]
    while time.perf_counter()<deadline:
     samples.append(await request(user))
    return samples
   tasks=[asyncio.create_task(user_loop(i)) for i in range(300)]
   await asyncio.sleep(0);deadline=time.perf_counter()+seconds;gate.set()
   results=await asyncio.gather(*tasks)
   return summarize([sample for user in results for sample in user])
  warm=await sustained(30)
  measured=await sustained(60)
  return {**measured,'partida_rajadas':waves,'aquecimento':warm}
load=asyncio.run(measure())
load.update({'gerador':'aiohttp '+aiohttp.__version__+', 300 usuarios em loop fechado, 2 alunos e entradas variadas','usuarios_simultaneos':300,'duracao_medida_segundos':60,'aquecimento_segundos':30,'observacao':'Rajadas iniciais e aquecimento reportados separadamente; criterio principal avalia os 60 s seguintes. Nao garante latencia de partida fria.','ambiente':'GitHub Actions ubuntu-24.04, Docker, rede local do runner; gerador e servicos no mesmo host'})
(OUT/'carga.json').write_text(json.dumps(load,indent=2))
print(json.dumps(load))
assert load['criterio_atendido'], 'RNF01 em regime aquecido: p95 deve ser <= 2 s, sem erros, com 300 usuarios simultaneos'
