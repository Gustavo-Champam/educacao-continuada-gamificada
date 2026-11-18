# EducaTrilha AI - Roteiro AF v3 de 20 minutos

Gustavo Gutierres Champam - RA 223645
Gustavo Oliveira Camargo - RA 236024

VERSÃO DE PREPARAÇÃO. As falas demonstrativas abaixo destinam-se à versão v3 implementada e validada. Ainda não gravar como entrega final: faltam adequar Spring AI, gateway, execução integral pelo Compose padrão e comprovar contribuições individuais por PR. A versão anterior funciona em seus cenários testados, mas não atende integralmente à nova orientação.

## O que a professora pediu

1. Extensão da AC1 com requisitos inéditos em relação à AC1/AC2, usando Spring Boot, Spring AI e FastAPI. Dois requisitos por integrante.
2. Frontend e backend funcionando em Docker com o comando exato: `docker compose up --build`.
3. Cada integrante deve mostrar sua contribuição na documentação de arquitetura e seu código, conforme seus requisitos.
4. Cada integrante deve registrar contribuição por branch e PR; o tech lead aprova o merge para main. Aprovação deve ser real e feita por outro integrante, não pelo autor do PR.
5. Vídeo de 20 minutos no YouTube, como NÃO LISTADO. Entregar o LINK. Outros formatos não são aceitos pela orientação recebida.
6. Os dois mantêm a câmera aberta durante toda a gravação. A orientação informa nota zero para quem fechar a câmera.
7. Entregar o link do GitHub com fontes e commits. O README deve conter a documentação C4; ela será apresentada diretamente pelo README.
8. Seguir a sequência a-i: equipe; problema/requisitos; C4; serviços/módulos; microsserviços/gateway; hexagonal ou clean; comunicações; limitações; considerações finais.

O PDF v3 atribui 6 pontos à organização arquitetural no código, 1 ao C4, 2 à comunicação, 0,5 aos ASRs e 0,5 ao ADR. A implementação e a coerência da arquitetura são centrais na avaliação.

Os links obrigatórios descritos são YouTube e GitHub. Relatório PDF e roteiro são materiais de apoio; a mensagem recebida não os lista como entregas obrigatórias separadas. Não enviar o roteiro como se fosse o relatório técnico.

## Divisão dos integrantes

- Champam: tech lead principal; RF02 (classificação ML) e RF05 (treinamento e acompanhamento).
- Camargo: desenvolvimento de IA e revisão técnica; RF03 (RAG com Spring AI) e RF04 (agente autorizado).
- Champam revisa os PRs de Camargo; Camargo atua como revisor técnico substituto nos PRs de Champam. Se a professora exigir um único tech lead para todas as aprovações, alinhar o tratamento do PR do próprio tech lead. Não fabricar aprovações ou autoria.
- RF01 é base de cadastro e não conta como um dos quatro requisitos inéditos da dupla.

## Preparação das telas

Abrir o README no GitHub, a aplicação, o editor, a lista de PRs, os testes da versão v3 e um terminal na raiz do projeto. Deixar fontes legíveis e câmeras dos dois fixas na gravação. Entrar no sistema antes de gravar, sem mostrar senhas.

Executar um ensaio completo com cronômetro. A demonstração Docker deve usar somente `docker compose up --build` para subir a aplicação; não depender de scripts Python, variáveis manuais ou outro terminal para iniciar componentes. Primeiro download de imagens/modelos pode demorar: preparar e testar antes, sem esconder dependências externas obrigatórias. No vídeo, mostrar o comando real e os serviços iniciando.

As durações abaixo somam exatamente 20 minutos, incluindo cliques, demonstrações e transições. As falas não ocupam todo o tempo: o restante é para mostrar o comportamento e explicar o código. Não preencher o vídeo com espera de downloads.

---

# a) Equipe, projeto e data | 00:00-01:00

MOSTRAR: capa do README com nome do projeto, nomes completos, RAs e data real da gravação. Os dois aparecem de câmera aberta.

CHAMPAM:
“Olá, professora. Eu sou Gustavo Gutierres Champam, RA 223645. Nosso projeto é o EducaTrilha AI, uma evolução da aplicação de Educação Continuada Gamificada. Hoje, [DATA REAL DA GRAVAÇÃO], vamos apresentar a implementação da AF e revisar suas decisões de arquitetura.”

