"""Aceite RF03/RF04 com Spring AI e Ollama reais no Compose."""
import httpx,time,json,subprocess
from pathlib import Path
# Reutiliza a configuração efetiva do Compose sem duplicar senhas de laboratório.
configuracao=json.loads(subprocess.check_output(['docker','compose','config','--format','json'],text=True))
credenciais=configuracao['services']['core-af']['environment']
c=httpx.Client(base_url='http://127.0.0.1:8085',auth=('camargo',credenciais['AF_ADMIN_PASSWORD']),headers={'X-AF-Request':'1'},timeout=125)
a=c.post('/api/alunos',json={'nome':'Aceite RF03 RF04'});a.raise_for_status();identificador=a.json()['id']
caminho=f'/api/af/alunos/{identificador}'
p={'pergunta':'Quero aprender Java e APIs REST','perfil':'iniciante','autorizaConsulta':False}
for invalido in [dict(p,pergunta='Oi'),dict(p,perfil='administrador')]:
 assert c.post(caminho+'/recomendacao',json=invalido).status_code==400
assert c.post(caminho+'/agente',json=p).status_code==403
r=None
prazo=time.monotonic()+900
while time.monotonic()<prazo:
 r=c.post(caminho+'/recomendacao',json=p)
 if r.status_code==200:break
 assert r.status_code==503,r.text
 time.sleep(5)
assert r.status_code==200,r.text
recomendacao=r.json();assert recomendacao['geracao'] and 'DOC-01' in recomendacao['resposta']
assert 'facens' not in recomendacao['resposta'].lower() and 'trilhas fictícias' in recomendacao['resposta']
sem=c.post(caminho+'/recomendacao',json=dict(p,pergunta='astronomia telescopios'));assert sem.status_code==200 and not sem.json()['geracao']
r=c.post(caminho+'/agente',json=dict(p,autorizaConsulta=True));assert r.status_code==200,r.text
agente=r.json();assert agente['progresso']['cursosConcluidos']==0 and not agente['efeitosExternos']
assert c.post(caminho+'/agente',json=p).status_code==403
outro=httpx.Client(base_url='http://127.0.0.1:8085',auth=('aluno1',credenciais['AF_ALUNO1_PASSWORD']),headers={'X-AF-Request':'1'})
alheio=identificador if identificador!=1 else 2
assert outro.post(f'/api/af/alunos/{alheio}/agente',json=dict(p,autorizaConsulta=True)).status_code==403
subprocess.run(['docker','compose','stop','ollama-af'],check=True)
try:
 assert c.post(caminho+'/recomendacao',json=p).status_code==503
 assert c.get(f'/api/alunos/{identificador}').status_code==200
finally:subprocess.run(['docker','compose','up','-d','--wait','ollama-af'],check=True)
saida=Path('evidencias/af-ci');saida.mkdir(parents=True,exist_ok=True)
(saida/'orientacao-real.json').write_text(json.dumps({'status':'passed','modelo_real':True,'recomendacao':recomendacao,'agente':agente,'isolamento':'403','falha_modelo':'503, consulta preservada'},ensure_ascii=False,indent=2))
c.close();outro.close()
