# AF | Arquitetura e evolução da AC1

Gustavo Gutierres Champam - RA 223645
Gustavo Oliveira Camargo - RA 236024

Estudo de Caso 1 - DevOps e QA | Preparação em 16/11/2026

## a) Organização arquitetural

Escolhemos a Alternativa A, com Core modular em Spring Boot integrado a serviços especializados de IA. Alunos, conclusões, recompensas, ranking, catálogo de cursos e solicitações permanecem no Core. Python atende classificação, treinamento, orientação RAG e avaliação. A solução preserva a AC1 e permite atualizar os componentes de IA separadamente.

A equipe reduzida mantém um único deploy para as regras centrais, evitando transações distribuídas entre cadastro e recompensas. Os módulos expõem serviços e contratos; o ranking possui porta e adaptador de persistência. A modularização é incremental: não afirmamos que todos os módulos existentes já seguem arquitetura hexagonal completa.

Separar inferência e treinamento permite dimensionar o atendimento sem executar o treinamento dentro da requisição. A orientação evolui por REST e o treinamento por mensagens. Isso reduz acoplamento de implantação, mas exige contratos estáveis, autenticação entre serviços e tratamento de indisponibilidade.

A Alternativa B aumentaria autonomia por domínio, mas também exigiria mais pipelines, monitoramento, gestão de versões e consistência distribuída. Não identificamos necessidade de separar cada cadastro agora. Extrairíamos um módulo somente após observar saturação ou necessidade real de evolução independente.

## Escopo da proposta e da demonstração

O PDF da AF solicita as respostas a-e e soma 2 pontos. A implementação na AC1 e a reunião em dupla complementam a preparação conforme orientação oral relatada pela equipe. O texto fornecido não define duração de vídeo nem afirma que a gravação substitui a prova.

Usamos modelo e embeddings locais, sem API paga. O protótipo utiliza contas didáticas, dados sintéticos e quatro documentos de exemplo. Para produção, seriam necessários identidade corporativa, documentos reais autorizados, TLS, auditoria, backups e testes de capacidade no ambiente contratado.

# b) C4 nível 2 - contêineres

[Diagrama C4 navegável](C4.md) | [Relatório diagramado em PDF](AF_Entrega_e_Roteiro.pdf)

Limites reais de implantação: Core, API ML, worker, PostgreSQL e RabbitMQ em contêineres Docker; orientação, avaliação e servidor de modelo como processos locais. A interface AF é servida pelo Core. Na CI, o teste integrado usa Docker; o modelo foi executado no Windows.

1: HTTP/REST com autenticação. 2: SQL/JDBC. 3: REST de recomendação e agente com token de serviço. 4: REST de classificação. 5-6: AMQP bidirecional; Core publica pedidos, worker publica estados. 7: gravação de modelo e metadados. 8: leitura do modelo. 9: REST para iniciar/consultar avaliação. 10-11: API local compatível com chat/completions.

Os volumes persistem dados após reinício dos processos. A recuperação RAG usa TF-IDF em memória, com documentos versionados no serviço; não implementamos pgvector nem Spring AI nesta adaptação. A escolha mantém o laboratório sem cobrança e deixa explícita a diferença para a referência V5.3.2.

# c) Comunicação e tratamento de falhas

REST atende cadastros, catálogo, classificação imediata, recomendação e consultas de status. O Core consulta os cursos concluídos do aluno antes de enviar as características ao ML. A classificação tem timeout de leitura de 2 segundos; a geração local possui orçamento separado de até 120 segundos. Timeout não substitui teste de desempenho.

Treinamento usa RabbitMQ porque é demorado e não exige resposta final imediata. O Core grava a solicitação em tabela persistente e devolve HTTP 202. A mesma linha representa o job e a outbox; o dispatcher publica depois. Portanto, API ML, worker ou broker indisponível não impedem a aceitação enquanto o banco estiver disponível.

A publicação utiliza mensagem persistente, fila durável, confirmação e roteamento obrigatório. Sem confirmação, o registro continua pendente. O worker confirma consumo depois de salvar o resultado e publicar o estado. Na reentrega, reaproveita um resultado terminal já salvo. Se houver falha antes desse checkpoint, o treinamento pode ser repetido; não prometemos execução exatamente uma vez.

