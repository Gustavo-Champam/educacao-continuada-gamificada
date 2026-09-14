# Educação Continuada Gamificada

Aplicação acadêmica em Java 17, Spring Boot e Vue.js para a **US01: progressão de Aluno Básico para Premium**.

## Escopo e estado da implementação

A responsabilidade desta parte termina na alteração de `BASICO` para `PREMIUM`. O domínio decide a promoção, a aplicação persiste o novo plano e publica o evento interno `AlunoPromovidoEvent`. Carteira, vouchers, moedas e demais recompensas pertencem à US02.

**Verificação realizada:** o domínio foi compilado com Java 17 e passou em 15 verificações auxiliares nas versões GREEN e BLUE. Os testes JUnit, a cobertura JaCoCo, o build Vue, H2/PostgreSQL em execução e Docker ainda precisam ser executados no ambiente de desenvolvimento ou na CI. Os arquivos de configuração e os testes estão preparados; isso não constitui evidência de execução dessas ferramentas.

## Estudo de caso

Uma plataforma de educação continuada oferece cursos online por assinatura. No estudo de caso, a conclusão de cursos e a participação no fórum geram benefícios; ao atingir a marca de 12 cursos, o aluno passa ao plano Premium e passa a ter benefícios de uma etapa posterior.

O recorte escolhido pelo grupo em `documentacao/Template_ATDD.xlsx` é a promoção de plano. A US01 determina que o 12º curso seja concluído com média igual ou superior a 7,0. Esta implementação considera como progresso apenas cursos distintos concluídos com média **≥ 7,0**. Notas menores não aumentam o contador e permitem nova tentativa do mesmo curso. Esta interpretação da contagem deve permanecer alinhada ao critério de aceite aprovado pelo grupo/professora.

Liberação de três cursos e premiação por fórum não fazem parte das duas US registradas na planilha recebida e não foram adicionadas a este recorte.

## Integrantes e autoria

- Gustavo Champam
- Gustavo Camargo

| História | Conteúdo | Autor da US e dos BDD |
| --- | --- | --- |
| US01 — Aluno Básico | Alterar o plano para Premium ao atingir 12 cursos válidos | **PENDENTE: identificar qual integrante é o responsável** |
| US02 — Aluno Premium | Receber voucher e três moedas após a promoção | **PENDENTE: identificar o outro integrante** |

O responsável pela US01 confirmou que sua parte termina na mudança de status, mas não informou qual dos dois nomes lhe corresponde. A autoria não foi inferida pelo dono do repositório. Os commits de preparação assistida estão identificados como Codex; não substituem a identificação da contribuição acadêmica individual.

## US escolhida e BDD

**US01:** Como aluno ativo da plataforma com assinatura básica, quero que minha assinatura seja atualizada automaticamente para Premium ao atingir 12 cursos concluídos com média válida, para ter acesso aos benefícios do novo plano.

Os cenários e sua relação com os testes estão em [BDD-US01.md](documentacao/BDD-US01.md). O Excel original foi preservado. A segunda aba ainda contém um exemplo de jogos de adivinhação e deve ser substituída pelo grupo na versão final de entrega.

## Organização

- `domain`: Aluno e Plano, sem dependência de Spring ou JPA.
- `src/test/java/.../domain/AlunoTest.java`: testes unitários da regra.
- `entity` e `repository`: persistência JPA dos alunos e cursos contabilizados.
- `service`: transação, prevenção de duplicidade e evento de promoção.
- `dto` e `controller`: contratos HTTP, validação e Swagger.
- `frontend`: interface Vue para cadastro, consulta e conclusão de cursos.
- `evidencias`: resultados auxiliares e checklist acadêmico.

Pacotes Java usam minúsculas (`domain`); os testes ficam em `src/test/java`, conforme a estrutura Maven. Isso corresponde ao pacote de domínio e à classe de teste pedidos na atividade.

## IntelliJ Ultimate e H2

1. Abrir o `pom.xml` como projeto Maven e selecionar **JDK 17**.
2. Recarregar o Maven para obter as dependências.
3. Na janela Maven, executar `clean` e `verify`, ou usar o comando abaixo se Maven estiver instalado:

```sh
mvn clean verify
```

4. Executar `EducacaoGamificadaApplication`. O perfil padrão é `h2`.
5. Abrir Swagger: `http://localhost:8080/swagger-ui/index.html`.
6. Abrir `http://localhost:8080/h2-console`: JDBC URL `jdbc:h2:mem:educacao`, usuário `sa`, senha vazia.

O H2 usa memória e perde os registros ao encerrar a aplicação. O teste PostgreSQL fica ignorado quando `TESTAR_POSTGRES` não for `true`; não deve ser apresentado como PostgreSQL validado.

### Front-end local

Com Node.js 22.12 ou superior na linha 22, em um segundo terminal:

```sh
cd frontend
npm install
npm run dev
```

Abrir `http://localhost:5173`. O Vite encaminha `/api` para `localhost:8080`. O primeiro `npm install` gera `package-lock.json`; inclua-o no versionamento após executar e validar o build.

## Docker e PostgreSQL

Com Docker Desktop ativo, na raiz:

```sh
docker compose up --build -d
docker compose ps
docker compose logs api
```

O build do backend executa `mvn clean verify`, incluindo testes H2 e a exigência de cobertura do domínio. Não pula testes. O teste PostgreSQL é executado separadamente ou pela CI.

| Componente | Endereço / acesso local |
| --- | --- |
| Vue | `http://localhost:5173` |
| Swagger | `http://localhost:8080/swagger-ui/index.html` |
| OpenAPI | `http://localhost:8080/v3/api-docs` |
| pgAdmin | `http://localhost:5050` |
| PostgreSQL | `localhost:5432`, banco `educacao`, usuário `educacao` |