CAMARGO:
“Eu sou Gustavo Oliveira Camargo, RA 236024. Vamos seguir a sequência solicitada: problema e requisitos, arquitetura C4, serviços, gateway, organização interna, comunicações, limitações e considerações finais. Cada um apresentará seus dois requisitos e suas contribuições no projeto.”

# b) Problema e requisitos | 01:00-03:00

MOSTRAR: seção de problema e tabela de requisitos/responsáveis no README. Apontar o que veio da AC1 e o que foi acrescentado para a AF.

CHAMPAM:
“O problema é apoiar a formação de colaboradores com classificação de competências, recomendações de cursos e acompanhamento da aprendizagem. A AC1 já possuía regras de cadastro, conclusão, promoção e recompensas. Para a AF, precisamos acrescentar funcionalidades de inteligência artificial e treinamento sem comprometer essa base.”

CHAMPAM:
“Sou responsável pelo RF02, que classifica o nível de competência por Machine Learning, e pelo RF05, que permite solicitar treinamento e acompanhar seu andamento. Vou mostrar os contratos, o processamento e os testes dessas duas funcionalidades.”

CAMARGO:
“Sou responsável pelo RF03, que recomenda cursos utilizando documentos recuperados por RAG, e pelo RF04, que coordena atividades de orientação com autorização do usuário. Vou mostrar a integração com Spring AI, as fontes utilizadas e o controle das ferramentas do agente.”

CAMARGO:
“Além das funcionalidades, consideramos três requisitos arquiteturalmente significativos: responder à classificação com baixa latência, aceitar treinamento quando o ML estiver indisponível e controlar o acesso aos dados e às ferramentas. Também precisamos permitir evolução independente da IA com uma operação compatível com uma equipe pequena.”

AÇÕES: apontar os quatro requisitos, mostrar os critérios de aceite e a comparação com a base AC1/AC2. Não contar cadastro herdado como requisito novo.

---

# c) Arquitetura C4 diretamente no README | 03:00-06:00

MOSTRAR: diagramas renderizados no README, não somente o PDF ou o código Mermaid. Preparar contexto, contêineres e a visão dos componentes/portas relevantes. O nível 2 é expressamente solicitado pelo PDF v3.

CHAMPAM:
“Na visão de contexto, o colaborador utiliza a plataforma para acompanhar sua formação, e a equipe administra os dados e os treinamentos. Na visão de contêineres, identificamos frontend, gateway, Core Spring Boot, serviços de IA, banco, RabbitMQ e processamento de treinamento.”

CHAMPAM:
“Minha contribuição na arquitetura está no fluxo de classificação e treinamento. A classificação exige resposta imediata. Já o treinamento é aceito de forma persistente e encaminhado para processamento assíncrono. Isso evita que a disponibilidade do serviço de ML determine se o pedido pode ser recebido.”

CAMARGO:
“Minha contribuição está no fluxo de orientação, na integração Spring AI e nos limites de acesso do agente. O serviço recupera informações relevantes, utiliza o modelo para gerar a orientação e devolve fontes para conferência. As ferramentas disponíveis ao agente precisam respeitar autorização e escopo.”

CAMARGO:
“As caixas identificam processos ou unidades de implantação. As setas mostram protocolos e responsabilidades. As fronteiras deixam claro o que pertence ao Core, o que é serviço especializado e onde os dados são persistidos.”

CHAMPAM:
“A decisão principal é manter as regras centrais organizadas em módulos e separar os componentes que precisam de evolução independente. O ADR registra o contexto, essa decisão, a justificativa e o custo de administrar comunicação entre serviços.”

AÇÕES: Champam percorre usuário → gateway → Core → ML e Core → fila → worker. Camargo percorre orientação → recuperação → modelo → resposta e aponta os limites do agente. Mostrar brevemente três ASRs e o ADR no README. Cada um deve explicar uma decisão da qual participou, sustentada por seu PR.

PENDENTE PARA GRAVAR: README v3 completo e diagramas coerentes com os serviços realmente executados. Não apresentar gateway ou Spring AI no desenho se não existirem no código e na execução.

---

# d) Serviços e módulos implementados | 06:00-12:00

