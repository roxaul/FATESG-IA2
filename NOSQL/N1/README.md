# Trabalho N1 - ETL e Armazenamento NoSQL

## Grupo
-Carlos Henrique
-Felipe Mendonça
-Gustavo de Carvalho
-Lauro Lobo

Professor
- Willgnner de Oliveira Souza

Repositório correspondente ao projeto prático de construção de um pipeline para ingerir, limpar e armazenar a base de dados `BD_Producao_Artistica` de JSONL para MongoDB.

## Descrição do Projeto

O objetivo principal consiste em trabalhar noções de Engenharia de Dados aplicadas num ambiente não estruturado. Convertemos mais de 15 milhões de linhas das bases primárias em documentos colecionáveis para MongoDB.

A estrutura do projeto compreende as seguintes etapas:
- **Etapas 1 e 2**: Entendimento e Ingestão (`/src/ingest.py`) dos arquivos `jsonl` (`/data/`).
- **Etapas 3 e 4**: Tratamento de consistências, tipos e carregamento do modelo definitivo via pipeline Aggregation do banco (`/src/clean_and_load.py`).
- **Etapa 5**: Consultas requeridas (`/src/queries.py`).
- **Etapas 6 e 7**: Documentação textual arquitetural (`/docs/`), Docker-compose e repositório.

## Como Executar

A inicialização e o teste dependem da aplicação do Docker instalada na sua máquina, além do motor em Python.

1. Subir infraestrutura da aplicação:
```bash
cd docker
docker-compose up -d
```
> O Docker trará o servidor do MongoDB na porta 27017, e a interface gráfica do Mongo-Express na porta 8081.

2. Atuando via código (Necessita do interpretador Python e bibliotecas como `pymongo` instaladas globalmente no ambiente virtual):
```bash
# Entrar na pasta root do src:
cd src

# 1. Realizar Ingestão Raw!
python ingest.py

# 2. Iniciar limpeza dos dados brutos e construção das coleções definitivas!
python clean_and_load.py

# 3. Ler o terminal das respostas para validação do resultado de tratamento:
python queries.py
```
