> **Registro histórico da stack anterior.** Consulte o [README AF v3](../../README.md) e a [entrega RF02/RF05](ENTREGA_CHAMPAM.md) para execução e pendências atuais.

# Executar a AF

Autores: Gustavo Gutierres Champam (RA 223645) e Gustavo Oliveira Camargo (RA 236024).

Use a branch `af/evolucao-ia-local`. A página AF é `/af.html`; a aplicação Vue original continua no laboratório da AC1.

## Preparação uma vez

Pré-requisitos: Git, Python 3.11, Docker Desktop iniciado e GPU/driver compatível com Vulkan para a configuração local usada. A primeira preparação baixa dependências e alguns GB de modelo; depois a geração usa a máquina local. Não há API paga nem cadastro em provedor de IA. CPU/GPU, memória, disco e energia continuam tendo custo operacional.

Execute de cima para baixo, dentro da pasta do repositório:

```powershell
git switch af/evolucao-ia-local
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r orientacao/requirements.txt -r evaluation/requirements.txt -r ml/requirements.txt
.\.venv\Scripts\python.exe preparar_af.py
.\preparar_ia_local.ps1
```

O script cria `.env.af` com senhas aleatórias. Abra esse arquivo **somente no computador**, copie `AF_ADMIN_PASSWORD` e use a conta `champam` ou `camargo` na interface. Não envie esse arquivo ao Git ou na entrega. Alunos usam as próprias senhas e IDs didáticos 1 e 2; o gestor deve cadastrar esses dois primeiros alunos antes da demonstração de segregação.

## Terminal 1: orientação e avaliação locais

```powershell
$env:AF_AI_HOST = '0.0.0.0'
.\.venv\Scripts\python.exe iniciar_ia_local.py
```

Esse endereço permite acesso dos contêineres ao serviço no host. O launcher exige o token gerado em `.env.af` para esse modo. Não exponha portas na Internet. Mantenha o terminal aberto; Ctrl+C encerra os processos filhos. O primeiro uso instala/verifica o backend, baixa o modelo e pode demorar. A geração e o juiz RAGAS usam Qwen3 local; o pacote `langchain-openai` é apenas um cliente compatível com a API local.

## Terminal 2: negócios, banco, filas e ML

```powershell
docker compose --env-file .env.af -f compose.af.yaml up -d --build
Start-Process 'http://localhost:8085/af.html'
```

Na interface, cadastre os alunos e um curso. Clique em **Solicitar treinamento**, aguarde e use **Atualizar andamento** até `completed`. Só depois classifique. Informe um objetivo como “Quero aprender Java e APIs REST” e consulte o RAG. Para o agente, marque o consentimento. A classificação usa o histórico de conclusões da AC1; o catálogo é administrativo e as trilhas RAG são documentos didáticos versionados, não extraídos automaticamente do catálogo.

Para RAGAS: gere uma recomendação, clique em **Avaliar última resposta**, aguarde e atualize as métricas. Sem resposta de referência, calcula fidelidade e relevância; com referência, solicita também precisão e recuperação de contexto. São estimativas do juiz local. O ensaio entregue calculou apenas as duas primeiras.

```powershell
docker compose --env-file .env.af -f compose.af.yaml ps
docker compose --env-file .env.af -f compose.af.yaml logs --tail 50 core-af ml-worker-af
```

RabbitMQ: `http://localhost:15675`, usuário `gamification`, senha `AF_RABBIT_PASSWORD` do arquivo local. PostgreSQL: porta 55435, banco `educacao_af`, usuário `educacao`, senha `AF_DB_PASSWORD`. Os volumes preservam dados; `down` encerra sem removê-los.

## Testes

Java 17 e Maven Wrapper:

```powershell
.\mvnw.cmd verify
```

Python, no ambiente preparado:

```powershell
.\.venv\Scripts\python.exe -m pytest orientacao/tests -q
Push-Location ml
..\.venv\Scripts\python.exe -m unittest test_predict -v
Pop-Location
```

O pytest é dependência de desenvolvimento (`pip install pytest`). O workflow `AF - integracao e carga reais` executa interrupção de ML/broker, recuperação, catálogo, classificação, carga e interface. Use a execução registrada em STATUS.md para consultar os artefatos.

`scripts/validar-af.py` é um teste de ambiente descartável, espera banco inicialmente vazio e para serviços intencionalmente. Não rode sobre seus dados de demonstração. A CI cria esse ambiente isolado a cada execução. O protocolo final registra três rajadas iniciais, aquece por 30 segundos e mede 60 segundos sustentados com 300 usuários, dois alunos e entradas variadas. A conclusão principal vale para esse regime aquecido; não garante partida fria nem capacidade em outra infraestrutura.

## Neste computador

A integração Docker foi executada no GitHub Actions porque o Docker local não estava disponível. O fluxo Core/H2, ML e RAG foi verificado no Windows; ele não comprova RabbitMQ local. Para gravar a reunião, é possível mostrar a execução real da CI e a interface local, explicando essa diferença. Para repetir toda a stack no próprio computador, é necessário instalar/configurar Docker Desktop e eventualmente reiniciar o Windows.

Com Java 17 no PATH e `.venv` preparada, `./iniciar_demo_local.ps1` inicia a demonstração sem Docker, treina o modelo sintético e mantém os processos até você pressionar Enter. Não rode junto à stack Docker: as portas são iguais. Nesse modo, mostre o treinamento assíncrono pela evidência da CI; não apresente a fila local como funcionando.

## O que a dupla faz manualmente

1. Ler o relatório e ensaiar o roteiro com os resultados exibidos nos JSONs.
2. Gravar a conversa real dos dois integrantes e a demonstração; não mostrar senhas.
3. Conferir no Canvas a orientação final da professora sobre vídeo e formato de envio.
4. Enviar PDF, link desta branch (ou ZIP do código) e vídeo conforme o campo da atividade. O vídeo não foi gravado pelo projeto e não está incluído no ZIP.

Não atribuímos nota garantida. A correção depende da professora e a prova escrita continua indicada nos documentos fornecidos.
