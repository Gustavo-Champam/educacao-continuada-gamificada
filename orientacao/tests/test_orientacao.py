import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient
spec=importlib.util.spec_from_file_location('orientacao_testada',Path(__file__).parents[1]/'app.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
client=TestClient(mod.app)
def test_recuperacao_retorna_fonte_real():
    fontes=mod.recuperar('Quero estudar Java e APIs REST','iniciante')
    assert fontes[0]['id']=='DOC-01'
    assert fontes[0]['text'] in [d['text'] for d in mod.DOCS]
def test_sem_consentimento_nao_executa_modelo(monkeypatch):
    def proibido(*args):raise AssertionError('Modelo nao deve ser chamado')
    monkeypatch.setattr(mod,'gerar',proibido)
    assert client.post('/agente',json={'pergunta':'Quero Java','autoriza_consulta':False}).status_code==403
def test_sem_configuracao_local_nao_inventa_resposta(monkeypatch):
    monkeypatch.delenv('LOCAL_AI_BASE_URL',raising=False)
    result=client.post('/recomendar',json={'pergunta':'Quero Java e REST'})
    assert result.status_code==503
    assert 'resposta' not in result.json()
def test_rejeita_pergunta_vazia():
    assert client.post('/recomendar',json={'pergunta':''}).status_code==422