Credenciais de demonstração estão em `.env.example`. Para personalizar, copie-o para `.env` antes da primeira inicialização. Por padrão, a senha do banco é `educacao_local`; o pgAdmin usa `admin@educacao.local` e `admin_local`.

No pgAdmin, cadastrar um servidor com host **`postgres`**, porta `5432`, banco `educacao`, usuário `educacao` e a senha configurada. `postgres` é o nome entre containers; `localhost` é usado pelo computador.

Consulta para evidências:

```sql
SELECT id, nome, plano, cursos_concluidos FROM alunos ORDER BY id;
SELECT aluno_id, codigo_curso, media FROM conclusoes_cursos ORDER BY aluno_id, codigo_curso;
```

Para parar preservando os dados: `docker compose down`. O volume PostgreSQL mantém os registros. H2 e PostgreSQL são perfis separados; demonstre cada um em sua execução correspondente.

## Demonstrar a promoção

Na interface, cadastrar um aluno e registrar 12 códigos diferentes com média ≥ 7. O 12º registro deve atualizar o status para Premium. Para uma demonstração rápida via PowerShell:

```powershell
./scripts/demonstrar-promocao.ps1
```

O script cria um aluno, registra 11 cursos, tenta o 12º com nota 6,99 e depois com 7,0. Verifica a resposta final e informa o ID para consultar na interface e no banco.

| Método | Caminho | Comportamento |
| --- | --- | --- |
| POST | `/api/alunos` | Cria Básico com zero cursos; 201 |
| GET | `/api/alunos` | Lista alunos |
| GET | `/api/alunos/{id}` | Consulta aluno; 404 se não existe |
| POST | `/api/alunos/{id}/conclusoes` | Contabiliza curso válido e avalia promoção; 409 para duplicidade |

Cadastro: `{"nome":"Gustavo"}`.

Conclusão: `{"codigoCurso":"JAVA-01","media":7.0}`.

A resposta contém `aluno`, `cursoContabilizado` e `promovidoAgora`. Nota abaixo de 7 é uma solicitação válida com HTTP 200 e `cursoContabilizado: false`. Campos ausentes, notas fora de 0–10 e nome/código vazios retornam 400. Códigos são normalizados removendo espaços das extremidades e convertendo para maiúsculas.

Não há endpoint para atribuir manualmente o plano ou o contador. Conclusões concorrentes do mesmo aluno são serializadas por bloqueio de escrita no banco. Uma restrição única por aluno/curso também protege a persistência.

## TDD e cobertura

| Etapa | Commit local | Conteúdo | Evidência disponível |
| --- | --- | --- | --- |
| RED | `45be164` | Testes e implementação vazia | Reexecução Java: 12 falhas e 3 sucessos |
| GREEN | `82e7c49` | Implementação mínima | Java: 15 sucessos |
| BLUE | `af3e96e` | Constantes e separação das regras | Java: 15 sucessos |

O executável `javac` não estava disponível, mas o módulo compilador do Java estava. O script foi corrigido para invocar esse módulo, e RED foi reexecutado a partir de seu commit. As primeiras tentativas RED/GREEN no histórico falharam por ausência de `javac`; os logs finais distinguem a reexecução das asserções. Não são capturas JUnit no IntelliJ.

Para gerar evidências JUnit históricas sem alterar a versão atual:

```sh
git worktree add ../us01-red 45be164
git worktree add ../us01-green 82e7c49
mvn -f ../us01-red/pom.xml -Dtest=AlunoTest test
mvn -f ../us01-green/pom.xml -Dtest=AlunoTest test
mvn clean verify
```

No RED, falhas de asserção são esperadas. Falha de download, compilação ou configuração não comprova RED de regra de negócio. No GREEN, os testes devem passar. Na versão final, usar **Run 'AlunoTest' with Coverage** no IntelliJ e gerar o relatório Maven em `target/site/jacoco/index.html`.

O JaCoCo relata **toda a aplicação**, e a verificação automática exige **100% de linhas e ramos do pacote `domain`**. Isso não significa 100% de toda a aplicação e não foi medido aqui. Se a professora exigir todas as camadas, ampliar testes a partir do relatório real, mantendo a cobertura do domínio.

## Teste PostgreSQL real

Com o banco em execução (`docker compose up -d postgres`), no PowerShell:

```powershell
$env:TESTAR_POSTGRES = "true"
$env:DB_URL = "jdbc:postgresql://localhost:5432/educacao"
$env:DB_USER = "educacao"
$env:DB_PASSWORD = "educacao_local"
mvn clean verify
```

`AlunoPostgresTest` confirma o produto PostgreSQL via JDBC e verifica a promoção após recarregar os dados da persistência. Os dados desse teste são revertidos ao terminar. Isso não valida a tela do pgAdmin nem substitui capturas.

## Verificação no GitHub

O workflow `.github/workflows/verificar.yml` foi preparado para testes H2/PostgreSQL, JaCoCo e build Vue após o envio da branch. Disponibiliza os relatórios como artefatos. Ainda não foi executado, e a branch não foi enviada ao remoto.

## Pendências antes da entrega

- Identificar autores de US e BDD no README e na planilha.
- Substituir o exemplo de jogos da segunda aba do Excel pelos cenários da aplicação.
- Executar JUnit RED/GREEN/BLUE no IntelliJ Ultimate e guardar prints.
- Medir a cobertura real e resolver linhas/ramos exigidos pela professora.
- Executar backend, build Vue e Docker e registrar o funcionamento.
- Capturar tabelas e mudança de status no H2 e PostgreSQL/pgAdmin.
- Revisar e enviar a branch ao GitHub, identificando a contribuição individual.

Checklist: [evidencias/README.md](evidencias/README.md).
