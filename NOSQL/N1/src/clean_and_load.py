import pymongo
from pymongo import MongoClient

# Configurações do Banco
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "n1_raw_data"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def clear_existing_collections():
    print("Iniciando limpeza de colecoes antigas limpas/tratadas, se existirem...")
    db.producao_clean.drop()
    db.pessoa_clean.drop()
    db.equipe_clean.drop()
    db.producoes_com_participantes.drop()

def clean_producao():
    print("Tratando dados de Producao...")
    pipeline = [
        {
            "$project": {
                "id_producao": { "$toInt": "$id_producao" },
                "titulo": { "$trim": { "input": "$titulo" } },
                "ano": {
                    "$convert": {
                        "input": "$ano",
                        "to": "int",
                        "onError": None,
                        "onNull": None
                    }
                },
                "tipo_id": { "$toInt": "$tipo_id" }
            }
        },
        {
            "$match": {
                "id_producao": { "$ne": None },
                "$or": [
                    { "ano": { "$gte": 1800, "$lte": 2030 } },
                    { "ano": None }
                ]
            }
        },
        {
            "$group": {
                "_id": "$id_producao",
                "id_producao": { "$first": "$id_producao" },
                "titulo": { "$first": "$titulo" },
                "ano": { "$first": "$ano" },
                "tipo_id": { "$first": "$tipo_id" }
            }
        },
        { "$project": { "_id": 0 } },
        { "$out": "producao_clean" }
    ]
    db.raw_producao.aggregate(pipeline, allowDiskUse=True)
    db.producao_clean.create_index("id_producao", unique=True)
    print("producao_clean criada e indexada!")

def clean_pessoa():
    print("Tratando dados de Pessoa e removendo duplicados...")
    pipeline = [
        {
            "$project": {
                "id_pessoa": { "$toInt": "$id_pessoa" },
                "nome": { "$trim": { "input": "$nome" } }
            }
        },
        {
            "$match": {
                "id_pessoa": { "$ne": None },
                "nome": { "$ne": "", "$ne": None }
            }
        },
        {
            "$group": {
                "_id": "$id_pessoa",
                "id_pessoa": { "$first": "$id_pessoa" },
                "nome": { "$first": "$nome" }
            }
        },
        { "$project": { "_id": 0 } },
        { "$out": "pessoa_clean" }
    ]
    db.raw_pessoa.aggregate(pipeline, allowDiskUse=True)
    db.pessoa_clean.create_index("id_pessoa", unique=True)
    print("pessoa_clean criada e indexada!")

def clean_equipe():
    print("Tratando dados de Equipe...")
    # Regras:
    # - cast de ids numéricos
    # - campos vazios e nulos para papel viram "Desconhecido"
    # - remover ids mal formatados ou sem correspondência parcial
    pipeline = [
        {
            "$project": {
                "id_producao": { "$toInt": "$id_producao" },
                "id_pessoa": { "$toInt": "$id_pessoa" },
                "papel": {
                    "$cond": {
                        "if": { "$or": [{ "$eq": ["$papel", None] }, { "$eq": ["$papel", ""] }, { "$eq": ["$papel", "\\N"] }] },
                        "then": "Desconhecido",
                        "else": { "$trim": { "input": "$papel" } }
                    }
                }
            }
        },
        {
            "$match": {
                "id_producao": { "$ne": None },
                "id_pessoa": { "$ne": None }
            }
        },
        { "$out": "equipe_clean" }
    ]
    db.raw_equipe.aggregate(pipeline)
    
    # Criar índices para buscas eficientes
    db.equipe_clean.create_index([("id_producao", 1)])
    db.equipe_clean.create_index([("id_pessoa", 1)])
    print("equipe_clean criada e indexada!")

def build_embedded_collection():
    print("Montando colecao aninhada 'producoes_com_participantes' (Essa etapa pode demorar alguns minutos)...")
    # Agrupamos as equipes por produção, juntando também os dados da pessoa
    pipeline = [
        # Iniciar da produção clean
        {
            "$lookup": {
                "from": "equipe_clean",
                "localField": "id_producao",
                "foreignField": "id_producao",
                "as": "equipe_info"
            }
        },
        {
            "$out": "producoes_com_participantes"
        }
    ]
    
    db.producao_clean.aggregate(pipeline, allowDiskUse=True)
    db.producoes_com_participantes.create_index("ano")
    print("producoes_com_participantes montada com sucesso!")

if __name__ == "__main__":
    print("====================================")
    print("  ETL MongoDB - Tratamento de Dados ")
    print("====================================\n")
    clear_existing_collections()
    clean_producao()
    clean_pessoa()
    clean_equipe()
    build_embedded_collection()
    print("\nTratamento finalizado!")
