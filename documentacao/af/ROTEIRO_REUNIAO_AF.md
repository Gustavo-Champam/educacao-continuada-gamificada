# Reunião técnica AF - roteiro de gravação

Gustavo Gutierres Champam - RA 223645
Gustavo Oliveira Camargo - RA 236024

Formato sugerido: reunião de revisão da arquitetura e validação da evolução da AC1. Duração estimada: 10 a 12 minutos, mais eventuais esperas da demonstração. Essa duração é uma sugestão; os documentos fornecidos não estabelecem tempo obrigatório de vídeo.

## Preparação antes de gravar

- Champam compartilha a tela e conduz arquitetura e demonstração. Camargo conduz as perguntas, a análise de testes e a conclusão. Essa divisão é para a gravação, sem atribuir autoria individual de partes do código.
- Mantenham as câmeras dos dois visíveis, testem o áudio e fechem notificações. Aumentem o zoom do navegador para que os resultados sejam legíveis.
- Abrir a aplicação e preencher a senha antes de iniciar a gravação. Não abrir o arquivo .env.af, tokens, gerenciador de senhas ou terminal com credenciais.
- Ensaiar os cliques uma vez. Separar um código de curso ainda não cadastrado para a gravação, por exemplo JAVA-VIDEO-01. Usar dados fictícios.
- Preparar uma avaliação RAGAS antes de gravar e guardar seu ID. O roteiro mostra a consulta desse resultado, identificando-o como execução prévia. Não é necessário esperar um novo julgamento completo durante o vídeo.
- Se Docker não estiver funcionando localmente, usar a demonstração Core/H2 para cadastro, ML e RAG, e a execução real da CI para a fila. Não tentar simular que RabbitMQ está rodando no computador.
- Se o sistema não estiver iniciado, seguir documentacao/af/EXECUCAO.md no repositório. O endereço local só funciona com os serviços ativos.

## Abas que devem ficar prontas, nesta ordem

1. Repositório na branch af/evolucao-ia-local.
2. AF_Entrega_e_Roteiro.pdf: página 2, diagrama C4; página 4, ASRs e ADR.
3. Aplicação local: http://localhost:8085/af.html.
4. GitHub Actions: execução AF 43948164512 e execução AC1 43948164464.
5. Pasta documentacao/af/evidencias: integracao.json, carga-final.json e testes-java-ci.json.
6. Avaliação RAGAS: resultado consultável na interface ou ragas-interface.png junto de ragas-integrado.json.

Não precisam ler código linha por linha. A prioridade é conectar requisito, decisão, comportamento e evidência.

---

# 1. Abertura e objetivo | 0:00 a 0:50

TELA: repositório, com o nome da branch e o README visíveis.

CHAMPAM:
“Olá, professora. Eu sou o Gustavo Gutierres Champam, RA 223645. Nesta reunião, vamos revisar a evolução da nossa plataforma de educação continuada da AC1 para o estudo de caso da AF. Vamos apresentar a arquitetura, demonstrar as funcionalidades e conferir as evidências de qualidade.”

CAMARGO:
“Eu sou o Gustavo Oliveira Camargo, RA 236024. Vou conduzir a revisão dos requisitos e dos testes. A nossa pauta é verificar se as decisões atendem ao cenário, quais resultados foram comprovados e quais limitações permanecem no protótipo.”

## 2. Problema e decisão principal | 0:50 a 1:50

TELA: página 1 do relatório ou início do README. Em seguida, abrir o C4.

CAMARGO:
“O cenário pede cadastro de colaboradores e cursos, classificação de competências, recomendações com RAG, orientação autorizada por agentes e acompanhamento dos treinamentos. Ao mesmo tempo, temos uma equipe pequena. Por que escolhemos manter o Core modular?”