Este bloco tem quatro demonstrações de 1 minuto e 30 segundos. Em cada uma: aproximadamente 25 segundos de explicação, 35 de código/contrato, 20 de comportamento e 10 de commit/PR. Preparar as abas antes.

## 06:00-07:30 | Champam: RF02 - classificação ML

MOSTRAR: interface de classificação; Core chamando FastAPI; `OrientacaoController.java`, `ml/app.py` e `ml/training.py`; teste e PR de Champam.

CHAMPAM:
“No RF02, o Core consulta o histórico do aluno e envia as características para a API de classificação. A FastAPI valida os dados e executa o modelo treinado. Aqui está o contrato de entrada, e aqui está o ponto em que a predição é calculada.”

CHAMPAM:
“Vou executar uma classificação e mostrar o perfil retornado. O modelo foi treinado com dados sintéticos, separados em treino, validação e teste. A inferência é real, mas essa base não permite afirmar que já avaliamos corretamente colaboradores reais.”

AÇÕES: consultar aluno existente; preencher valores válidos; clicar em classificar; ler o perfil efetivamente retornado. Mostrar o teste relevante e seu PR. Não fixar um resultado antecipadamente: o histórico e o modelo podem mudar a classificação.

## 07:30-09:00 | Champam: RF05 - treinamento e status

MOSTRAR: `Treinamentos.java`, `ml/worker.py`, solicitação na interface e consulta do job; evidência de retomada; PR de Champam.

CHAMPAM:
“No RF05, a solicitação é salva antes de ser publicada. A API retorna a aceitação e um identificador para consulta. O worker recebe o pedido, executa o treinamento e informa o resultado. O usuário acompanha os estados pela interface.”

CHAMPAM:
“Aqui vemos o registro persistente e a publicação. No worker, vemos consumo e confirmação. Este teste verifica que o Core aceita o pedido mesmo com o ML interrompido e que o processamento conclui após a retomada.”

AÇÕES: iniciar um job, mostrar seu ID e atualizar andamento. Caso não conclua dentro desse intervalo, continuar a apresentação e usar uma execução anterior da mesma versão, explicitamente identificada, para mostrar a conclusão. A evidência de interrupção deve corresponder à stack v3 validada.

---

## 09:00-10:30 | Camargo: RF03 - RAG com Spring AI

MOSTRAR APÓS IMPLEMENTAÇÃO: dependência Spring AI no serviço; chamada real ao ChatClient/ChatModel; recuperação dos documentos; interface com recomendação e fontes; teste e PR de Camargo.

CAMARGO:
“No RF03, a recomendação utiliza RAG. Primeiro recuperamos trechos relevantes dos documentos; depois a integração Spring AI fornece esse contexto ao modelo. A resposta inclui as fontes usadas, para que o usuário possa conferir a origem da orientação.”

CAMARGO:
“Aqui mostro a dependência e a chamada real do Spring AI. Neste trecho está a recuperação, e neste outro a construção do contexto. Agora vou solicitar uma trilha de Java e APIs REST e conferir a resposta com as fontes.”

AÇÕES: usar pergunta curta, por exemplo “Quero aprender Java e APIs REST. Qual trilha devo seguir?”. Apontar a fonte retornada. Mostrar o arquivo efetivamente desenvolvido e o PR real de Camargo. Não apresentar `orientacao/app.py` da versão anterior como implementação Spring AI: ele é Python e não comprova esse requisito.

## 10:30-12:00 | Camargo: RF04 - agente autorizado

MOSTRAR APÓS ADEQUAÇÃO: código do agente, validação de consentimento, ferramentas permitidas e uso do contexto de acompanhamento; duas execuções na interface e PR de Camargo.

CAMARGO:
“No RF04, o agente coordena a orientação dentro de um escopo permitido. A autenticação identifica o usuário, e o consentimento autoriza a atividade. Aqui está a validação que impede a execução sem autorização, e aqui estão as ferramentas disponíveis.”

CAMARGO:
“Primeiro executo sem consentimento e mostro a recusa. Depois autorizo a consulta e mostro o fluxo permitido. Vou apontar quais informações de acompanhamento são consultadas e quais ações o agente não pode realizar.”

