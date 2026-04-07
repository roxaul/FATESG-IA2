import pymongo
from pymongo import MongoClient
import pprint

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "n1_raw_data"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def run_queries():
    print("==========================================")
    print("       ETL MongoDB - Consultas (Etapa 5)")
    print("==========================================\n")

    # ----------------------------------------------------
    # 1. 3 Consultas Simples com Filtros
    # ----------------------------------------------------
    print("--- 3 Consultas Simples ---")
    
    # 1.1 Produções mais recentes (Filme do tipo_id = 1 gravado após 2020)
    print("\n1.1 - Buscar uma produção cinematográfica (tipo=1) lançada em ou após 2020:")
    prod = db.producao_clean.find_one({"tipo_id": 1, "ano": {"$gte": 2020}})
    pprint.pprint(prod)
    
    # 1.2 Qual a pessoa que tem o id_pessoa = 2523 (Exemplo do Json)
    print("\n1.2 - Mostrar o nome da pessoa com id_pessoa 2523:")
    pessoa = db.pessoa_clean.find_one({"id_pessoa": 2523})
    pprint.pprint(pessoa)

    # 1.3 Mostrar um vínculo de equipe em que o papel seja 'Reporter'
    print("\n1.3 - Encontrar uma participação de 'Reporter':")
    equipe_exemplo = db.equipe_clean.find_one({"papel": "Reporter"})
    pprint.pprint(equipe_exemplo)


    # ----------------------------------------------------
    # 2. 2 Agregações
    # ----------------------------------------------------
    print("\n--- 2 Agregações ---")
    
    # 2.1 Contar quantidade total de produções por ano de lançamento
    print("\n2.1 - Quantidade de produções feitas por década (Agrupadas a partir de 2000):")
    pipeline_q21 = [
        {"$match": {"ano": {"$gte": 2000}}},
        {"$bucket": {
            "groupBy": "$ano",
            "boundaries": [2000, 2010, 2020, 2030],
            "default": "Other",
            "output": {"count": {"$sum": 1}}
        }}
    ]
    aggs1 = list(db.producao_clean.aggregate(pipeline_q21))
    pprint.pprint(aggs1)

    # 2.2 Quantidade de participantes por tipos diferentes de papeis mapeados na equipe (top 5 papéis, ignorando Desconhecidos)
    print("\n2.2 - Os 5 papéis mais frequentes na base (sem ser Desconhecido):")
    pipeline_q22 = [
        {"$match": {"papel": {"$ne": "Desconhecido"}}},
        {"$group": {"_id": "$papel", "totalRegistros": {"$sum": 1}}},
        {"$sort": {"totalRegistros": -1}},
        {"$limit": 5}
    ]
    aggs2 = list(db.equipe_clean.aggregate(pipeline_q22))
    for p in aggs2:
        print(f"Papel: {p['_id']} | Quantidade: {p['totalRegistros']}")


    # ----------------------------------------------------
    # 3. 1 Ranking
    # ----------------------------------------------------
    print("\n--- 1 Ranking ---")
    print("\n3.1 - Ranking do Top 5 pessoas com MAIS participações em todas produções:")
    # Aqui fazemos um group em equipe e trazemos o nome da pessoa através de lookup
    pipeline_q31 = [
        {"$group": {"_id": "$id_pessoa", "numero_participacoes": {"$sum": 1}}},
        {"$sort": {"numero_participacoes": -1}},
        {"$limit": 5},
        {
            "$lookup": {
                "from": "pessoa_clean",
                "localField": "_id",
                "foreignField": "id_pessoa",
                "as": "pessoa_dados"
            }
        },
        {"$unwind": "$pessoa_dados"},
        {"$project": {
            "_id": 0,
            "id_pessoa": "$_id",
            "nome": "$pessoa_dados.nome",
            "numero_participacoes": 1
        }}
    ]
    # AllowDiskUse é essencial para group/sort numa collection de 12 milhões!
    ranking = list(db.equipe_clean.aggregate(pipeline_q31, allowDiskUse=True))
    for i, p in enumerate(ranking):
        print(f"{i+1}º Lugar) {p['nome']} - Participou de {p['numero_participacoes']} produções.")


    # ----------------------------------------------------
    # 4. Demonstração de Modelo Escohido (Vantagem)
    # ----------------------------------------------------
    print("\n--- 1 Consulta Expondo o Modelo Escolhido ---")
    print("\n4.1 - Na coleção `producoes_com_participantes`, criamos um array embutido de todos os papéis por filme.")
    print("Vantagem: Caso queiramos listar todos que trabalharam em um filme especifico, evitamos JOIN em app.")
    print("Exemplo buscando participantes do filme que é uma obra Prima das comédias (tentamos buscar pelo titulo aproximado):")
    
    filme = db.producoes_com_participantes.find_one({
        "titulo": {"$regex": "Matrix", "$options": "i"}
    })
    
    if filme:
        print(f"Filme Encontrado: {filme['titulo']} (Lançado em {filme['ano']})")
        print(f"Número de integrantes de equipe catalogados neste json: {len(filme.get('equipe_info', []))}")
        print("Três primeiros integrantes (com seus papéis) armazenados localmente e vinculados no documento principal sem lookup:")
        if 'equipe_info' in filme and len(filme['equipe_info']) > 0:
            for membro in filme['equipe_info'][:3]:
                print(f" - Pessoa ID: {membro['id_pessoa']} | Desempenhou a função de: {membro['papel']}")
    else:
        print("Filme selecionado para a demonstração não foi encontrado.")

if __name__ == "__main__":
    run_queries()
