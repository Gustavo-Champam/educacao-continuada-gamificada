# Evidências da entrega

Execução local: **14/09/2026**, Java 17, Maven, JUnit 5, PostgreSQL 18 dedicado e H2. Capturas de navegador são reais. Nenhuma captura de IntelliJ ou Docker Desktop foi simulada.

## Testes e cobertura

- [RED JUnit US01](red/us01-junit.log) e [GREEN JUnit US01](green/us01-junit.log), reexecutados a partir dos commits históricos.

- [RED: três falhas JUnit US02](red/us02-junit.log).
- [RED: aceite HTTP e idempotência](red/us02-aceitacao.log).
- [RED: histórico da carteira ausente](red/historico-carteira.log).
- [GREEN: testes aprovados](green/us02-junit.log).
- [BLUE: 37 testes aprovados, nenhum ignorado](blue/verificacao-completa.log).
- [Relatório JaCoCo completo](blue/cobertura/index.html) e [CSV](blue/cobertura/jacoco.csv).
- [Build Vue](blue/vue-build.log) e [teste de navegador](blue/vue-e2e.log).

![Cobertura JaCoCo](blue/cobertura.png)

## Aplicação em execução

![Vue desktop](execucao/vue-desktop.png)

[Visualização móvel](execucao/vue-mobile.png).

![Swagger](execucao/swagger.png)

![H2 com consultas SQL](execucao/h2-console.png)

[Respostas HTTP e histórico com H2](execucao/h2-http.json).

[Respostas HTTP com PostgreSQL](execucao/postgres-http.json) e [consultas SQL reais](execucao/postgres-sql.txt).

## PostgreSQL e Docker

O teste PostgreSQL executou em banco real, confirmando o produto JDBC e a persistência da promoção e dos saldos após limpar o contexto JPA. Consulte `AlunoPostgresTest` e o log BLUE.

A verificação Docker é realizada pelo job `docker` em [GitHub Actions](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions). O artefato `docker-e-interface` contém logs, lista dos containers, consultas PostgreSQL, aceite HTTP de H2/PostgreSQL e capturas de navegador. **Resultado confirmado: SUCCESS** na [execução 34880100641](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/34880100641), código `29a20e7`. Todos os três jobs passaram.

No computador local, Docker Desktop falhou antes de iniciar o engine com `initializing Inference manager ... socket: Foi usado um endereço incompatível com o protocolo solicitado`. Os testes locais de PostgreSQL não são apresentados como execução local em container.

## IntelliJ Ultimate e Canvas

Para a comprovação específica na IDE, abrir o projeto no IntelliJ Ultimate, executar os testes históricos indicados no README e capturar o resultado do BLUE usando Run with Coverage. Os logs Maven/JUnit comprovam os resultados automatizados, mas não comprovam uso da IDE.

O link do repositório deve ser enviado pelo integrante no Canvas. Não houve postagem automática.


## Comprovantes Docker concluídos

- [Containers em execução](execucao/docker-ps.txt): API, Vue, PostgreSQL, pgAdmin e H2.
- [Aceite PostgreSQL em container](execucao/docker-postgres.json).
- [Aceite H2 em container](execucao/docker-h2.json).
- [Consultas SQL no PostgreSQL em container](execucao/docker-postgres-sql.txt).
- [Logs dos serviços](execucao/docker.log).
- [Relatório de navegador contra os containers](execucao/docker-playwright.html).

![Vue conectado ao Spring e PostgreSQL em Docker](execucao/docker-vue-desktop.png)

O endpoint `/misc/ping` do pgAdmin respondeu com sucesso no job. A evidência comprova execução do serviço, sem simular uma captura de login na ferramenta.