AÇÕES: mostrar recusa, marcar consentimento e executar novamente. Explicar os passos reais e a relação com progresso/aprendizagem. Se a implementação for um fluxo controlado e somente leitura, dizer isso; não afirmar autonomia ou ferramentas inexistentes.

ATENÇÃO DE AUTORIA: Camargo precisa desenvolver/revisar e registrar sua contribuição real. Os commits antigos sob autoria de Champam não são prova de código desenvolvido por Camargo. Todos devem mostrar seu código e seu trabalho de arquitetura, não apenas ler falas.

---

# e) Microsserviços e gateway obrigatório | 12:00-14:00

MOSTRAR APÓS ADEQUAÇÃO: `compose.yaml`, serviço de gateway e rotas reais; terminal; aplicação acessível pelo ponto de entrada correto.

CHAMPAM:
“O gateway é o ponto de entrada das chamadas e encaminha cada rota ao serviço responsável. Aqui estão as rotas efetivamente configuradas. A interface usa esse endereço de entrada, e os serviços internos continuam com responsabilidades próprias.”

CAMARGO:
“A existência de vários contêineres, sozinha, não caracteriza uma boa arquitetura de microsserviços. Precisamos de limites claros, contratos e possibilidade de evolução independente. Vamos apontar quais partes são serviços separados e quais continuam como módulos dentro do Core.”

CHAMPAM:
“Para executar o projeto, usamos o comando solicitado pela professora: docker compose up --build. Ele deve subir frontend, backend, gateway, persistência, mensageria e os componentes necessários da IA, sem exigir processos iniciados manualmente fora do Compose.”

AÇÕES: mostrar o comando exato sendo executado e os serviços iniciando; acessar o frontend pelo gateway e fazer uma consulta. Se houver downloads demorados, prepará-los no ensaio; não fingir que um serviço já aberto fora do Docker foi iniciado pelo comando. Mostrar na configuração onde cada rota aponta.

PENDENTE: o Compose anterior com `--env-file`, `-f compose.af.yaml` e launcher no host não atende a essa exigência. Este bloco só pode ser gravado após a correção e validação.

# f) Arquitetura hexagonal ou clean | 14:00-16:00

MOSTRAR: editor com domínio, caso de uso, porta e adaptador reais de um fluxo AF. Preferir um requisito apresentado pelos integrantes; não usar apenas um diagrama genérico ou nomes de pastas.

CAMARGO:
“Na organização interna, separamos as regras e os casos de uso dos detalhes de tecnologia. A porta define o contrato necessário à aplicação; o adaptador implementa a comunicação com o recurso externo.”

CHAMPAM:
“Neste fluxo, vamos seguir a chamada da entrada até o caso de uso e o adaptador. O controller recebe a requisição, o caso de uso coordena a regra e a porta permite substituir a integração sem espalhar detalhes de HTTP ou mensageria pelo domínio.”

CAMARGO:
“O teste deste caso de uso mostra como verificamos o comportamento usando o contrato. A organização em camadas só é demonstrada quando a direção das dependências e as responsabilidades realmente seguem essa separação.”

AÇÕES: abrir uma interface de porta e sua implementação, apontar quem depende de quem e mostrar um teste do caso de uso. Não afirmar que todo o Core já é hexagonal: a modularização anterior era incremental. O exemplo AF precisa estar implementado e consistente com a explicação.

---

# g) Comunicação síncrona e assíncrona | 16:00-18:00

MOSTRAR: setas do C4 no README, endpoint REST de classificação, publicação/consumo AMQP e testes.

CHAMPAM:
“A classificação usa REST porque o usuário precisa do resultado durante a interação. O Core aguarda a resposta dentro de um tempo limite. Quando o serviço falha, devemos responder de forma controlada, sem inventar uma classificação.”

CAMARGO:
“O treinamento usa comunicação assíncrona porque pode demorar e não precisa concluir dentro da requisição inicial. A confirmação HTTP 202 informa aceitação, enquanto a conclusão é acompanhada pelo estado do job.”

CHAMPAM:
“A persistência do pedido antes da publicação permite aceitar solicitações com o broker ou o ML temporariamente indisponíveis. Mensagens podem ser reentregues, então precisamos tratar repetição e estados terminais. Não prometemos processamento exatamente uma vez.”

