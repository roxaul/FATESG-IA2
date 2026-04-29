# Análise e Previsão de Dados - Casos de COVID-19 em Goiás

Este diretório (Ex3) contém notebooks de experimentação desenvolvidos para a disciplina de Big Data, focados na construção de modelos de regressão e previsão de séries temporais. A base de dados utilizada acompanha a evolução diária dos casos e mortes por COVID-19 (`casos-covid-go.csv`).

---

## 1. `ml-algoritmos-knn-ad.ipynb`

Este notebook demonstra a aplicação de algoritmos clássicos de aprendizado de máquina supervisionado para a tarefa de regressão (tentando prever números contínuos baseados em características históricas).

### Principais etapas:
- **Tratamento de Dados**: Lê a base CSV, filtra exclusivamente as agregações referentes ao Estado de Goiás (`place_type == 'state'` e `state == 'GO'`) e agrupa o número de mortes diárias (`deaths`).
- **Treino e Teste**: Separa os dados em base de treinamento (70%) e teste (30%), utilizando as datas como variável independente e as mortes como variável alvo (dependente).
- **Modelo KNN Regressor**: Treina um modelo focado no algoritmo *K-Nearest Neighbors* (k=4) para prever as mortes em uma data específica no futuro (ex: `2021-11-01`), obtendo também a métrica de acerto (Score).
- **Modelo Random Forest Regressor**: Instancia um modelo focado em *Florestas Aleatórias*, treina com a mesma base e efetua as previsões para servir de termo de comparação da precisão em relação ao KNN.

---

## 2. `ml_prophet.ipynb`

Este notebook foca no uso da biblioteca **Prophet** (criada pelo Facebook/Meta), que é uma ferramenta extremamente poderosa e otimizada unicamente para previsão de dados de séries temporais (dados atrelados à linha do tempo).

### Principais etapas:
- **Análise de Casos Confirmados (Goiás)**: Faz a limpeza e correlação das variáveis da base. Para rodar o Prophet, o código formata o dataset renomeando a coluna de datas para `ds` e a coluna alvo de casos confirmados para `y`. Em seguida, cria uma janela de futuro de 30 dias para a previsão da evolução dos casos da pandemia.
- **Análise de Mortes (Goiânia)**: Realiza uma segunda experimentação, filtrando os dados unicamente para o nível municipal de Goiânia (`city == 'Goiânia'`) e troca a variável alvo para número de óbitos (`deaths`). A partir disso, treina um novo modelo Prophet projetando 60 dias para o futuro e plota o resultado em gráficos.
- *Observação técnica*: Os logs apontam falhas de execução no carregamento do modelo (`AttributeError: stan_backend`). Isso evidencia que será necessário refazer as compatibilidades de versões entre a biblioteca `prophet` e as compilações em C++ no ambiente local (geralmente resolvido pela atualização de pacotes no ambiente).

---

## 3. Base de Dados e Materiais de Apoio

- **`casos-covid-go.csv`**: Tabela principal fornecendo a linha do tempo desde o início da pandemia em 2020 para as diversas cidades do estado.
- **`Aula 22-04-2026.pdf` e `Aula 29-04-2026 - Prophet.pdf`**: Arquivos de apoio com fundamentações teóricas ensinadas nas aulas a respeito dos algoritmos explorados nestes códigos.
