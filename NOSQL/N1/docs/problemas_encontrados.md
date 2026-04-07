# Problemas Encontrados nos Dados Brutos

Durante a exploração da base de dados originada da conversão dos arquivos Textos/Jsonl (Base de Produção Artística do Brasil), alguns gargalos de dados sujos foram identificados e mapeados para tratamento no momento do ETL.

## 1. Tipos de Dados Incorretos
Arquivos JSONL não tem schema. Constatamos:
- `ano` chegando como *String* em `producao.jsonl`.
- `id_producao` e `id_pessoa` tipados no MongoDB muitas vezes como *String* devido ao parse padrão de alguns dados mal modelados.

**Tratamento:** O casting forçado foi adotado (`$toInt`).

## 2. Inconsistência nos Anos
Alguns registros de produções traziam anos absurdos, ou valores representados pela string nula literal do dump do sistema anterior (`\N`), gerando anos do tipo nulo ou textos puros incalculáveis.

**Tratamento:** Valores em strings que não correspondam à inteiros viraram `null` no `$convert`, e criamos um `$match` delimitando apenas anos com sentido (`gte 1800` e `lte 2030`) e anos não informados explícitamente (`null`).

## 3. Duplicação de Chaves
Uma falha detectada com gravidade foi a presença de chaves primárias duplicadas nos datasets mestres.
A tentativa de construir um índice único `unique=True` para `pessoa_clean` falhou ao revelar duplicidade no registro `{ id_pessoa: 86414 }`.

**Tratamento:** Introduzimos na etapa `clean` uma pipeline de `$group`, que desconsidera os registros subjacentes idênticos, garantindo a unicidade que deveríamos esperar em um banco de dados sadio.

## 4. Campos Nulos ou Vazios (Papel)
Na coleção de equipe, o tipo de trabalho desenvolvido por alguém (`papel`) frequentemente aparece vazio `""`, `null` ou preenchido pelas literais `\N`.

**Tratamento:** Atribuímos um comando de condição `$cond` atribuindo todos estes casos irregulares para a string `"Desconhecido"`, assim a interface gráfica poderia lidar consistentemente.
