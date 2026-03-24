import pymongo

# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Selecionar o banco de dados e a coleção
db = client["startup"]
collection = db["funcionarios"]

# Definir a consulta (query) para buscar funcionários do setor "TI"
query = {"setor": "TI"}

# Buscar todos os documentos que correspondem à query
resultados = collection.find(query)

# Exibir os resultados
print("Funcionários do setor de TI:")
for funcionario in resultados:
    print(f"- Nome: {funcionario.get('nome')}, Cargo: {funcionario.get('cargo')}, Salário: R$ {funcionario.get('salario')}")
