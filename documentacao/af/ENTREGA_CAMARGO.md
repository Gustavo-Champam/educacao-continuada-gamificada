# Entrega Camargo — RF03 e RF04

Branch baseada em `feat/af-champam-rf02-rf05`, com apoio do Codex. Histórico anterior preservado.

A manutenção do ambiente removeu a implementação local antes da publicação. Esta é uma reconstrução: não reutilizar os resultados de 60/16 testes da versão perdida como evidência desta versão. Os testes da reconstrução são executados no GitHub Actions, incluindo geração real via Ollama no workflow AF.

## Executar no Windows

Abra o Docker Desktop. No PowerShell:

```powershell
git clone --branch feat/af-camargo-rf03-rf04 https://github.com/Gustavo-Champam/educacao-continuada-gamificada.git educacao-af-camargo
cd educacao-af-camargo
docker compose up --build
```

Em outro terminal nessa pasta:

```powershell
docker compose ps -a
docker compose logs --tail=30 ollama-init
```

Espere o download do modelo terminar. `ollama-init` e `ml-init` terminam com código zero; isso é normal. Abra http://localhost:8085. Conta de laboratório `camargo`, mesma senha da equipe documentada no README. Não use essas credenciais em produção.

1. Cadastre um aluno e registre cursos com média 8.
2. Pergunte sobre Java e APIs REST e use Consultar RAG. Confira resposta e fontes.
3. Execute o agente sem autorização: deve retornar 403.
4. Autorize e execute: confira o plano e total real de cursos no campo progresso. Nenhum dado deve mudar.
5. Desmarque e repita: 403. Trocar conta/aluno limpa o consentimento.
6. Pergunte sobre astronomia: nenhuma fonte e nenhuma geração.
7. Execute `docker compose stop ollama-af`: orientação retorna 503, consulta de alunos continua. Retome com `docker compose start ollama-af`.
8. Encerre com `docker compose down`, preservando volumes.

## Estudar e apresentar

- `OrientarAluno`: caso de uso e portas, autorização antes de ferramentas.
- `DocumentosLocais`: recuperação lexical com normalização e fontes do corpus didático.
- `GeradorSpringAi`: uso real de ChatModel, prompt com contexto recuperado e validação de IDs citados.
- `AcessoInterno`: token entre serviços, sem porta pública da orientação.
- `OrientacaoController`: progresso consultado no banco após consentimento, sem nome/ID enviado ao modelo.
- `compose.yaml`: modelo independente do Core e download inicial automático.

## Testes e entrega

Com JDK 17: `mvnw.cmd verify` e `mvnw.cmd -f orientacao-ai/pom.xml verify`. Os relatórios JaCoCo ficam em `target/site/jacoco` de cada projeto. Testes unitários simulam o modelo; `scripts/validar-orientacao.py` usa geração real e interrompe Ollama para verificar falhas. O workflow AF produz `evidencias/af-ci/orientacao-real.json`.

A revisão técnica do PR #1 foi registrada sem aprovação automática. Existe um check GitGuardian reprovado por credenciais didáticas no histórico: Champam deve avaliar os alertas e corrigir a afirmação de que todos os checks passaram. Não desabilitar o scanner nem reatribuir autores para simular participação.

Após checks aprovados, Camargo deve ler e compreender seu código; Champam deve revisar seu PR; Camargo deve concluir a revisão humana do PR #1. Não houve merge automático. Gravar e postar o vídeo e enviar links no portal são etapas de vocês.

O PDF recebido contém itens a–e de arquitetura, C4, comunicação, três ASRs e ADR. As exigências de vídeo de 20 minutos e sequência a–i aparecem nas notas da equipe; falta conferir o enunciado complementar. A base documental é fictícia, não oficial da FACENS. Agente somente leitura, sem matrícula nem mudança de plano.