CAMARGO:
“Mostramos também os testes de integração e desempenho. A meta da classificação é responder a 95% das consultas em até dois segundos com 300 usuários. A evidência usada aqui deve identificar o commit, o ambiente, a quantidade de requisições, o p95 e os erros da versão que estamos apresentando.”

AÇÕES: mostrar a execução v3 aprovada e os resultados reais. A medição antiga de 70.179 consultas, p95 0,354 s e zero erros pertence à stack anterior; não atribuir esses números automaticamente ao novo gateway ou aos novos serviços. Substituir pela medição atual ou identificá-la explicitamente como histórica.

# h) Limitações | 18:00-19:00

MOSTRAR: seção “Limitações” do README, coerente com o código final.

CAMARGO:
“As limitações do protótipo incluem o uso de dados sintéticos no ML e documentos didáticos no RAG. Isso permite validar a integração, mas não substitui uma avaliação com dados reais representativos e autorizados. A qualidade das recomendações deve ser acompanhada com um conjunto maior de perguntas e referências.”

CHAMPAM:
“A execução local do modelo também depende dos recursos da máquina. Para produção, precisamos revisar identidade corporativa, TLS, auditoria, operação das filas e capacidade. Vamos distinguir essas evoluções de produção dos requisitos obrigatórios da AF, que precisam funcionar nesta entrega.”

Não classificar ausência de Spring AI, gateway, execução Docker ou contribuição individual como simples limitação aceitável: são pendências obrigatórias antes de gravar.

---

# i) Considerações finais | 19:00-20:00

MOSTRAR: README, tabela de responsabilidades e PRs realmente revisados e integrados à main.

CHAMPAM:
“Concluímos a apresentação relacionando requisitos, arquitetura e implementação. Apresentei classificação de competências e treinamento com acompanhamento, incluindo seus contratos, processamento e testes.”

CAMARGO:
“Apresentei recomendação RAG com Spring AI e o agente autorizado, incluindo a recuperação documental, os limites das ferramentas e as evidências da minha contribuição. A documentação registra as decisões, os ASRs, o ADR e os limites do projeto.”

CHAMPAM:
“Aqui estão os PRs e as revisões da equipe, com integração à main. O repositório contém as instruções para executar a aplicação com docker compose up --build e reproduzir os cenários apresentados.”

CAMARGO:
“Encerramos a revisão do EducaTrilha AI com as decisões justificadas e os resultados identificados. Obrigado.”

AÇÕES: conferir que os dois continuam de câmera aberta; encerrar com aproximadamente 20:00 no cronômetro, visando o tempo exigido. Essa fala de conclusão só pode ser usada quando os PRs, revisões, merge e funcionalidades estiverem efetivamente concluídos.

## Conferência final antes de enviar

- Vídeo com 20 minutos, ambos visíveis durante toda a gravação e sequência a-i respeitada.
- Cada integrante mostrou nome completo, RA, duas funcionalidades, código, contribuição na arquitetura e seus registros de branch/PR.
- Projeto com nome e data real da gravação; README com C4, três ASRs e ADR coerentes com o código.
- Spring Boot, Spring AI e FastAPI realmente executados; gateway demonstrado; frontend e backend disponíveis.
- Execução validada com o comando exato `docker compose up --build`, incluindo os componentes necessários à IA.
- PRs revisados e integrados à main conforme o fluxo da equipe. Não entregar somente uma branch incompleta como se fosse a main final.
- Vídeo publicado no YouTube como NÃO LISTADO. Abrir o link em janela sem login e conferir vídeo e áudio. Se o repositório for privado, assegurar que a professora tenha acesso.
- Enviar os dois links: vídeo do YouTube e repositório GitHub. Anexar documentos extras somente se o campo da atividade ou a professora pedir.

Modelo de mensagem após a conclusão real:

“Professora, segue a entrega da AF do projeto EducaTrilha AI - Educação Continuada Gamificada. Integrantes: Gustavo Gutierres Champam, RA 223645, e Gustavo Oliveira Camargo, RA 236024. Vídeo de 20 minutos, não listado no YouTube: [LINK REAL]. Repositório com fontes, documentação C4, commits e PRs integrados: [LINK REAL]. Comando de execução: docker compose up --build.”
