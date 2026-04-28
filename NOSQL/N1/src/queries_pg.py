import psycopg2

# Configurações do Banco PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5433"
DB_USER = "postgres"
DB_PASS = "aluno"
DB_NAME = "postgres"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )

def run_queries():
    print("==========================================")
    print("       ETL PostgreSQL - Consultas")
    print("==========================================\n")

    conn = get_connection()
    cursor = conn.cursor()

    # ----------------------------------------------------
    # 1. 3 Consultas Simples com Filtros
    # ----------------------------------------------------
    print("--- 3 Consultas Simples ---")
    
    # 1.1 Produções mais recentes (Filme do tipo_id = 1 gravado após 2020)
    print("\n1.1 - Buscar uma produção cinematográfica (tipo=1) lançada em ou após 2020:")
    cursor.execute("SELECT * FROM producao_clean WHERE tipo_id = 1 AND ano >= 2020 LIMIT 1;")
    prod = cursor.fetchone()
    if prod:
        print(f"{{'id_producao': {prod[0]}, 'titulo': '{prod[1]}', 'ano': {prod[2]}, 'tipo_id': {prod[3]}}}")
    else:
        print("Nenhuma encontrada.")
        
    # 1.2 Qual a pessoa que tem o id_pessoa = 2523
    print("\n1.2 - Mostrar o nome da pessoa com id_pessoa 2523:")
    cursor.execute("SELECT * FROM pessoa_clean WHERE id_pessoa = 2523;")
    pessoa = cursor.fetchone()
    if pessoa:
        print(f"{{'id_pessoa': {pessoa[0]}, 'nome': '{pessoa[1]}' }}")
    else:
        print("Nenhuma pessoa encontrada.")

    # 1.3 Mostrar um vínculo de equipe em que o papel seja 'Reporter'
    print("\n1.3 - Encontrar uma participação de 'Reporter':")
    cursor.execute("SELECT * FROM equipe_clean WHERE papel = 'Reporter' LIMIT 1;")
    equipe_exemplo = cursor.fetchone()
    if equipe_exemplo:
        print(f"{{'id_producao': {equipe_exemplo[0]}, 'id_pessoa': {equipe_exemplo[1]}, 'papel': '{equipe_exemplo[2]}' }}")
    else:
        print("Nenhum reporter encontrado.")

    # ----------------------------------------------------
    # 2. 2 Agregações
    # ----------------------------------------------------
    print("\n--- 2 Agregações ---")
    
    # 2.1 Contar quantidade total de produções por ano de lançamento em décadas
    print("\n2.1 - Quantidade de produções feitas por década (Agrupadas a partir de 2000):")
    # Para simular o bucket:
    query_21 = """
        SELECT FLOOR(ano/10)*10 AS decada, COUNT(*) AS count
        FROM producao_clean 
        WHERE ano >= 2000 AND ano < 2040
        GROUP BY decada
        ORDER BY decada;
    """
    cursor.execute(query_21)
    aggs1 = cursor.fetchall()
    for row in aggs1:
        print(f"{{'_id': {int(row[0])}, 'count': {row[1]} }}")

    # 2.2 Quantidade de participantes por tipos diferentes de papeis mapeados na equipe (top 5 papéis)
    print("\n2.2 - Os 5 papéis mais frequentes na base (sem ser Desconhecido):")
    query_22 = """
        SELECT papel, COUNT(*) as totalRegistros
        FROM equipe_clean 
        WHERE papel != 'Desconhecido'
        GROUP BY papel
        ORDER BY totalRegistros DESC
        LIMIT 5;
    """
    cursor.execute(query_22)
    aggs2 = cursor.fetchall()
    for row in aggs2:
        print(f"Papel: {row[0]} | Quantidade: {row[1]}")

    # ----------------------------------------------------
    # 3. 1 Ranking
    # ----------------------------------------------------
    print("\n--- 1 Ranking ---")
    print("\n3.1 - Ranking do Top 5 pessoas com MAIS participações em todas produções:")
    query_31 = """
        SELECT p.nome, COUNT(e.id_producao) as numero_participacoes
        FROM equipe_clean e
        JOIN pessoa_clean p ON e.id_pessoa = p.id_pessoa
        GROUP BY e.id_pessoa, p.nome
        ORDER BY numero_participacoes DESC
        LIMIT 5;
    """
    cursor.execute(query_31)
    ranking = cursor.fetchall()
    for i, p in enumerate(ranking):
        print(f"{i+1}º Lugar) {p[0]} - Participou de {p[1]} produções.")

    # ----------------------------------------------------
    # 4. Demonstração Relacional (JOIN)
    # ----------------------------------------------------
    print("\n--- 1 Consulta Expondo o Modelo Escolhido ---")
    print("\n4.1 - No modelo Relacional (PostgreSQL), para obter os participantes de um filme, fazemos um JOIN.")
    print("Vantagem: Dados não são duplicados, estrutura rigidamente definida.")
    print("Exemplo buscando participantes do filme que é uma obra Prima das comédias (tentamos buscar pelo titulo aproximado):")
    
    query_41 = """
        SELECT p.id_producao, p.titulo, p.ano, e.id_pessoa, pe.nome, e.papel
        FROM producao_clean p
        JOIN equipe_clean e ON p.id_producao = e.id_producao
        JOIN pessoa_clean pe ON e.id_pessoa = pe.id_pessoa
        WHERE p.titulo ILIKE '%Matrix%'
        LIMIT 10;
    """
    cursor.execute(query_41)
    filme_participantes = cursor.fetchall()
    
    if filme_participantes:
        # Obter dados do filme a partir do primeiro registro retornado
        titulo_filme = filme_participantes[0][1]
        ano_filme = filme_participantes[0][2]
        
        # Como o JOIN traz as linhas por integrante, podemos apenas iterar
        print(f"Filme Encontrado: {titulo_filme} (Lançado em {ano_filme})")
        print(f"Número de integrantes de equipe puxados nesta query limite: {len(filme_participantes)}")
        print("Alguns integrantes (com seus papéis) vinculados via JOIN:")
        
        for membro in filme_participantes[:3]:
            print(f" - Pessoa: {membro[4]} (ID: {membro[3]}) | Desempenhou a função de: {membro[5]}")
    else:
        print("Filme selecionado para a demonstração não foi encontrado.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_queries()