CHAMPAM:
“Porque a AC1 já concentra regras de negócio relacionadas, como conclusão de cursos, promoção e recompensas. Mantendo essas regras no Core Java, preservamos as transações e evitamos separar cada cadastro em um serviço. A inteligência artificial fica em componentes Python independentes, que podem evoluir sem exigir a publicação de todas as regras de negócio.”

CAMARGO:
“Então a escolha aproxima-se da Alternativa A: um Core modular integrado a serviços especializados de IA. Qual é o principal trade-off?”

CHAMPAM:
“Reduzimos a complexidade em comparação com microsserviços para cada domínio, mas ainda precisamos administrar contratos de API, falhas de rede e mensageria. Além disso, os módulos do Core compartilham a mesma implantação. Uma separação futura deve ser orientada por necessidade real de escala ou autonomia.”

O QUE COMPROVAR: decisão explícita, justificativa ligada ao tamanho da equipe e reconhecimento de uma consequência. Não dizer que todo o sistema é um único processo nem que todos os módulos já são totalmente hexagonais.

---

# 3. Percurso pelo C4 | 1:50 a 3:00

TELA: página 2 do PDF, ocupando a maior parte da tela. Apontar as caixas enquanto fala.

CHAMPAM:
“Aqui o usuário acessa a interface servida pelo Core Spring Boot. O Core mantém os dados de negócio no PostgreSQL. Para classificação, ele consulta a API de Machine Learning por REST. Para orientação, chama o serviço de RAG e agente. A geração utiliza o Qwen3 executado localmente pelo Lemonade.”

CHAMPAM:
“O treinamento segue outro caminho: o Core salva a solicitação, publica no RabbitMQ e um worker Python realiza o processamento. O worker publica o resultado, e o Core atualiza o andamento. A avaliação RAGAS também é um serviço separado.”

CAMARGO:
“Por que usamos REST em algumas interações e RabbitMQ no treinamento?”

CHAMPAM:
“REST atende operações em que precisamos de uma resposta imediata, como consultar dados e classificar. O treinamento pode levar mais tempo. Por isso, usamos uma solicitação assíncrona: a API confirma que aceitou o pedido e o usuário acompanha o estado depois. Isso também permite aceitar o pedido quando o ML está temporariamente indisponível.”

CAMARGO:
“E quais são os limites de implantação?”

CHAMPAM:
“Core, PostgreSQL, RabbitMQ, API ML e worker possuem contêineres no Compose. Orientação, avaliação e modelo local rodam como processos no host. A stack Docker foi validada no GitHub Actions. Nesta demonstração local usamos H2; vamos mostrar a evidência da CI para PostgreSQL e mensageria.”

AJUSTE DE FALA: a última frase descreve a demonstração Windows já validada. Se vocês estiverem efetivamente usando a stack Docker local, substituam por: “Nesta demonstração também estamos usando a stack Docker com PostgreSQL e RabbitMQ.” Só façam essa substituição se for verdade.

O QUE COMPROVAR: apontar Core, banco, API ML, fila, worker, orientação e modelo local. Não afirmar que o RAG implementado usa Spring AI ou pgvector: ele usa TF-IDF em Python.

---

# 4. Cadastro, regras da AC1 e classificação | 3:00 a 4:30

TELA: aplicação em /af.html. Conta de equipe já preenchida, sem expor a senha.

AÇÕES DE CHAMPAM:

1. Em “Catálogo de cursos”, preencher código inédito, nome “Java e APIs REST” e uma descrição curta. Clicar em “Cadastrar curso” e depois “Consultar catálogo”.
2. Em “Acesso e aluno”, cadastrar “Aluno Demonstração AF”. O campo de ID será atualizado. Mostrar o ID criado.
3. Registrar uma conclusão usando o código do curso e média 8. Mostrar o retorno. Uma conclusão não gera promoção Premium.
4. Em classificação, usar experiência 12 meses, avaliação 80, estudo 6 horas, REST 70 e banco de dados 80. Clicar em “Classificar perfil”. Ler o perfil que realmente aparecer, sem prometer um resultado específico.

