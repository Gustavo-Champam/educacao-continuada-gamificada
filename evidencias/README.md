# Evidências da US01

## Executado nesta preparação

- Compilação do domínio e de `scripts/VerificacaoDominio.java` pelo módulo compilador Java 17.
- Reexecução RED `45be164`: **12 falhas e 3 sucessos**.
- GREEN: **15 sucessos e zero falhas**.
- BLUE: **15 sucessos e zero falhas**.
- Análise de sintaxe dos 19 arquivos Java: zero erros, sem resolver dependências Spring/JUnit.
- Sintaxe do JavaScript da tela Vue, configuração Vite, POM XML, package.json e YAML conferida. Isso não substitui o build ou a execução da interface.

Os logs estão em `red`, `green` e `blue`. O verificador auxiliar **não substitui JUnit, JaCoCo ou capturas do IntelliJ Ultimate**.

As primeiras tentativas falharam porque `javac` não estava disponível. Depois foi utilizado `java -m jdk.compiler/com.sun.tools.javac.Main`, e RED foi recuperado do commit para reexecução. Os logs finais mostram os resultados de asserções; o histórico preserva as tentativas anteriores.

## Evidências acadêmicas a produzir

| Requisito | Como produzir | Situação |
| --- | --- | --- |
| RED JUnit | Executar AlunoTest no commit RED pelo IntelliJ; capturar asserções falhando | Pendente |
| GREEN JUnit | Executar AlunoTest no commit GREEN; capturar todos passando | Pendente |
| GREEN cobertura | Run with Coverage na versão GREEN | Pendente |
| BLUE JUnit e cobertura | Maven clean verify e Run with Coverage no IntelliJ | Pendente |
| 100% sem vermelho/amarelo | Conferir linhas e ramos no relatório real, conforme escopo da professora | Não medido |
| H2 | Rodar perfil H2, promover aluno e consultar alunos no Console | Pendente |
| PostgreSQL/pgAdmin | Rodar Compose e consultar tabelas no pgAdmin | Pendente |
| Docker | Capturar docker compose ps e logs da aplicação iniciada | Pendente |
| Swagger | Mostrar endpoints e resposta da promoção | Pendente |
| Vue | Mostrar Básico com 11 cursos e Premium após o 12º | Pendente |

Maven e Docker não estão instalados no ambiente utilizado; o acesso ao Maven Central falhou. As dependências Vue não estão disponíveis. Portanto não foi possível executar Spring/JUnit, JaCoCo, build Vue, bancos ou containers.

O workflow GitHub foi preparado para testes com H2 e PostgreSQL real, cobertura e build Vue. Apenas depois de executado seus relatórios poderão ser usados como evidências adicionais. Ele não substitui a demonstração no IntelliJ exigida pela professora.
