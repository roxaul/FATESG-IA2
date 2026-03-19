import psycopg2

try:
    conn = psycopg2.connect(
        dbname='dbextracaodados',
        user='postgres',
        password='aluno',
        host='localhost',
        port='5433'
    )
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cur.fetchall()
    print("Database Connection Successful!")
    print("Tables found:")
    for t in tables:
        print(f"- {t[0]}")
    cur.close()
    conn.close()
except Exception as e:
    import traceback
    print("Connection Exception Type:", type(e))
    try:
        print(e.pgerror)
    except:
        pass
    print("Underlying Exception:", repr(e))
