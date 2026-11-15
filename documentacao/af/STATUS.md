# Evolução AF em andamento

Autores: Gustavo Gutierres Champam (RA 223645) e Gustavo Oliveira Camargo (RA 236024).

Esta branch evolui a AC1 com a modularização do B1 e os primeiros componentes da AF. Não representa entrega prática completa.

## Verificado em 15/11/2026
- Maven test: 44 testes encontrados, 43 executados com sucesso, um teste PostgreSQL ignorado por ausência do banco local.
- Orientação Python: quatro testes aprovados (recuperação, consentimento, configuração ausente e validação de entrada).
- Qwen3-4B-GGUF executado localmente no Lemonade, sem API paga.
- RAG lexical TF-IDF seguido de geração real: resposta citou DOC-01 para Java/REST. Documentos são exemplos didáticos do laboratório, não documentos reais da FACENS.
- Regressão logística treinada com 1500 registros sintéticos; métricas e divisão constam na evidência JSON.

## Implementado, ainda sem comprovação integrada completa
- Endpoints Java /api/af/alunos/{id}/classificacao, /recomendacao e /agente, ativos no perfil af.
- Job persistente/outbox, publicação AMQP com confirmação e consulta de status; worker com reaproveitamento de resultado em reentrega.
- Agente de fluxo controlado, só leitura, com consentimento. Não é um agente autônomo com escolha livre de ferramentas.

## Pendências
- Executar integração Core–RabbitMQ–worker e testar interrupção/retomada real.
- Adaptar e executar RAGAS com modelo e embeddings locais: evaluation ainda deriva do exemplo com OpenAI; não executar como se já fosse local.
- Completar autenticação/autorização e segregação de acesso. Usar apenas ambiente local com dados fictícios.
- Validar PostgreSQL, Docker, carga de 300 usuários e p95; não alegar atendimento já medido.
- Atualizar C4 conforme implementação final e gravar reunião real entre os integrantes.
- Executamos mvnw test, não mvnw verify: o gate herdado de 100% de cobertura ainda precisa ser revalidado com o código novo.

## Execução parcial
1. Java 17: ./mvnw test; ./mvnw package -DskipTests.
2. Instalar dependências Python de orientacao/requirements.txt e ml/requirements.txt em ambiente virtual.
3. Preparar Lemonade com preparar_ia_local.ps1; iniciar python iniciar_ia_local.py.
4. O serviço de orientação fica em 127.0.0.1:8012. ML deve executar na porta 8011; ML_DATA_DIR aponta para armazenamento persistente e ML_AUTO_TRAIN=false desativa publicação inicial.
5. Core: java -jar target/educacao-gamificada-0.0.1-SNAPSHOT.jar --spring.profiles.active=af --server.address=127.0.0.1.

Os modelos e executáveis locais não são versionados. A primeira preparação requer download. O acesso ao provedor local usa uma credencial efêmera gerada internamente, sem chave de nuvem.
