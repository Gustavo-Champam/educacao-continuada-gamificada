> **Registro histórico da stack anterior.** Consulte o [README AF v3](../../README.md) e a [entrega RF02/RF05](ENTREGA_CHAMPAM.md) para execução e pendências atuais.

# AF - implementação e evidências

Gustavo Gutierres Champam (RA 223645) e Gustavo Oliveira Camargo (RA 236024).

A evolução está publicada na branch `af/evolucao-ia-local` da AC1. O relatório escrito responde aos itens a-e; a implementação e o roteiro complementam a preparação conforme o escopo solicitado pela dupla.

## Funcionalidades verificadas

- Cadastro/consulta de alunos e catálogo persistente de cursos, com validação e rejeição de código duplicado.
- Regras anteriores da AC1: conclusão, promoção Premium e recompensas preservadas.
- Classificação Python com modelo real treinado em 1.500 registros sintéticos; o histórico de conclusões vem do Core.
- Job/outbox, RabbitMQ, worker e consulta de estado: aceitação com ML ou broker interrompido e conclusão após retomada, testadas em Docker na CI.
- Autorização: 401 anônimo, 403 para outro aluno e agente sem consentimento; acesso ao próprio aluno permitido.
- Interface real: cadastro, catálogo, classificação, recomendação com fontes e gráfico RAGAS verificados em navegador.
- RAG local e agente somente leitura: Qwen3-4B-GGUF, recuperação TF-IDF, quatro documentos didáticos. Não usa Spring AI ou pgvector nesta adaptação.
- RAGAS iniciado pelo Core e executado localmente: fidelidade 1,000 e relevância 0,862 em uma amostra. Métricas de contexto não foram calculadas nessa execução sem referência.

## Testes e rastreabilidade

56 testes Java aprovados na CI com H2 e PostgreSQL, nenhum ignorado. JaCoCo: 100% de linhas e ramificações, sem reduzir o gate. No Windows, o teste PostgreSQL é ignorado quando o banco não está disponível: 55 executados e um ignorado. Python: quatro testes de orientação e um teste de equivalência da inferência com o pipeline treinado.

A cobertura Java não significa qualidade total nem cobertura de todos os serviços. As evidências específicas estão em `evidencias/testes-java-ci.json`, `testes-java-local.json`, `testes-python.json`, `demo-integrada.json`, `agente-integrado.json` e `ragas-integrado.json`.

## Desempenho

Resultado final aprovado no commit `6c9e499a40ab709d234a72cb10b4cb88f40cf323`:

- 300 usuários em loop fechado, dois alunos e entradas variadas.
- 60 segundos medidos após 30 segundos fixos de aquecimento.
- **70.179 classificações; p95 de 0,354 s; zero erros.**
- Três rajadas iniciais de 300 requisições: p95 de 0,990 s, 0,698 s e 0,603 s, todas sem erros.
- Ambiente: GitHub Actions Ubuntu 24.04, Docker, gerador e serviços no mesmo host.
- Gerador: aiohttp 3.14.5. O histórico com HTTPX foi preservado, incluindo as tentativas que não atingiram a meta. O diagnóstico local mostrou influência do gerador; a mudança não relaxou o limite de 2 s nem a concorrência.

[Evidência da integração, carga e interface](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/43948164512) - concluída com sucesso.

[Regressão Java, Vue e Docker da AC1](https://github.com/Gustavo-Champam/educacao-continuada-gamificada/actions/runs/43948164464) - concluída com sucesso.

JSONs: `evidencias/carga-final.json`, `historico-carga.json`, `diagnostico-gerador.json`, `integracao.json` e `interface-ci.json`. O resultado atende ao RNF01 no ensaio executado; não é garantia de capacidade de produção, de outro hardware ou de concorrência com geração RAG.

## Limites e passos manuais

Contas didáticas fixas, documentos de exemplo e dados sintéticos. O agente coordena um fluxo autorizado de leitura; não escolhe ferramentas livremente nem realiza matrícula. Identidade corporativa, TLS, auditoria, fila de falhas e política operacional de retentativas são evoluções para produção. A inferência deve ser revalidada em dados reais autorizados.

Docker foi testado no GitHub Actions; RAG/RAGAS foram executados no Windows. O teste local Core/H2 não é apresentado como teste local de RabbitMQ. Consulte EXECUCAO.md para reproduzir cada cenário.

A dupla ainda precisa gravar a reunião real e enviar os arquivos e o vídeo no Canvas conforme a orientação final da professora. A documentação fornecida não estabelece duração obrigatória de vídeo nem dispensa da prova. Não há garantia de nota.