CHAMPAM:
“Primeiro vamos cadastrar um curso e um aluno fictício. O catálogo é persistente, e a API rejeita códigos duplicados. Agora registramos uma conclusão válida. As regras da AC1 foram preservadas: a promoção acontece após 12 cursos válidos, com um voucher e três moedas. Uma única conclusão, como esta, ainda não atende ao critério.”

CAMARGO:
“O total de cursos usado na classificação é digitado na tela?”

CHAMPAM:
“Não. O Core consulta o histórico do aluno na AC1. Os demais dados representam a avaliação de competências. A API Python retorna o perfil e as probabilidades do modelo, que podemos observar aqui.”

CAMARGO:
“Qual modelo foi usado e qual é o limite dessa classificação?”

CHAMPAM:
“Usamos regressão logística, treinada com 1.500 registros sintéticos, separados em treino, validação e teste. A inferência é real, mas os dados são didáticos. Antes de avaliar colaboradores reais, precisaríamos validar o modelo com dados representativos e autorizados.”

O QUE COMPROVAR: cadastro persistente, ID do aluno, conclusão e resposta ML. A promoção completa já está comprovada em integracao.json; não é preciso cadastrar 12 conclusões durante o vídeo. Não chamar a probabilidade retornada de garantia de acerto.

---

# 5. RAG e autorização do agente | 4:30 a 6:10

TELA: “Recomendação com fontes”. Para a demonstração documental, selecionar perfil “iniciante” e explicar essa seleção.

AÇÕES DE CHAMPAM:

1. Digitar: “Quero aprender Java e APIs REST. Qual trilha devo seguir?”
2. Clicar em “Consultar RAG”. Aguardar a resposta e mostrar o texto e as fontes. Apontar DOC-01 se estiver presente no resultado.
3. Com a autorização desmarcada, clicar em “Executar agente”. Mostrar a recusa HTTP 403.
4. Marcar “Autorizo a consulta documental pelo agente” e executar novamente. Mostrar a resposta e os passos do fluxo.

CAMARGO:
“Qual é a diferença entre essa recomendação e uma pergunta enviada diretamente a um modelo?”

CHAMPAM:
“Aqui recuperamos primeiro os trechos relevantes dos documentos por TF-IDF. Esses trechos são enviados ao modelo local para orientar a resposta, e as fontes são devolvidas para conferência. Para esse exemplo, selecionei o perfil iniciante e pedi uma trilha de Java e REST. Os documentos utilizados são exemplos didáticos, não documentos institucionais reais da FACENS.”

CAMARGO:
“Como controlamos o acesso do agente?”

CHAMPAM:
“Além da autenticação e das permissões da conta, exigimos consentimento para essa consulta. Sem autorização, a execução é recusada. Com autorização, o agente segue as etapas permitidas: buscar documentos e gerar a orientação. É um fluxo controlado e somente leitura; ele não altera cadastros nem realiza matrículas.”

CAMARGO:
“Então conseguimos demonstrar o uso autorizado da ferramenta, sem conceder ao modelo acesso irrestrito ao sistema.”

O QUE COMPROVAR: resposta com fontes, recusa sem consentimento e execução autorizada. A formulação exata da resposta pode variar. Se a geração demorar, explicar que o requisito de 2 segundos é da classificação, não do RAG. Não confundir consentimento com substituição da autenticação.

---

# 6. Treinamento e tolerância a falhas | 6:10 a 7:20

TELA: execução AF aprovada no GitHub Actions; depois abrir integracao.json no repositório.

AÇÕES DE CHAMPAM: mostrar o sucesso da etapa de integração. No JSON, apontar job_ml_offline, estado_em_fila, conclusao, job_broker_offline e conclusao_apos_retomada. Os nomes extensos dos IDs não precisam ser lidos.

CAMARGO:
“O requisito pede que o sistema continue aceitando treinamento com o ML indisponível. Como comprovamos isso?”

