# Decisões Técnicas de Modelagem e Agregação

Para adequarmos o conjunto de dados provido para uso em um ambiente NoSQL, abandonamos em parte a rigidez da terceira forma normal, otimizando as capacidades de um sistema Document-Oriented baseado em JSON, como o MongoDB.

## Separação Inicial x Aninhamento de Documentos

1. **Separação Inicial (`producao_clean`, `pessoa_clean`, `equipe_clean`)**: Optamos por em um primeiro momento limpar e persistir exatamente as mesmas 3 entidades em coleções próprias. Isso atende às exigências numéricas massivas de operações que muitas vezes requerem isolamento em relatórios (ex: número total de artistas sem necessidade de se buscar por filmes).
2. **Aninhamento (`producoes_com_participantes`)**: Para evitar operações como `JOIN` (Lookup no MongoDB) toda vez que uma requisição quiser abrir uma obra e exibir imediatamente o elenco completo, consolidamos as regras. Criamos essa coleção híbrida, anexando um vetor (`array`) com os elencos (`equipe`). Isto explora a **vantagem total do modelo NoSQL**.

## Tratamento via Pipeline do MongoDB (Aggregation)
Ao invés de consumir 12 milhões de registros da `raw_equipe` puxando para o back-end em Python e percorrendo em `for` - que é notoriamente pesado por custo de I/O de disco para memória e processador -, a transformação usou a Aggregation API (`$match`, `$project`, `$group`). As transformações ocorreram inteiramente a nível de motor de banco de dados, sendo reescritas com `$out` velozmente e indexadas depois.
