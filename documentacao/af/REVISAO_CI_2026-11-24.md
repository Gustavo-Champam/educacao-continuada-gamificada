# Revisão da falha de CI — 24/11/2026

O e-mail recebido refere-se ao commit `ed4c94b`, não ao head `7bc4f95` que estava na branch ao iniciar esta revisão.

## Evidências da execução com falha

- [Run 45288689810](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/45288689810): `RuntimeError: Tempo excedido: /actuator/health` após 600 segundos.
- A interface falhou depois com `ERR_CONNECTION_REFUSED` na porta 8085, pois a aplicação não estava disponível.
- O artefato contém a lista de containers vazia e log de containers vazio. O log de build em `/tmp/af-compose.log` não foi publicado.
- A execução de push do mesmo commit passou. Os quatro workflows de push/PR de `7bc4f95` também passaram. Portanto, não há evidência de erro determinístico de compilação nesse commit.

O motivo inicial da falha de construção/inicialização não pode ser recuperado com certeza: seu log não foi preservado. Não se atribui a falha a Maven, download de imagem ou rede sem essa evidência.

## Correções desta revisão

1. O workflow aguarda `docker compose up --build -d`, propaga seu código de erro com `pipefail` e publica `compose-build.log`. Os testes começam somente após o comando concluir.
2. O navegador só executa quando a integração que prepara seus dados tiver passado. Isso evita uma segunda falha sem diagnóstico quando a aplicação sequer iniciou.
3. A API pública valida tamanho mínimo da pergunta e os três perfis aceitos. Antes, entradas incompatíveis chegavam ao serviço interno, cujo 400 era convertido pelo Core em 503.
4. Um teste HTTP verifica 400 sem consultar aluno/IA. O teste do agente confere o progresso do banco, ausência de nome/ID no payload e recusa antes de consultar o aluno. O aceite Docker também verifica as entradas inválidas.
5. `mvnw` passa a ter permissão de execução no Git, conforme o comando Linux documentado.

## Conferência após publicação

Consultar os checks do [PR #2](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/pull/2) para o commit desta revisão. A descrição do PR registra os runs efetivamente concluídos. A mensagem antiga de falha permanece no histórico, mesmo depois de execuções posteriores aprovadas.

GitGuardian é uma pendência separada: senhas didáticas no histórico continuam exigindo triagem. Esta revisão não desabilita o scanner, não reescreve histórico e não realiza merge. As limitações do corpus fictício e da geração local continuam documentadas no README.
