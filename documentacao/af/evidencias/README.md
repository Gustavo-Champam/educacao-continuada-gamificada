# Evidências AF

Código funcional validado: `6c9e499a40ab709d234a72cb10b4cb88f40cf323`.

- `carga-final.json`: medição Docker/CI, 300 usuários, 60 segundos, 70.179 consultas, p95 0,354 s e zero erros. Inclui rajadas iniciais e aquecimento.
- `integracao.json`: regras da AC1, autorização, treinamento com ML interrompido e com RabbitMQ interrompido, retomada e classificação.
- `interface-ci.json` e `interface-ci.png`: consultas e classificação reais na interface AF; recusa do agente sem consentimento.
- `containers-ci.txt` e `commit-ci.txt`: serviços e revisão da execução.
- `testes-java-ci.json`: 56 testes, nenhum ignorado; JaCoCo 100% de linhas e ramificações. `testes-java-local.json` distingue o teste PostgreSQL ignorado no Windows.
- `testes-python.json`: quatro testes de orientação e um de equivalência da inferência.
- `demo-integrada.json` e `demo-af.png`: navegador Windows, Core/H2, ML e RAG reais. Não comprovam fila local.
- `agente-integrado.json`: consulta consentida, fontes e passos do agente somente leitura.
- `ragas-integrado.json` e `ragas-interface.png`: avaliação iniciada pelo Core e exibida na interface; fidelidade 1,000 e relevância 0,862. `ragas-inicial.json` preserva o primeiro ensaio separado, com relevância 0,870.
- `ml-training.json`: modelo e métricas sobre dados sintéticos.
- `rag-real.json` e `primeira-inferencia.json`: primeiros ensaios locais, anteriores à validação pela interface.
- `historico-carga.json`: tentativas anteriores, inclusive falhas; mudanças de gerador e protocolo estão identificadas. `diagnostico-gerador.json` registra a comparação local que motivou o uso de aiohttp.

Execuções públicas: [AF](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/43948164512) e [regressão AC1](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/43948164464).

Estas evidências demonstram os cenários descritos, não qualidade universal nem nota garantida. Os valores RAGAS são de uma amostra didática e juiz local. A gravação da reunião deve ser feita pelos integrantes.
