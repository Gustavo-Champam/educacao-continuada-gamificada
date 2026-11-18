# RF02 e RF05 — Gustavo Gutierres Champam, RA 223645

## Escopo

Esta entrega implementa classificação de competências e treinamento assíncrono como extensão da AC1. O cadastro, a promoção após 12 cursos e as recompensas da AC1 permanecem como base, sem contá-los como requisitos inéditos.

RF03/RF04 e a integração Spring AI são responsabilidade atribuída ao Camargo. A existência dos adaptadores experimentais de orientação não comprova essa implementação nem sua autoria. A aprovação do PR e a gravação são etapas humanas pendentes.

## RF02 — classificação

Entrada HTTP: `POST /api/af/alunos/{id}/classificacao`. O Core valida a avaliação e consulta o histórico real do aluno; o cliente não fornece a quantidade de cursos concluídos. O caso de uso `ClassificarCompetencias` depende de duas portas Java: `HistoricoAluno` e `Classificador`. Os adaptadores de composição no controller usam `AlunoService` e HTTP para FastAPI. O resultado contém perfil, probabilidades, versão e indicação de dados sintéticos.

O modelo usa StandardScaler e regressão logística. A base de 1.500 exemplos sintéticos é dividida em treino, validação e teste com semente explícita. Não são dados reais de aprendizagem e as métricas não comprovam eficácia pedagógica. O teste Python compara a previsão HTTP interna com o pipeline realmente treinado, incluindo recarga após novo treinamento.

## RF05 — treinamento e status

`POST /api/af/treinamentos` grava uma linha persistente e retorna 202 com endereço de consulta. A própria linha funciona como outbox. O publicador só marca a publicação após confirmação do RabbitMQ e ausência de retorno por falta de rota. O worker processa uma mensagem por vez e grava o resultado antes do ACK. Em reentrega após término, republica o resultado sem treinar novamente. Se morrer durante o treino, a tentativa pode ser refeita: a garantia é entrega pelo menos uma vez, não execução exatamente uma vez.

Mensagens malformadas são publicadas em `ml.training.invalid` antes de confirmar sua remoção da fila original. Se a publicação falhar, não há ACK. Essa fila de quarentena requer inspeção manual; não existe interface de reprocessamento automático. Eventos atrasados não fazem o estado terminal do Core regredir.

## Execução e evidências

Na raiz: `docker compose up --build`. Acessar `http://localhost:8085`. Login de demonstração: `champam`, senha `af-demo-champam-2026`. O gateway é a única porta publicada, limitada ao localhost. O frontend AF é servido pelo Core através do gateway. PostgreSQL, broker, API ML e worker ficam na rede interna do Compose. O serviço `ml-init` cria o modelo somente quando ausente e termina antes de API ML e worker iniciarem.

As credenciais padrão são públicas e exclusivas da demonstração com dados sintéticos. Sobrescritas opcionais usam variáveis de ambiente. O Compose atual entrega RF02/RF05; `orientacao-af` e `evaluation-af` ainda não estão definidos, portanto recomendações, agente autorizado e avaliação RAG não estão disponíveis neste ambiente. Camargo deve integrar seu serviço e o modelo local ao mesmo Compose, sem comandos extras.

Validação local de 18/11/2026: Maven `verify`, 58 testes, 57 executados com sucesso e 1 PostgreSQL condicionado ao CI; cobertura 100% linhas/ramos. Python: 6 testes com sucesso. A execução Docker, PostgreSQL, interface e carga são validadas pelo GitHub Actions no commit correspondente; consultar o resultado do PR. Evidências anteriores a esta alteração não validam o gateway novo.

## Limitações

- Autenticação Basic para demonstração local, sem TLS, SSO ou gestão real de contas.
- ML baseado em dados sintéticos; não substitui avaliação humana.
- Modelo e metadados são substituídos em arquivos separados: pode haver transição de versão durante uma atualização. Não há rollout transacional ou múltiplas réplicas de worker.
- API espera até 2 segundos pela inferência. O prazo ponta a ponta depende de gateway, banco e carga; é medido no CI, não garantido para qualquer máquina.
- Não é declarada conclusão da AF inteira: Spring AI, RF03/RF04, revisão individual e vídeo seguem pendentes.
