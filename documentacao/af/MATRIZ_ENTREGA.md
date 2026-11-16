# Matriz de entrega AF

## Fontes e interpretação
- AF_Facens_v2.pdf: estudo de caso escrito para a prova de 01/12/2026. Exige itens a–e, totalizando 2 pontos. Não determina duração de vídeo nem exige código no comando.
- A4: exige execução e análise do laboratório, prints de PostgreSQL, RabbitMQ, API, ML e RAGAS; análise REST, Spring AI e mensageria. A integração ao projeto integrado é explicitamente opcional no texto, com possível uso na AF conforme aula.
- Orientação oral relatada por Gustavo: gravar reunião em dupla e provavelmente evoluir a AC1. Incluímos a implementação e o roteiro como escopo solicitado pela equipe. Não apresentamos duração, papéis ou prazo inventados como instruções da professora.

## Pacote planejado
| Item | Entrega | Critério de verificação |
|---|---|---|
| Organização e ASRs | Respostas a, d e ADR | Justificativas ligadas a requisitos |
| C4 | Contêineres reais e limites de implantação | Diagramas coerentes com Compose |
| AC1 | Core Java preservando promoção e recompensas | Testes anteriores passam |
| ML | Python, classificação e métricas | Modelo treinado; dados sintéticos identificados |
| Treinamento | Job durável e RabbitMQ | Aceita pedido com ML parado; conclui após retomada |
| RAG | Documentos, recuperação e geração | Fontes e execução real do modelo |
| Agente | Ferramentas permitidas e consentimento | Sem ação autorizada, nenhum efeito |
| RAGAS | Serviço e resultados | Apenas métricas efetivamente calculadas |
| Operação | Docker, testes, logs e capturas | Não confundir configuração com execução |
| Reunião | Roteiro e demonstração em dupla | Gravação real pelos integrantes |

## Implementação e evidências

| Requisito | Implementação | Evidência / limite |
|---|---|---|
| RF01 | Cadastro e consulta de alunos e catálogo de cursos persistente | Testes HTTP, H2, PostgreSQL e interface |
| RF02 | Classificação Python; histórico de cursos obtido da AC1 | Modelo real treinado com dados sintéticos |
| RF03 | TF-IDF + Qwen3 local com fontes | demo-integrada.json; quatro documentos didáticos |
| RF04 | Agente de fluxo controlado, consulta somente leitura | agente-integrado.json; consentimento obrigatório |
| RF05 | Job/outbox persistente, consulta de estados | integracao.json; operação administrativa para a equipe |
| RNF01 | Pools, inferência em dois processos e ensaio com 300 usuários | Consultar carga-final.json e histórico; sem extrapolar para produção |
| RNF02 | Aceita com ML ou RabbitMQ interrompidos | Interrupção e retomada reais na CI |
| RNF03 | Contas por papel, escopo do aluno, token entre serviços | 401/403 e testes; OIDC/TLS/auditoria ainda são evolução de produção |
| RNF04 | IA em serviços com APIs e imagens separadas | Regressão da AC1 e indisponibilidade de ML |
| RNF05 | Modelo local sem cobrança de API; poucos serviços centrais | Hardware e operação ainda têm custos |

O vídeo deve ser gravado pela dupla. O documento escrito, o roteiro e o código não substituem a gravação nem autorizam presumir dispensa da prova.
