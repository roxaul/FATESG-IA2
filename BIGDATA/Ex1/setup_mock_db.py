import psycopg2

try:
    conn = psycopg2.connect(dbname='dbextracaodados', user='postgres', password='aluno', host='localhost', port='5433')
    conn.autocommit = True
    cur = conn.cursor()

    print("Criando tabela categoria...")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria SERIAL PRIMARY KEY,
            nome_categoria VARCHAR(255) NOT NULL
        );
    ''')

    print("Adicionando coluna id_categoria na tabela produtos...")
    try:
        cur.execute('''
            ALTER TABLE produtos 
            ADD COLUMN IF NOT EXISTS id_categoria INT;
        ''')
    except Exception as e:
        print("Aviso na adição da coluna:", e)

    print("Adicionando chave estrangeira...")
    try:
        cur.execute('''
            ALTER TABLE produtos 
            ADD CONSTRAINT fk_categoria 
            FOREIGN KEY (id_categoria) 
            REFERENCES categoria(id_categoria);
        ''')
    except psycopg2.errors.DuplicateObject:
        print("Aviso: Chave estrangeira já existe.")
    except Exception as e:
        print("Aviso na adição da chave estrangeira:", e)

    print("Limpando dados antigos (opcional para evitar duplicação em testes)...")
    cur.execute('TRUNCATE TABLE produtos, categoria RESTART IDENTITY CASCADE;')

    print("Inserindo dados mock em categoria...")
    cur.execute('''
        INSERT INTO categoria (nome_categoria) VALUES 
        ('Eletrônicos'),
        ('Móveis'),
        ('Roupas')
        RETURNING id_categoria;
    ''')
    categorias = cur.fetchall()

    if len(categorias) >= 3:
        cat_eletro = categorias[0][0]
        cat_moveis = categorias[1][0]
        cat_roupas = categorias[2][0]

        print("Inserindo dados mock em produtos...")
        cur.execute('''
            INSERT INTO produtos (id_produto, doc_produto, preco_produto, id_categoria) VALUES 
            (1, 'Smartphone Galaxy', 3000, %s),
            (2, 'Notebook Dell', 5000, %s),
            (3, 'Cadeira Ergonomica', 800, %s),
            (4, 'Mesa de Escritorio', 1200, %s),
            (5, 'Camisa Polo V', 150, %s);
        ''', (cat_eletro, cat_eletro, cat_moveis, cat_moveis, cat_roupas))
        
    print("Dataset mock criado com sucesso!")
    
    cur.execute('SELECT * FROM produtos;')
    print("Produtos:", cur.fetchall())

    cur.close()
    conn.close()
except Exception as e:
    print("Erro durante a execução:", e)
