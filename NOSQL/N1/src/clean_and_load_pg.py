import json
import os
import time
import psycopg2
from io import StringIO

# Configurações do Banco PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5433"
DB_USER = "postgres"
DB_PASS = "aluno"
DB_NAME = "postgres"  # Usaremos o banco de dados default do postgres

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )

def create_tables():
    print("Criando tabelas no PostgreSQL...")
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DROP TABLE IF EXISTS producoes_com_participantes;
        DROP TABLE IF EXISTS equipe_clean;
        DROP TABLE IF EXISTS pessoa_clean;
        DROP TABLE IF EXISTS producao_clean;
        
        CREATE TABLE producao_clean (
            id_producao INTEGER PRIMARY KEY,
            titulo TEXT,
            ano INTEGER,
            tipo_id INTEGER
        );
        
        CREATE TABLE pessoa_clean (
            id_pessoa INTEGER PRIMARY KEY,
            nome TEXT
        );
        
        CREATE TABLE equipe_clean (
            id_producao INTEGER,
            id_pessoa INTEGER,
            papel TEXT
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tabelas criadas com sucesso!")

def clean_and_load_producao(filepath):
    print("Tratando e carregando dados de Produção...")
    start_time = time.time()
    seen_ids = set()
    buffer = StringIO()
    count = 0
    total_inserted = 0

    conn = get_connection()
    cursor = conn.cursor()

    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if not line.strip(): continue
            try:
                doc = json.loads(line)
            except:
                continue

            try:
                id_producao = int(doc.get("id_producao"))
            except (TypeError, ValueError):
                continue
            
            if id_producao in seen_ids:
                continue
            seen_ids.add(id_producao)

            titulo = str(doc.get("titulo", "")).strip()
            
            try:
                ano = int(doc.get("ano"))
                if not (1800 <= ano <= 2030):
                    ano = None
            except (TypeError, ValueError):
                ano = None
                
            try:
                tipo_id = int(doc.get("tipo_id"))
            except (TypeError, ValueError):
                tipo_id = None

            # CSV format: id_producao,titulo,ano,tipo_id
            # Escapar aspas duplas no titulo
            titulo_escaped = titulo.replace('"', '""')
            ano_str = str(ano) if ano is not None else ""
            tipo_id_str = str(tipo_id) if tipo_id is not None else ""
            
            buffer.write(f'{id_producao},"{titulo_escaped}",{ano_str},{tipo_id_str}\n')
            count += 1

            if count >= 100000:
                buffer.seek(0)
                cursor.copy_expert("COPY producao_clean (id_producao, titulo, ano, tipo_id) FROM STDIN WITH CSV", buffer)
                total_inserted += count
                count = 0
                buffer.seek(0)
                buffer.truncate()
                print(f" -> {total_inserted} produções inseridas...")

    if count > 0:
        buffer.seek(0)
        cursor.copy_expert("COPY producao_clean (id_producao, titulo, ano, tipo_id) FROM STDIN WITH CSV", buffer)
        total_inserted += count

    # Criando índices adicionais se necessário
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_producao_ano ON producao_clean(ano);")
    conn.commit()
    cursor.close()
    conn.close()

    elapsed = time.time() - start_time
    print(f"producao_clean populada! Total inserido: {total_inserted} em {elapsed:.2f}s")


def clean_and_load_pessoa(filepath):
    print("Tratando e carregando dados de Pessoa...")
    start_time = time.time()
    seen_ids = set()
    buffer = StringIO()
    count = 0
    total_inserted = 0

    conn = get_connection()
    cursor = conn.cursor()

    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if not line.strip(): continue
            try:
                doc = json.loads(line)
            except:
                continue

            try:
                id_pessoa = int(doc.get("id_pessoa"))
            except (TypeError, ValueError):
                continue
                
            nome = str(doc.get("nome", "")).strip()
            if not nome:
                continue
            
            if id_pessoa in seen_ids:
                continue
            seen_ids.add(id_pessoa)

            nome_escaped = nome.replace('"', '""')
            buffer.write(f'{id_pessoa},"{nome_escaped}"\n')
            count += 1

            if count >= 100000:
                buffer.seek(0)
                cursor.copy_expert("COPY pessoa_clean (id_pessoa, nome) FROM STDIN WITH CSV", buffer)
                total_inserted += count
                count = 0
                buffer.seek(0)
                buffer.truncate()
                print(f" -> {total_inserted} pessoas inseridas...")

    if count > 0:
        buffer.seek(0)
        cursor.copy_expert("COPY pessoa_clean (id_pessoa, nome) FROM STDIN WITH CSV", buffer)
        total_inserted += count

    conn.commit()
    cursor.close()
    conn.close()

    elapsed = time.time() - start_time
    print(f"pessoa_clean populada! Total inserido: {total_inserted} em {elapsed:.2f}s")


def clean_and_load_equipe(filepath):
    print("Tratando e carregando dados de Equipe...")
    start_time = time.time()
    buffer = StringIO()
    count = 0
    total_inserted = 0

    conn = get_connection()
    cursor = conn.cursor()

    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if not line.strip(): continue
            try:
                doc = json.loads(line)
            except:
                continue

            try:
                id_producao = int(doc.get("id_producao"))
                id_pessoa = int(doc.get("id_pessoa"))
            except (TypeError, ValueError):
                continue

            papel = doc.get("papel")
            if not papel or str(papel).strip() == "" or str(papel) == "\\N":
                papel_clean = "Desconhecido"
            else:
                papel_clean = str(papel).strip()

            papel_escaped = papel_clean.replace('"', '""')
            buffer.write(f'{id_producao},{id_pessoa},"{papel_escaped}"\n')
            count += 1

            if count >= 200000:
                buffer.seek(0)
                cursor.copy_expert("COPY equipe_clean (id_producao, id_pessoa, papel) FROM STDIN WITH CSV", buffer)
                total_inserted += count
                count = 0
                buffer.seek(0)
                buffer.truncate()
                print(f" -> {total_inserted} registros de equipe inseridos...")

    if count > 0:
        buffer.seek(0)
        cursor.copy_expert("COPY equipe_clean (id_producao, id_pessoa, papel) FROM STDIN WITH CSV", buffer)
        total_inserted += count

    # Criando índices para buscas eficientes
    cursor.execute("CREATE INDEX idx_equipe_producao ON equipe_clean(id_producao);")
    cursor.execute("CREATE INDEX idx_equipe_pessoa ON equipe_clean(id_pessoa);")
    conn.commit()
    cursor.close()
    conn.close()

    elapsed = time.time() - start_time
    print(f"equipe_clean populada! Total inserido: {total_inserted} em {elapsed:.2f}s")


if __name__ == "__main__":
    print("====================================")
    print(" ETL PostgreSQL - Tratamento de Dados ")
    print("====================================\n")
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    
    create_tables()
    
    filepath_prod = os.path.join(base_dir, "producao.jsonl")
    if os.path.exists(filepath_prod):
        clean_and_load_producao(filepath_prod)
        
    filepath_pessoa = os.path.join(base_dir, "pessoa.jsonl")
    if os.path.exists(filepath_pessoa):
        clean_and_load_pessoa(filepath_pessoa)
        
    filepath_equipe = os.path.join(base_dir, "equipe.jsonl")
    if os.path.exists(filepath_equipe):
        clean_and_load_equipe(filepath_equipe)
        
    print("\nTratamento finalizado para o PostgreSQL!")
