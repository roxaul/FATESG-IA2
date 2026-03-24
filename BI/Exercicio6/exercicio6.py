import pandas as pd
import os

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # Tratamento caso o arquivo chame "salarios_profs.csv" ou "salario_prof.csv"
    arquivo_entrada = os.path.join(dir_path, 'salarios_profs.csv')
    if not os.path.exists(arquivo_entrada):
        arquivo_entrada = os.path.join(dir_path, 'salario_prof.csv')

    # Lê o arquivo CSV ignorando a coluna "Posição" (índice 2) utilizando usecols=[0, 1, 3]
    df = pd.read_csv(arquivo_entrada, sep=';', encoding='latin-1')
    
    # Renomear as colunas (pois a posição foi removida da leitura)
    df.columns = ['UF', 'Salario', 'Regiao']
    
    # Limpa possíveis espaços em branco extras dos valores de UF e Região
    df['UF'] = df['UF'].str.strip()
    df['Regiao'] = df['Regiao'].str.strip()

    # Formata o salário para float
    df['Salario'] = df['Salario'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

    print("------ RESULTADOS ------\n")

    # - O estado com menor salário
    estado_menor = df.loc[df['Salario'].idxmin()]
    print(f"1. Estado com menor salário: {estado_menor['UF']} (R$ {estado_menor['Salario']:.2f})")

    # - O estado com o maior salário
    estado_maior = df.loc[df['Salario'].idxmax()]
    print(f"2. Estado com maior salário: {estado_maior['UF']} (R$ {estado_maior['Salario']:.2f})")

    # - Mostrar a média salárial entre todos os estados
    media_todos = df['Salario'].mean()
    print(f"3. Média salarial de todos os estados: R$ {media_todos:.2f}\n")

    print("--- DADOS POR REGIÃO ---\n")
    # Agrupamento por Região
    grupo_regiao = df.groupby('Regiao')['Salario']

    # - Mostrar a media salárial entre todos os estados por região
    print("4. Média Salarial por Região:")
    print(grupo_regiao.mean().apply(lambda x: f"R$ {x:.2f}"))

    # - Mostrar o maior salário por região
    print("\n5. Maior Salário por Região:")
    print(grupo_regiao.max().apply(lambda x: f"R$ {x:.2f}"))

    # - Mostrar o menor salário por região
    print("\n6. Menor Salário por Região:")
    print(grupo_regiao.min().apply(lambda x: f"R$ {x:.2f}"))

    # - Mostrar a região com maior e menor média salarial
    medias_por_regiao = grupo_regiao.mean()
    regiao_maior_media = medias_por_regiao.idxmax()
    regiao_menor_media = medias_por_regiao.idxmin()
    
    print(f"\n7. Região com MAIOR média salarial: {regiao_maior_media} (R$ {medias_por_regiao[regiao_maior_media]:.2f})")
    print(f"8. Região com MENOR média salarial: {regiao_menor_media} (R$ {medias_por_regiao[regiao_menor_media]:.2f})")


if __name__ == "__main__":
    main()
