# Divisão da AF v3 e revisão técnica

Planejamento registrado em 18/11/2026. Este documento distribui o trabalho futuro; não altera nem reatribui a autoria dos commits existentes.

Projeto: **EducaTrilha AI - Educação Continuada Gamificada**. Evolução da AC1 para classificação, orientação e acompanhamento de aprendizagem.

| Integrante | Papel | Dois requisitos AF |
|---|---|---|
| Gustavo Gutierres Champam - RA 223645 - `Gustavo-Champam` | Tech lead principal e desenvolvimento de ML/mensageria | RF02: classificação de competências com FastAPI; RF05: solicitação e acompanhamento do treinamento |
| Gustavo Oliveira Camargo - RA 236024 - `gustavocamargo1904` | Desenvolvimento de orientação com Spring AI; revisor técnico dos PRs de Champam | RF03: recomendação RAG; RF04: agente de orientação/acompanhamento com autorização |

RF01 (cadastros) é base herdada e não é contado como um dos quatro requisitos inéditos da dupla. A novidade de RF02-RF05 deve ser demonstrada comparando com as entregas AC1 e AC2, não apenas com o código experimental anterior da própria AF.

## Evidência histórica observada

- Champam: commits de regras, API, persistência, frontend, Docker, testes e integração; posteriormente, evolução experimental da AF.
- Camargo: commits `771bb31` e `2a0d552` alteram o README com o mesmo patch, em históricos distintos. Não são duas implementações independentes. O README registra sua responsabilidade pela US01/BDD da AC1; o conteúdo desses commits é documental.
- Histórico observado: não foram encontrados PRs na consulta pública do repositório em 18/11/2026. Merge commits ou mensagens de integração, por si só, não comprovam aprovação de PR.

Referências: [commit Camargo](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/commit/2a0d552a562867856dbb6b66c7187bd30694eda1) e [histórico da evolução AF](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/commits/af/evolucao-ia-local/).

## Entregas por requisito

- RF02 / Champam: contrato e integração Core-FastAPI, inferência, validação de entrada, dados de treino identificados, testes e evidência de desempenho.
- RF05 / Champam: job persistente/outbox, publicação AMQP, worker, consulta de estados, interface e teste de interrupção/retomada.
- RF03 / Camargo: serviço Spring AI real, recuperação documental e geração local sem API paga, fontes na resposta, interface e testes de recuperação/falha.
- RF04 / Camargo: consentimento, acesso às ferramentas permitidas, orientação com contexto de progresso, demonstração de recusa e execução autorizada, testes e limites documentados.
- Infraestrutura compartilhada: gateway obrigatório, frontend, Compose padrão, C4 completo no README, três ASRs e ADR. Esses itens não substituem os dois requisitos individuais.

## Fluxo de contribuição e aprovação

1. Cada integrante trabalha em sua branch com a própria conta, revisa e compreende as alterações, executa os testes e registra seus commits reais.
2. Branches sugeridas: `feat/af-champam-rf02-rf05` e `feat/af-camargo-rf03-rf04`. A branch de adequação compartilhada preserva os experimentos anteriores.
3. Cada integrante abre seu PR para `main`, descrevendo requisitos, código, documentação e evidências.
4. Champam revisa os PRs de Camargo. Camargo atua como revisor técnico/tech lead substituto nos PRs de Champam. O autor não aprova o próprio PR. Se a professora exigir um único tech lead para toda aprovação, confirmar com ela como tratar o PR do próprio tech lead numa equipe de dois.
5. Após revisão real, correções e checks aprovados, realizar o merge. Não marcar uma aprovação ainda não realizada nem mudar o autor do código antigo para simular participação.
6. No vídeo, cada um mostra seus dois requisitos, arquivos, commits, PRs e contribuição na arquitetura. Todos mantêm a câmera aberta.

## Regras novas que substituem o roteiro anterior

- Vídeo de **20 minutos**, publicado como **não listado no YouTube**; entregar o link. Não enviar somente arquivo de vídeo ou outro serviço de hospedagem.
- Frontend e backend executados por **`docker compose up --build`**, sem argumentos adicionais necessários para iniciar a aplicação.
- Spring Boot, Spring AI e FastAPI efetivamente utilizados; não basta mencionar Spring AI no diagrama.
- README com C4 completo; apresentação obrigatória de gateway e arquitetura hexagonal ou clean.
- Sequência a-i: equipe/nome do projeto/data; problema e requisitos; C4 no README; serviços/módulos; microsserviços e gateway; hexagonal/clean; comunicação síncrona/assíncrona; limitações; considerações finais.

O roteiro anterior de 10-12 minutos e a stack dependente de processos iniciados fora do Docker não atendem a essas novas instruções. As evidências anteriores permanecem históricas; a stack v3 precisa de nova validação.
