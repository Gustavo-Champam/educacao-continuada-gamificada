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

## Situação desta preparação
Fontes relidas e projetos de referência extraídos. Base AC1/B1 copiada para core; ML e avaliação provenientes do laboratório V5.3.2. A cópia é ponto de partida: ainda não comprova integração, execução ou conclusão da AF prática.

O computador não possui Docker no caminho padrão nem no PATH verificado. O laboratório de referência depende de API de LLM para RAG/RAGAS. A opção de execução do modelo está sendo definida sem publicar credenciais nem contratar serviços.