O consumidor do Core atualiza o andamento e impede que eventos atrasados revertam um estado terminal. A interface consulta received, queued, running, completed ou failed. Nesta versão, apenas a equipe solicita e acompanha treinamentos, pois são operações administrativas sobre o modelo compartilhado.

Quando a IA falha, a API responde indisponibilidade e os cadastros permanecem independentes. Ainda seriam necessários circuit breaker, fila de mensagens inválidas, retentativas com limite e monitoramento operacional antes de produção. Essas melhorias não são apresentadas como funcionalidades já implementadas.

## Diferença para o laboratório fornecido

Na referência V5.3.2, a API Python recebe a solicitação de treinamento e publica na fila. Isso cria dependência da disponibilidade do serviço ML para aceitar o pedido. Transferimos a aceitação durável para o Core, atendendo diretamente ao cenário de falha do RNF02.

Na demonstração de autorização, aluno1 não pode consultar aluno2 e o agente recusa execução sem consentimento. A ferramenta permitida é busca documental somente leitura; o agente coordena etapas fixas, sem escolher livremente ferramentas nem realizar matrícula ou enviar mensagens.

# d) Três requisitos significativos - ASRs

## RNF01 - classificação em até 2 segundos para 95% das consultas, com 300 usuários simultâneos

Esse requisito separa inferência de treinamento, favorece modelo carregado e limita chamadas remotas. Medimos latência ponta a ponta da classificação com autenticação e banco. O ensaio final registra três rajadas iniciais e mede 60 segundos de carga contínua com 300 usuários, após 30 segundos fixos de aquecimento. Usa dois alunos e entradas variadas. As rajadas iniciais permanecem no relatório. O resultado vale para o ambiente e protocolo medidos, sem garantir a mesma capacidade em outra infraestrutura ou em concorrência com RAG. Escala adicional deve ser guiada pelos resultados.

## RNF02 - aceitar treinamento com ML indisponível

Determina persistência da solicitação no Core, outbox e fila durável. HTTP 202 significa aceitação, não conclusão. O teste interrompe API ML e worker, aceita o pedido e verifica conclusão após retomada. Também interrompe RabbitMQ e comprova que o registro pendente é publicado depois da recuperação.

## RNF03 - proteger dados e limitar agentes

Determina autenticação, escopo por usuário e consentimento. O protótipo possui contas locais de equipe e alunos, acesso restrito ao próprio aluno e token entre Core e orientação/avaliação. Produção exige OIDC, TLS, segregação por organização e auditoria. O RAG recebe apenas pergunta, perfil e documentos didáticos; o agente não possui ferramenta de escrita.

# e) ADR-001 - Core modular e IA separada

Contexto: equipe pequena, AC1 existente, necessidade de classificação imediata, orientação com RAG e treinamento tolerante à indisponibilidade do ML.

Decisão: manter negócios em um Core Spring Boot e implantar componentes Python de IA separadamente. Usar REST para respostas imediatas e consultas, e RabbitMQ com aceitação persistente no Core para treinamento.

Justificativa: preserva transações e regras já verificadas da AC1, reduz decomposição desnecessária e permite atualizar modelo, recuperação e avaliação sem republicar todas as regras de negócio.

Consequência: menor complexidade que microsserviços por domínio, mas continuam existindo falhas de rede, contratos distribuídos e operação do broker. O Core mantém um limite de escala compartilhado; uma extração futura depende de evidências. Status: adotada no protótipo AF.

# Evidências e limites da implementação

Carga: 70179 consultas, 300 usuários simultâneos, p95 de 0.354 s e 0 erros. Critério em regime aquecido: atendido. Foram 60 segundos medidos após 30 segundos de aquecimento. As três rajadas iniciais também passaram: p95 de 0,990 s, 0,698 s e 0,603 s, sem erros. O resultado não deve ser extrapolado para outra infraestrutura.

