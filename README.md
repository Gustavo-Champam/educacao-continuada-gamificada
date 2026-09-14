# Educação Continuada Gamificada

Aplicação acadêmica de **ATDD, BDD e TDD** com Spring Boot, JPA, H2, PostgreSQL, Swagger, Vue e Docker.

## Estudo de caso e integrantes

Uma plataforma de educação continuada incentiva o aluno a concluir cursos. Ao completar 12 cursos distintos com média igual ou superior a 7,0, o aluno Básico passa ao Premium. A promoção habilita sua carteira com **1 voucher de projeto real e 3 moedas virtuais**, registrando a origem e a data dos prêmios. Cursos com média inferior a 7,0 não aumentam o progresso e podem ser tentados novamente. Um curso aprovado conta apenas uma vez por aluno.

| Integrante | História e BDD sob sua responsabilidade |
| --- | --- |
| **Gustavo Camargo** | **US01 — Aluno Básico:** Como aluno com assinatura básica, quero ser promovido automaticamente ao Premium ao concluir 12 cursos válidos, para acessar os benefícios do novo plano. |
| **Gustavo Champam** | **US02 — Aluno Premium:** Como aluno recém-promovido, quero receber um voucher e três moedas em minha carteira, para ter acesso às recompensas da plataforma. |

**US escolhida originalmente: US01. Entrega integrada: US01 + US02.** A branch `feat/us01-promocao-aluno` foi integrada à `main`, preservando o histórico do Gustavo Camargo e os testes RED da US02 do Gustavo Champam. O desenvolvimento recebeu assistência de IA, incluindo implementação complementar e verificação. As atribuições acadêmicas seguem a documentação existente do grupo.

A entrega implementa concessão e consulta de prêmios. Resgate, conversão em criptomoeda e premiação por fórum não têm critérios de aceite neste recorte.

## BDD e ATDD

- [Cenários da US01 — Gustavo Camargo](documentacao/BDD-US01.md)
- [Cenários da US02 — Gustavo Champam](documentacao/BDD-US02.md)
- [Planilha ATDD preenchida](documentacao/Template_ATDD.xlsx)

Os critérios de aceite são automatizados com JUnit 5 e MockMvc, executando Controller → Service → Domain → JPA → H2. O teste `AlunoPostgresTest` verifica também PostgreSQL real. Cucumber é opcional na atividade e não é necessário para executar estes cenários. Os testes de aceitação da US02 foram registrados falhando antes da implementação das recompensas e do histórico.

## Executar com IntelliJ Ultimate

1. Abrir esta pasta no IntelliJ Ultimate e importar o `pom.xml` como Maven.
2. Selecionar **JDK 17** e recarregar as dependências.
3. Executar `EducacaoGamificadaApplication`. O perfil padrão é H2.
4. Abrir o Swagger em <http://localhost:8080/swagger-ui/index.html>.
5. Em outro terminal, executar o front-end:

```sh
cd frontend
npm ci
npm run dev
```

Interface: <http://localhost:5173>. Requer Node.js 22.12+ e Java 17. O proxy Vite encaminha `/api` ao Spring Boot em 8080.

Para testar e medir cobertura:

```sh
mvn clean verify
```

Ou executar as mesmas tarefas na janela Maven do IntelliJ. **Run with Coverage** sobre os testes permite gerar a captura da IDE solicitada pela professora. As evidências desta entrega foram produzidas por Maven/JUnit, JaCoCo e navegador real; não são capturas de execução dentro do IntelliJ.

## Docker, PostgreSQL e pgAdmin

```sh
docker compose up --build -d
```

| Serviço | Endereço |
| --- | --- |
| Vue | <http://localhost:5173> |
| Spring Boot / Swagger | <http://localhost:8080/swagger-ui/index.html> |
| pgAdmin | <http://localhost:5050> |
| PostgreSQL | `localhost:5432`, banco e usuário `educacao` |

Credenciais locais de demonstração: PostgreSQL `educacao_local`; pgAdmin `admin@educacao.com` / `admin_local`. Para alterar, copiar `.env.example` para `.env` antes da primeira inicialização. O servidor PostgreSQL já é cadastrado no pgAdmin; informar a senha do banco quando solicitada. Entre containers, o host é `postgres`.

Para demonstrar também H2 em um container separado:

```sh
docker compose --profile demonstracao up --build -d
```

H2/Swagger adicional: <http://localhost:8081/swagger-ui/index.html>. Console: <http://localhost:8081/h2-console>. JDBC `jdbc:h2:mem:educacao`, usuário `sa`, senha vazia. Fora do Docker, com o perfil H2 padrão, usar a porta 8080.

Para encerrar preservando o volume PostgreSQL: `docker compose --profile demonstracao down`. H2 é volátil; PostgreSQL usa volume persistente. Os serviços são publicados apenas em localhost.

## Endpoints e demonstração

| Método | Endpoint | Resultado |
| --- | --- | --- |
| POST | `/api/alunos` | Cadastra Básico com zero cursos e zero prêmios (201) |
| GET | `/api/alunos` | Lista alunos com progresso e prêmios |
| GET | `/api/alunos/{id}` | Consulta aluno (404 se ausente) |
| POST | `/api/alunos/{id}/conclusoes` | Registra curso e avalia promoção; 409 se repetido |
| GET | `/api/alunos/{id}/recompensas` | Histórico com origem, quantidades e data |

