"""Inicia Lemonade privado e serviço RAG; fecha os filhos ao encerrar."""
import os,sys,json,threading,urllib.request,subprocess
from pathlib import Path
from lemond_launcher import start_lemond
ROOT=Path(__file__).parent.resolve()
def main():
    print('[IA local] Iniciando servidor...',flush=True)
    proc,key,port=start_lemond();worker=None
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
        worker=subprocess.Popen([sys.executable,'-m','uvicorn','orientacao.app:app','--host','127.0.0.1','--port','8012'],cwd=ROOT,env=env)
        worker.wait()
    finally:
        if worker and worker.poll() is None:worker.terminate();worker.wait(timeout=15)
        if proc.poll() is None:proc.kill()
        proc.wait()
        print('[IA local] Processos encerrados.',flush=True)
if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:pass
