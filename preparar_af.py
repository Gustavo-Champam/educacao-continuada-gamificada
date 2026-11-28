"""Gera credenciais didáticas locais. Nunca sobrescreve um arquivo já configurado."""
from pathlib import Path
import secrets
p=Path(__file__).parent/'.env.af'
if p.exists():
 print('Configuracao existente preservada:',p)
else:
 keys=['AF_ADMIN_PASSWORD','AF_ALUNO1_PASSWORD','AF_ALUNO2_PASSWORD','AF_DB_PASSWORD','AF_RABBIT_PASSWORD','AF_SERVICE_TOKEN']
 p.write_text(''.join(k+'='+secrets.token_urlsafe(24)+'\n' for k in keys),encoding='utf-8')
 print('Configuracao local criada em .env.af. Consulte apenas no seu computador; nao envie ao Git.')
print('Docker: docker compose --env-file .env.af -f compose.af.yaml up -d --build')
print('Interface: http://localhost:8085/af.html; usuarios champam, camargo, aluno1 e aluno2.')