Integração Docker: PostgreSQL, Core, RabbitMQ, API ML e worker foram exercitados no GitHub Actions. O teste comprova promoção da AC1, autorização, classificação e aceitação/retomada de treinamento com ML e broker interrompidos. O catálogo AF possui teste de persistência, validação de entrada e rejeição de código duplicado.

ML: regressão logística com 1.500 registros sintéticos, separação de treino, validação e teste e métricas em ml-training.json. Os resultados avaliam o conjunto sintético; não validam competência de colaboradores reais. A inferência otimizada foi comparada ao pipeline realmente treinado.

RAG: recuperação TF-IDF seguida de resposta real do Qwen3-4B local, com citação DOC-01 para Java/REST. RAGAS local: faithfulness = 1,000 e answer_relevancy = 0,862 em uma amostra. Não foram calculadas context_precision e context_recall nessa execução, pois não foi fornecida resposta de referência. Uma amostra e um juiz local não garantem qualidade geral.

Testes Java: 56 testes aprovados na CI, sem ignorados, com H2 e PostgreSQL. Gate de 100% de linhas e ramificações verificado pelo JaCoCo, sem relaxar os limites. Essa cobertura não equivale a 100% de qualidade nem cobre todos os serviços Python. Há testes adicionais de recuperação, consentimento, entradas inválidas e indisponibilidade da IA.

## Reprodução e rastreabilidade

Repositório: github.com/Gustavo-Champam/educacao-continuada-gamificada, branch af/evolucao-ia-local. O guia EXECUCAO.md contém os comandos; STATUS.md informa commits, execuções e pendências. Evidências ficam em documentacao/af/evidencias. Senhas, modelos, executáveis e dados de runtime ficam fora do Git.

O Docker foi validado no runner Ubuntu da CI. A IA generativa foi executada no Windows com GPU local. Não apresentamos esses ensaios como uma medição única de todos os componentes em produção. A reunião deve mostrar os resultados reais e mencionar essa distinção.

# Roteiro da reunião - Champam e Camargo

Sugestão de 6 a 8 minutos; não é uma duração estabelecida no PDF. Usem como apoio e adaptem às próprias palavras. Gravem os dois participantes e compartilhem a tela, sem mostrar senhas ou arquivos .env.

## Abertura | Champam

Eu sou o Gustavo Champam, RA 223645. Vamos apresentar a evolução da nossa AC1 para o estudo de caso da AF e explicar as decisões e os testes.

## Problema | Camargo

Eu sou o Gustavo Camargo, RA 236024. A plataforma precisa cadastrar alunos e cursos, classificar competências e recomendar trilhas. Como a equipe é pequena, comparamos um Core modular com a decomposição completa em microsserviços.

## Decisão | Champam

Mantivemos as regras da AC1 no Core Java e separamos a IA em Python. Aqui no C4 vemos REST para classificação e orientação, e RabbitMQ para treinamento. Assim, o treinamento não bloqueia a resposta ao usuário.

## Demonstração | Camargo

Vamos cadastrar e consultar um curso e um aluno. A classificação usa o histórico real de conclusões da AC1, mas o modelo foi treinado com dados sintéticos. Isso serve para o laboratório, não para avaliar pessoas em produção.

## RAG e consentimento | Champam

Nesta consulta, a resposta foi gerada localmente e apresenta suas fontes. Antes de executar o agente, precisamos autorizar a busca. O fluxo só consulta documentos e não altera cadastros.

## Falhas e evidências | Camargo

Na execução do GitHub Actions, paramos o ML e depois o broker. O Core continuou aceitando pedidos e concluiu após a retomada. Vamos abrir integracao.json e carga-final.json e ler os resultados exibidos, incluindo o ambiente do teste.

## Qualidade | Champam

Também rodamos o RAGAS local. A amostra teve fidelidade 1,00 e relevância aproximada de 0,86. Esses valores não garantem todas as respostas. Precisamos ampliar o conjunto de avaliação com documentos e perguntas reais autorizados.

## Conclusão | Camargo

A decisão prioriza baixo custo e evolução independente da IA. Para produção, ainda precisamos de identidade corporativa, TLS, auditoria e ensaios sustentados. Nossa entrega distingue a proposta, o que implementamos e o que realmente testamos.
