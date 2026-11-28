"""Inicia Lemonade privado e serviço RAG; fecha os filhos ao encerrar."""
import os,sys,json,threading,urllib.request,subprocess
from pathlib import Path
from lemond_launcher import start_lemond, stop_lemond
ROOT=Path(__file__).parent.resolve()
def main():
    config=ROOT/'.env.af'
    if config.exists():
        for line in config.read_text(encoding='utf-8').splitlines():
            if '=' in line and not line.startswith('#'):
                k,v=line.split('=',1);os.environ[k]=v
    if os.getenv('AF_AI_HOST','127.0.0.1')!='127.0.0.1' and not os.getenv('AF_SERVICE_TOKEN'):
        raise RuntimeError('Gere .env.af antes de permitir conexoes dos containers')
    print('[IA local] Iniciando servidor...',flush=True)
    proc,key,port=start_lemond();workers=[]
    def drain():
        for _ in proc.stdout: pass
    threading.Thread(target=drain,daemon=True).start()
    def api(path,body):
        req=urllib.request.Request(f'http://127.0.0.1:{port}/api/v1/{path}',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=3600) as r:return r.read()
    try:
        print('[IA local] Servidor saudavel. Verificando backend...',flush=True)
        api('install',{'recipe':'llamacpp','backend':'vulkan'})
        model='Qwen3-4B-GGUF'
        print('[IA local] Baixando/verificando modelo. Primeiro uso pode demorar.',flush=True)
        api('pull',{'model':model})
        env={**os.environ,'LOCAL_AI_BASE_URL':f'http://127.0.0.1:{port}/api/v1','LOCAL_AI_KEY':key,'LOCAL_AI_MODEL':model}
        print('[IA local] Modelo no disco. Iniciando orientacao em 127.0.0.1:8012',flush=True)
        env.update({'EVALUATION_DATA_DIR':str(ROOT/'runtime/evaluation'),'EMBEDDINGS_CACHE':str(ROOT/'runtime/embeddings')})
        for module,api_port in [('orientacao.app:app','8012'),('evaluation.app:app','8013')]:
            workers.append(subprocess.Popen([sys.executable,'-m','uvicorn',module,'--host',os.getenv('AF_AI_HOST','127.0.0.1'),'--port',api_port],cwd=ROOT,env=env))
        print('[IA local] Orientacao 8012 e avaliacao RAGAS 8013. Ctrl+C encerra.',flush=True)
        workers[0].wait()
    finally:
        for worker in workers:stop_lemond(worker)
        stop_lemond(proc)
        print('[IA local] Processos encerrados.',flush=True)
if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:pass
