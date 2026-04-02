import pandas as pd
from pymongo import MongoClient

def main():
    # 1. Configurar a string de conexão do nosso banco no Docker
    uri = "mongodb://admin:admin@127.0.0.1:27017/?authSource=admin"
    
    # 2. Conectar ao MongoDB
    print("Conectando ao banco MongoDB local...")
    client = MongoClient(uri)
    
    # Selecionar o banco de dados e a coleção
    # NOTA: Estou assumindo que no Compass você criará o banco 'ProjetoBI' e a coleção 'vendas'
    db = client['ProjetoBI']
    collection = db['vendas']
    
    # 3. Buscar os dados no MongoDB
    # Trazendo todos os documentos. Omitimos a coluna '_id' nativa do Mongo para o DF ficar mais limpo.
    dados = list(collection.find({}, {'_id': 0}))
    
    if len(dados) == 0:
        print("Nenhum dado encontrado! Verifique se você fez o import do CSV corretamente passo a passo no Compass.")
        return

    # 4. Carregar os dados num DataFrame do Pandas para análise
    df = pd.DataFrame(dados)
    
    # 5. Exibir 5 amostras dos dados utilizando Pandas, conforme pedido
    print("\n--- 5 Amostras dos Dados Inseridos (DataFrame Pandas) ---")
    print(df.head(5))

if __name__ == "__main__":
    main()
