import psycopg2

try:
    conn = psycopg2.connect(dbname='dbextracaodados', user='postgres', password='aluno', host='localhost', port='5433')
    cur = conn.cursor()
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'produtos';")
    print(cur.fetchall())
    cur.close()
    conn.close()
except Exception as e:
    print(e)
