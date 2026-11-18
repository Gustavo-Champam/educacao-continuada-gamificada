# Guia clicável da apresentação AF v3

Ainda é um guia de estudo: a AF v3 não está concluída. Etapas pendentes não devem ser gravadas como prontas. Os links de código mostram uma revisão real do projeto; a aplicação local só abre com os serviços ativos.

Abra os links de cada etapa em outra aba. Leia “Entenda primeiro”, confira o código e pratique explicar sem decorar. O roteiro completo é um apoio; a professora exige a contribuição real de cada integrante.

## 1. a) Quem somos | 00:00–01:00
**Quem:** Os dois · **Situação:** Preparar

**Entenda primeiro:** É a identificação do trabalho. Cada um fala seu nome e RA; os dois ficam de câmera aberta o tempo todo.

- [Abrir nomes e divisão](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/af/v3-adequacao-entrega/documentacao/af/DIVISAO_AF_V3.md)
- [Abrir README](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/tree/af/v3-adequacao-entrega)

**O que fazer:**

1. Abra a divisão da equipe e a capa do README.
2. Diga a data em que vocês estiverem realmente gravando.

**Fala / explicação para ensaiar:**

> Champam: “Eu sou Gustavo Gutierres Champam, RA 223645. Nosso projeto é o EducaTrilha AI, evolução da Educação Continuada Gamificada.”
> Camargo: “Eu sou Gustavo Oliveira Camargo, RA 236024. Vamos apresentar os requisitos, a arquitetura, o código e as evidências da AF.”

**Confira se entendeu:** Você consegue explicar em uma frase o que o projeto faz? Ele apoia a formação com classificação de competências e orientação de cursos.

## 2. b) Problema e requisitos | 01:00–03:00
**Quem:** Os dois · **Situação:** Preparar

**Entenda primeiro:** Requisito é algo que o sistema precisa fazer. Cada um deve desenvolver e apresentar dois novos requisitos.

- [Abrir tabela de requisitos](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/af/v3-adequacao-entrega/documentacao/af/DIVISAO_AF_V3.md)

**O que fazer:**

1. Mostre a tabela de responsáveis.
2. Diferencie o que já existia na AC1 do que será entregue na AF.

**Fala / explicação para ensaiar:**

> Champam: “Sou responsável pelo RF02, classificação de competências com ML, e pelo RF05, treinamento e acompanhamento.”
> Camargo: “Sou responsável pelo RF03, recomendação com RAG e Spring AI, e pelo RF04, agente com autorização.”

**Confira se entendeu:** Cadastro já era base do projeto. Não use o cadastro herdado para completar a quantidade de requisitos inéditos.

## 3. c) C4 no README | 03:00–06:00
**Quem:** Os dois · **Situação:** Pendente na v3

**Entenda primeiro:** C4 é o mapa da arquitetura. As caixas mostram as partes do sistema e as setas mostram como conversam.

- [Estudar C4 da versão anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/documentacao/af/C4.md)
- [Abrir README em adequação](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/tree/af/v3-adequacao-entrega)

**O que fazer:**

1. Abra o C4 anterior apenas para estudar.
2. Para a gravação final, o C4 atualizado precisa estar no README e refletir o gateway e o Spring AI reais.

**Fala / explicação para ensaiar:**

> Para ensaiar: “O usuário entra pelo frontend. O Core cuida das regras de negócio; a classificação consulta o ML; o treinamento usa uma fila. A orientação precisa recuperar documentos e gerar uma resposta com fontes.”
> Na versão final, cada um explica a parte da arquitetura em que realmente contribuiu.

**Confira se entendeu:** O desenho anterior ainda não comprova gateway nem Spring AI. Não o apresente como arquitetura final da v3.

## 4. d.1) RF02: classificação | 06:00–07:30
**Quem:** Champam · **Situação:** Existe na versão anterior

**Entenda primeiro:** A classificação recebe características de estudo e estima um perfil. O Core é Java; o cálculo do modelo acontece na API Python.

