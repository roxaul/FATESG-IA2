import pandas as pd
import os

def main():
    # Obtém o diretório atual do script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Define os caminhos dos arquivos de entrada e saída
    arquivo_entrada = os.path.join(dir_path, 'teste.csv')
    arquivo_saida = os.path.join(dir_path, 'Exercicio CSV.csv')

    # Lê o arquivo CSV usando pandas
    df = pd.read_csv(arquivo_entrada)
    
    dfloc=df.loc[:,'Nome']
    print (dfloc)
    
    df=df.rename(columns={'Nome':'Colaborador(a)'})
    print (df)


    dfmin=df.loc[df['Idade']==df['Idade'].min()]
    print (dfmin)

    dfmax=df.loc[df['Idade']==df['Idade'].max()]
    print (dfmax)

    # Remove '$' e ',', em seguida converte para numérico
    df['Salario'] = df['Salario'].replace(r'[\$,]', '', regex=True).astype(float)
    dfmedia = df['Salario'].mean()

    dfsalmin=df.loc[df['Salario']==df['Salario'].min()]
    print (dfmin)

    dfsalmax=df.loc[df['Salario']==df['Salario'].max()]
    print (dfmax)

    print("Média Salarial: R$", dfmedia)

    df.to_csv(arquivo_saida, index=False)

    print("Arquivo lido e salvo com sucesso usando pandas em:", arquivo_saida)
if __name__ == "__main__":
    main()
