import json
import pymongo
from pymongo import MongoClient
import os
import time

# Configuração
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "n1_raw_data" # Pode ser alterado conforme desejado
BATCH_SIZE = 25000 # Tamanho do lote otimizado para lidar com arquivos maiores

# Mapeamento de arquivos para coleções
FILES_TO_COLLECTIONS = {
    "producao.jsonl": "raw_producao",
    "pessoa.jsonl": "raw_pessoa",
    "equipe.jsonl": "raw_equipe"
}

def ingest_jsonl(filepath, collection):
    print(f"Iniciando ingestão de '{os.path.basename(filepath)}' para a coleção '{collection.name}'...")
    start_time = time.time()
    batch = []
    total_inserted = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            
            try:
                doc = json.loads(line)
                batch.append(doc)
            except json.JSONDecodeError:
                print(f"Aviso: Erro ao decodificar JSON na linha {i}. Ignorando.")
                continue
            
            if len(batch) >= BATCH_SIZE:
                collection.insert_many(batch)
                total_inserted += len(batch)
                batch = []
                print(f" -> {total_inserted} documentos inseridos até agora...")
                
        # Inserir os documentos restantes no lote
        if batch:
            collection.insert_many(batch)
            total_inserted += len(batch)
            
    elapsed_time = time.time() - start_time
    print(f"Ingestão de '{collection.name}' concluída! Total inserido: {total_inserted} em {elapsed_time:.2f} segundos.\n")

if __name__ == "__main__":
    print("Conectando ao MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # Garantir que as coleções existam explicitamente ou apagar os dados antigos se a ideia for re-ingestar
    # Neste caso vamos manter o comportamento padrão de adicionar
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    
    for filename, col_name in FILES_TO_COLLECTIONS.items():
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            collection = db[col_name]
            ingest_jsonl(filepath, collection)
        else:
            print(f"Aviso: Arquivo não encontrado: {filepath}\n")
            
    print("Processo de ingestão de todos os arquivos finalizado!")