CHAMPAM:
“O teste interrompeu a API ML e o worker, enviou a solicitação e verificou a aceitação. O pedido ficou em fila e concluiu depois da retomada. Também interrompemos o RabbitMQ: nesse caso, o registro permaneceu recebido no banco e foi publicado após a recuperação.”

CAMARGO:
“Então a confirmação de aceitação não depende de o treinamento estar concluído.”

CHAMPAM:
“Exatamente. O Core persiste o job antes de publicar e retorna HTTP 202. A mesma linha atua como outbox. Usamos fila durável, mensagem persistente, confirmação de publicação e ACK do consumidor. O resultado final é registrado e pode ser consultado pela equipe.”

CAMARGO:
“Esses dados são de uma execução real da CI. Não estamos apresentando a fila como se estivesse sendo executada nesta demonstração H2.”

OPCIONAL COM DOCKER LOCAL: mostrar “Solicitar treinamento” e atualizar o andamento até completed. Isso complementa a evidência de falha, mas uma solicitação normal não substitui o teste de interrupção. Sem Docker, não acionar esse botão durante a gravação: o job pode permanecer pendente.

## 7. Testes e desempenho | 7:20 a 8:40

TELA: testes-java-ci.json e carga-final.json. Deixar os valores ampliados.

CAMARGO:
“Na CI, os 56 testes Java passaram, incluindo H2 e PostgreSQL, sem testes ignorados. O JaCoCo registrou 100% de cobertura de linhas e ramificações. Também temos testes Python e validação da interface em navegador real. A cobertura mostra execução do código nos cenários testados; não significa ausência de qualquer defeito.”

CHAMPAM:
“E o requisito de responder a 95% das classificações em até dois segundos, com 300 usuários?”

CAMARGO:
“No ensaio final, usamos 300 usuários simultâneos, dois alunos e entradas variadas. Depois de 30 segundos de aquecimento, medimos 60 segundos de carga contínua. Foram 70.179 classificações, p95 de 0,354 segundo e zero erros. Isso significa que pelo menos 95% das respostas ficaram nesse tempo ou abaixo dele. As três rajadas iniciais também ficaram abaixo de dois segundos.”

CAMARGO:
“A meta foi atendida no ambiente medido: Docker no runner do GitHub Actions. O histórico das tentativas foi preservado. Isso não garante o mesmo resultado em qualquer infraestrutura ou com outras cargas concorrentes.”

---

# 8. Avaliação RAGAS | 8:40 a 9:35

TELA: “Avaliação RAGAS local”, com o ID de uma avaliação previamente concluída. Clicar em “Atualizar métricas”. Se o registro não existir neste ambiente, abrir ragas-interface.png e ragas-integrado.json e identificar claramente que são evidências de uma execução anterior.

CHAMPAM:
“Além de testar a API, avaliamos uma resposta RAG com o RAGAS usando modelo e embeddings locais. Esta avaliação foi executada previamente; agora estamos consultando seu resultado.”

CAMARGO:
“Na amostra registrada, a fidelidade foi 1,00 e a relevância da resposta foi aproximadamente 0,862. A fidelidade estima a sustentação da resposta no contexto recuperado. A relevância estima sua relação com a pergunta. Não devemos interpretar 0,862 como uma taxa universal de acerto de 86,2%.”

CHAMPAM:
“Como não fornecemos resposta de referência nessa execução, não calculamos as métricas de precisão e recuperação de contexto. Também não generalizamos uma amostra para todas as respostas. O próximo passo seria ampliar a avaliação com perguntas e documentos reais autorizados.”

## 9. ADR, encaminhamentos e encerramento | 9:35 a 10:40

TELA: página 4 do relatório, ADR-001. Ao final, voltar ao repositório na branch AF.

CAMARGO:
“Para concluir a revisão, os três requisitos que mais influenciaram a arquitetura foram desempenho, continuidade da aceitação de treinamento e controle de acesso. Eles orientaram a separação da inferência, a outbox com mensageria e as permissões do agente.”