Cadastro: `{"nome":"Gustavo"}`. Conclusão: `{"codigoCurso":"JAVA-01","media":7.0}`.

A promoção devolve `promovidoAgora: true`, plano `PREMIUM`, `vouchers: 1` e `moedas: 3`. Média abaixo de 7 devolve HTTP 200 com `cursoContabilizado: false`. Dados inválidos devolvem 400. Códigos são normalizados com remoção de espaços externos e conversão para maiúsculas.

Demonstração automatizada, criando apenas um aluno novo por execução:

```sh
python scripts/verificar-http.py http://localhost:8080 evidencias/execucao/http.json
```

Consultas para mostrar os dados no H2 e pgAdmin:

```sql
SELECT id, nome, plano, cursos_concluidos, vouchers, moedas FROM alunos ORDER BY id;
SELECT aluno_id, codigo_curso, media FROM conclusoes_cursos ORDER BY aluno_id, codigo_curso;
SELECT aluno_id, vouchers, moedas, origem, registrado_em FROM recompensas_premium ORDER BY aluno_id;
```

## Camadas e proteção contra duplicação

`domain` contém `Aluno` e `Plano`, sem Spring/JPA. Os pacotes `entity`, `repository`, `service`, `dto` e `controller` separam persistência, transações, contratos e HTTP. O teste individual da US02 está em `src/test/java/.../domaintest/AlunoPremiumTest.java`; a US01 mantém `.../domain/AlunoTest.java`. Nomes de pacotes seguem a convenção Java de letras minúsculas.

A transação de conclusão bloqueia o aluno para atualização, grava a aprovação e publica `AlunoPromovidoEvent`. O listener síncrono `RecompensaService` registra o histórico na mesma transação. A chave única aluno/curso evita conclusões repetidas; a chave por aluno do histórico e o bloqueio evitam registrar duas vezes a premiação. Os prêmios deste recorte são benefícios fixos da promoção, sem operações de consumo de saldo.

## Evidências RED, GREEN e BLUE

| Etapa | Commit / arquivo | Resultado |
| --- | --- | --- |
| RED US01 | `45be164` e `evidencias/red/verificacao-java.txt` | Histórico preservado da implementação do colega |
| GREEN US01 | `82e7c49` | Implementação mínima preservada |
| BLUE US01 | `af3e96e` | Refatoração preservada |
| RED US02 | `94d0807`, `evidencias/red/us02-junit.log` | 3 testes executados, 3 falhas de asserção |
| RED integração US02 | `dca15de`, `evidencias/red/us02-aceitacao.log` | 20 testes, 5 falhas esperadas |
| GREEN US02 | `a1c46c4`, `evidencias/green/us02-junit.log` | 33 testes aprovados; PostgreSQL ainda ignorado nessa etapa |
| BLUE final | `evidencias/blue/verificacao-completa.log` | **37 testes, 0 falhas, 0 erros, 0 ignorados**, incluindo PostgreSQL |
| Cobertura final | `evidencias/blue/cobertura/index.html` | **100% de instruções, linhas, ramos e métodos nas 16 classes Java medidas** |
| Navegador | `evidencias/blue/vue-e2e.log` | Cadastro, promoção, carteira, duplicidade, recarga e tela móvel |

Os erros de compilação preliminares estão identificados separadamente em `us02-compilacao.log`; eles não são a evidência de RED comportamental. O relatório JaCoCo mantém todas as classes e não exclui camadas para obter 100%. Cobertura mede execução do código; não substitui os critérios de aceite.

Reproduzir RED e GREEN da US02 sem modificar o projeto atual:

```sh
git worktree add ../educacao-red 94d0807
git worktree add ../educacao-green a1c46c4
mvn -f ../educacao-red/pom.xml -Dtest=AlunoPremiumTest test
mvn -f ../educacao-green/pom.xml -Dtest=AlunoPremiumTest test
```

RED deve falhar por asserções. GREEN deve passar. Para BLUE, executar `mvn clean verify` na versão atual e abrir `target/site/jacoco/index.html`.

## Verificação PostgreSQL e GitHub Actions

No PowerShell, com o PostgreSQL dedicado de teste acessível:

```powershell
$env:TESTAR_POSTGRES = "true"
$env:DB_URL = "jdbc:postgresql://localhost:5432/educacao"
$env:DB_USER = "educacao"
$env:DB_PASSWORD = "educacao_local"
mvn clean verify
```

Sem `TESTAR_POSTGRES=true`, o teste PostgreSQL é explicitamente ignorado. A execução local registrada usou PostgreSQL 18 dedicado em 55432; o Compose usa PostgreSQL 17.

[GitHub Actions](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions) verifica o backend com H2/PostgreSQL, o build Vue e o Compose completo. Os artefatos incluem testes, cobertura, logs dos containers, consultas SQL e capturas da interface.

O Docker Desktop deste computador apresentou erro interno no gerenciador de inferência antes de iniciar o engine. A execução de containers deve ser comprovada pelos resultados reais do job Docker, não pelo arquivo Compose isoladamente. Consulte o [índice de evidências](evidencias/README.md) para o estado verificado.

## Entrega no Canvas

Link do projeto: **https://github.com/Gustavo-Champam/educacao-continuada-gamificada**.

Antes da apresentação, abrir o projeto no IntelliJ Ultimate e capturar o RED, GREEN e BLUE com cobertura na IDE, caso a professora exija especificamente essas telas. Não houve envio ao Canvas por esta automação.