- [1. Abrir chamada no Java](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/src/main/java/br/com/educacao/gamificada/af/OrientacaoController.java#L39-L44)
- [2. Abrir predição no Python](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/ml/app.py#L131-L139)
- [3. Abrir aplicação local](http://localhost:8085/af.html)
- [4. Ver captura anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/documentacao/af/evidencias/demo-af.png)

**O que fazer:**

1. Abra o primeiro link e olhe as linhas destacadas: o Core busca o aluno e monta os dados.
2. Abra o segundo: predict_proba calcula as probabilidades e o retorno escolhe a classe.
3. Com a aplicação iniciada, escolha um aluno existente, use valores válidos e clique em Classificar perfil.

**Fala / explicação para ensaiar:**

> “Aqui o Core consulta o histórico do aluno e envia os dados para a API Python. Neste segundo trecho, o modelo calcula as probabilidades e devolve o perfil. Os dados de treinamento são sintéticos; isso demonstra a integração, mas não valida avaliação de pessoas reais.”

**Confira se entendeu:** Você sabe a diferença entre treinar e classificar? Treinar cria/ajusta o modelo; classificar usa o modelo já treinado.

## 5. d.2) RF05: treinamento | 07:30–09:00
**Quem:** Champam · **Situação:** Existe na versão anterior

**Entenda primeiro:** Job é um pedido de trabalho. A fila guarda pedidos para o worker, que é o processo que executa o treinamento.

- [1. Criar e publicar o job](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/src/main/java/br/com/educacao/gamificada/af/Treinamentos.java#L27-L57)
- [2. Worker que treina](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/ml/worker.py#L29-L50)
- [3. Evidência de retomada anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/documentacao/af/evidencias/integracao.json)

**O que fazer:**

1. No Java, mostre criar: ele salva o pedido e devolve seu identificador.
2. Depois mostre publicar: o pedido é enviado para RabbitMQ.
3. No Python, mostre o consumo, treinamento e confirmação.
4. Abra a evidência de retomada, identificando-a como teste anterior. Não clique em treinar no modo local sem RabbitMQ.

**Fala / explicação para ensaiar:**

> “A solicitação é registrada antes da publicação. O usuário recebe um identificador e consulta o andamento. O worker processa o treinamento e publica o resultado. Nesta evidência anterior, o pedido concluiu após a retomada do serviço.”

**Confira se entendeu:** HTTP 202 significa pedido aceito. Não significa treinamento concluído. A v3 precisa repetir o teste na stack final.

## 6. d.3) RF03: RAG e Spring AI | 09:00–10:30
**Quem:** Camargo · **Situação:** Pendente na v3

**Entenda primeiro:** RAG significa buscar informações em documentos antes de gerar a resposta. Spring AI é a biblioteca Java exigida para integrar a IA.

- [Estudar o RAG Python anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/orientacao/app.py#L19-L44)
- [Ver fontes da demonstração anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/documentacao/af/evidencias/demo-integrada.json)

**O que fazer:**

1. O link existente mostra o protótipo Python para estudo.
2. Ainda falta a implementação Spring AI: não há um arquivo desse serviço pronto para abrir.
3. Depois de implementar, esta etapa precisa apontar para a chamada real do Spring AI, fontes e PR do Camargo.

**Fala / explicação para ensaiar:**

> Explicação para estudar: “Primeiro buscamos trechos relevantes dos documentos. Depois fornecemos esse contexto ao modelo e devolvemos a orientação com suas fontes.”
> Não afirmar que o código Python do link é Spring AI.

**Confira se entendeu:** Mostrar a dependência em um pom.xml não basta: é preciso mostrar uma chamada Spring AI real e funcionando.

## 7. d.4) RF04: agente autorizado | 10:30–12:00
**Quem:** Camargo · **Situação:** Adaptação e contribuição pendentes

**Entenda primeiro:** Um agente coordena etapas e ferramentas. Neste protótipo, o fluxo é controlado e somente leitura; o consentimento permite a consulta.

- [1. Ver recusa sem autorização](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/src/main/java/br/com/educacao/gamificada/af/OrientacaoController.java#L49-L54)
- [2. Ver fluxo Python anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/orientacao/app.py#L45-L50)
- [3. Ver execução anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/documentacao/af/evidencias/agente-integrado.json)

**O que fazer:**

1. Estude a verificação de autorização no Java.
2. Na aplicação ativa, Executar agente sem marcar consentimento deve ser recusado.
3. A versão final precisa mostrar a contribuição real do Camargo, as ferramentas e o contexto de acompanhamento.

**Fala / explicação para ensaiar:**

> Explicação do protótipo: “Sem consentimento, a chamada é recusada. Quando autorizada, segue o fluxo permitido. Não afirmamos que o agente tem autonomia ou ferramentas de escrita.”
> A contribuição final e o PR do Camargo ainda precisam ser realizados.

**Confira se entendeu:** Consentimento não substitui login e permissões. Ele autoriza a atividade dentro do acesso que o usuário já possui.

## 8. e) Gateway e Docker | 12:00–14:00
**Quem:** Os dois · **Situação:** Pendente na v3

**Entenda primeiro:** Gateway é a porta de entrada que encaminha chamadas ao serviço certo. Docker Compose inicia os componentes definidos no projeto.

- [Ver Compose anterior: NÃO é a entrega final](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/compose.af.yaml)
- [Ver Compose padrão atual](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/compose.yaml)

**O que fazer:**

1. O comando obrigatório é docker compose up --build.
2. A configuração anterior pode ser aberta para estudo, mas ainda exige outro arquivo/configuração e processos externos.
3. Não existe gateway v3 pronto para demonstrar. Esta etapa fica bloqueada até a implementação e validação.

**Fala / explicação para ensaiar:**

> Explicação para estudar: “O gateway recebe as chamadas e encaminha cada rota ao serviço responsável. O Compose precisa iniciar frontend, backend e todos os componentes necessários.”
> Não narrar essa execução como concluída antes de ela realmente funcionar.

**Confira se entendeu:** Não basta os contêineres aparecerem como iniciados: a aplicação tem que funcionar por meio deles, sem um launcher manual no host.

## 9. f) Hexagonal ou clean | 14:00–16:00
**Quem:** Os dois · **Situação:** Exemplo anterior; adequar à AF

**Entenda primeiro:** Porta é um contrato do que a aplicação precisa. Adaptador é a implementação que conversa com banco ou serviço externo.

- [1. Abrir porta](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/src/main/java/br/com/educacao/gamificada/ranking/application/RankingPort.java)
- [2. Abrir serviço](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/src/main/java/br/com/educacao/gamificada/ranking/application/RankingService.java)
- [3. Abrir adaptador](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/src/main/java/br/com/educacao/gamificada/ranking/internal/RankingJpaAdapter.java)

**O que fazer:**

1. Abra a porta: é uma interface.
2. Abra o serviço: observe a dependência da porta.
3. Abra o adaptador: veja como o contrato é implementado para persistência.
4. Este exemplo de ranking ajuda a estudar, mas não é prova de um requisito AF inédito. A apresentação final precisa ligar a organização a um fluxo AF real.

**Fala / explicação para ensaiar:**

> “A porta define o contrato, e o adaptador implementa o acesso à tecnologia. O serviço usa o contrato para reduzir o acoplamento. Não afirmamos que todo o sistema é hexagonal apenas por ter pastas com esses nomes.”

**Confira se entendeu:** Você consegue apontar a interface e a classe que a implementa? Esse é o primeiro passo para entender este exemplo.

## 10. g) REST, fila e testes | 16:00–18:00
**Quem:** Os dois · **Situação:** Evidências históricas

**Entenda primeiro:** Síncrono: a chamada aguarda a resposta. Assíncrono: o pedido é aceito e o resultado é acompanhado depois. p95 é o tempo no qual 95% das respostas já terminaram.

- [Teste AF anterior no GitHub](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/43948164512)
- [Medição anterior: 300 usuários](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/documentacao/af/evidencias/carga-final.json)
- [56 testes Java da versão anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/documentacao/af/evidencias/testes-java-ci.json)

**O que fazer:**

1. Mostre REST na classificação e AMQP no treinamento.
2. Abra os testes e a medição anteriores para estudo.
3. Na entrega final, use testes da v3. Não atribua os 0,354 s antigos ao gateway novo sem medir novamente.

**Fala / explicação para ensaiar:**

> “A classificação usa resposta imediata por REST. O treinamento usa fila porque pode demorar e precisa tolerar indisponibilidade. As evidências devem indicar a versão e o ambiente testados.”

**Confira se entendeu:** Os resultados anteriores continuam reais, mas não comprovam automaticamente a arquitetura nova.

## 11. h) Limitações | 18:00–19:00
**Quem:** Os dois · **Situação:** Preparar

**Entenda primeiro:** Limitações são fronteiras reais do protótipo. Uma exigência obrigatória ainda não implementada é uma pendência de entrega.

- [Ver status e limites da versão anterior](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/220a5718a0abb64db3ae16d1bc9279554f5d1821/documentacao/af/STATUS.md)
- [Ver exigências da v3](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/af/v3-adequacao-entrega/documentacao/af/DIVISAO_AF_V3.md)

**O que fazer:**

1. Mostre a seção de limitações atualizada no README final.
2. Fale de dados sintéticos, documentos didáticos e recursos da máquina.

**Fala / explicação para ensaiar:**

> “Usamos dados sintéticos e documentos de exemplo; isso não substitui validação com dados reais autorizados. Modelo local também depende de memória e processamento. Para produção, precisamos ampliar segurança, auditoria e avaliação.”

**Confira se entendeu:** Não usar limitações para justificar a ausência de Spring AI, gateway, Docker correto ou PRs individuais.

## 12. i) Encerramento e PRs | 19:00–20:00
**Quem:** Os dois · **Situação:** PRs e merge pendentes

**Entenda primeiro:** PR é um pedido de revisão das alterações. O outro integrante revisa; só depois ocorre o merge, que integra o trabalho à main.

- [Abrir PRs reais](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/pulls?q=is%3Apr)
- [Abrir main para conferir](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/tree/main)
- [Abrir roteiro completo v3](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/blob/af/v3-adequacao-entrega/documentacao/af/Roteiro_AF_V3_20_Minutos.md)

**O que fazer:**

1. Abra a lista real de PRs. Ela não deve ser apresentada como aprovada se ainda estiver vazia ou pendente.
2. Na entrega final, cada um aponta seus requisitos, commits e revisão.
3. Encerrar com 20 minutos e os dois ainda de câmera aberta.

**Fala / explicação para ensaiar:**

> Após concluir de verdade: “Apresentamos os requisitos, a arquitetura, o código e os resultados. Aqui estão as contribuições revisadas da equipe e a integração à main. A documentação explica a execução e os limites do projeto.”

**Confira se entendeu:** Você só deve dizer “meu código” e “meu PR aprovado” quando puder mostrar sua contribuição e a revisão real.

## O que enviar
Vídeo de 20 minutos no YouTube NÃO LISTADO e link do GitHub com documentação, fontes e contribuições revisadas. Ambos de câmera aberta durante todo o vídeo. O roteiro não é relatório de entrega.