CHAMPAM:
“O ADR registra nossa decisão de manter o Core modular e separar os componentes de IA, usando REST para as interações imediatas e RabbitMQ para treinamento. Essa organização preserva a AC1 e equilibra evolução independente com a capacidade operacional de uma equipe pequena.”

CAMARGO:
“Com base no que foi demonstrado, mantemos essa decisão para o protótipo. Para uma implantação de produção, registramos como próximos passos identidade corporativa, TLS, auditoria, tratamento operacional de mensagens com falha e validação do modelo com dados reais.”

CHAMPAM:
“O código, o relatório, o C4, o ADR e as evidências estão publicados nesta branch. Encerramos a revisão com os cenários testados documentados e com as limitações e os próximos passos identificados. Obrigado.”

O QUE COMPROVAR: terminar com uma decisão e encaminhamentos, como em uma reunião técnica. Não anunciar aprovação da professora, nota garantida ou prontidão para produção.

---

# Apoio para ensaio e imprevistos

## Se algum resultado não aparecer ao vivo

Dizer: “Neste momento a demonstração local não respondeu como esperado. Vamos mostrar a evidência da execução validada e registrar essa diferença.” Abrir a captura e o JSON correspondentes. Não narrar uma captura como se fosse uma operação acabada de executar.

Se um curso retornar conflito, o código já existe: consultar o catálogo ou usar um novo código. Se o agente retornar 403 com consentimento desmarcado, esse é o comportamento esperado. Se a classificação falhar por modelo ausente, preparar o modelo antes de gravar. Não tentar resolver instalação, credenciais ou dependências durante a apresentação.

## Respostas curtas para perguntas prováveis

“Por que não microsserviços em todos os módulos?”
“Porque a equipe é pequena, as regras centrais compartilham transações e não há evidência de que separar cada domínio compense o custo operacional. A IA já possui limites de implantação próprios.”

“O que é outbox neste projeto?”
“É o registro durável que permite publicar o pedido depois. Aqui a própria linha do job cumpre esse papel, evitando depender do broker no momento da aceitação.”

“A mensagem será processada exatamente uma vez?”
“Não garantimos isso. Pode haver reentrega. O worker reaproveita resultados terminais já salvos, mas uma falha antes do checkpoint pode repetir o treinamento.”

“O sistema usa Spring AI ou pgvector?”
“Nesta implementação, não. Adaptamos o RAG para Python com TF-IDF e geração local. A diferença em relação ao laboratório de referência está documentada.”

“O agente é autônomo?”
“É um agente de fluxo controlado, com consulta documental autorizada e somente leitura. Não possui escolha livre de ferramentas nem permissão para alterar dados.”

“O p95 de 0,354 segundo vale para o RAG?”
“Não. A medição é da classificação ML. A geração RAG e a avaliação possuem tempos e recursos diferentes.”

“100% de cobertura garante que não há bugs?”
“Não. Significa cobertura das linhas e ramificações Java segundo os testes executados. Precisamos considerar também cenários, qualidade das asserções, integração, segurança e limitações dos dados.”

“A IA não tem custo?”
“A execução utilizada não exige API paga. Ainda existem custos de equipamento, energia, armazenamento e operação.”

## Links da gravação

- Projeto: https://github.com/Gustavo-Champam/educacao-continuada-gamificada/tree/af/evolucao-ia-local
- Integração, carga e interface AF: https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/43948164512
- Regressão AC1: https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/43948164464
- Pasta de evidências: https://github.com/Gustavo-Champam/educacao-continuada-gamificada/tree/af/evolucao-ia-local/documentacao/af/evidencias

Critério para o ensaio: cada integrante deve conseguir explicar suas falas sem depender de leitura literal. Usem o roteiro como guia, façam pausas para mostrar os resultados e adaptem a duração caso a professora tenha dado uma orientação diferente em aula.
