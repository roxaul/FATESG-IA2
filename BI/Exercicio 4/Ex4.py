import pandas as pd

def exercicio_4():
    print("--- Nível 4: Uso de Dicionários e Tratamento de Dados Ausentes (NaN) ---")
    
    # Criando um dicionário original com valores para 'jan' e 'fev'
    dicionario_de_vendas = {'jan': 100, 'fev': 200}
    
    # Definindo a lista de índices que inclui uma chave ausente no dicionário ('mar')
    indices_dos_meses = ['jan', 'fev', 'mar']
    
    # Criando a Series a partir do dicionário passando a lista de índices especificados
    serie_de_vendas = pd.Series(dicionario_de_vendas, index=indices_dos_meses)
    
    # Imprimindo o resultado da Series
    print("Series criada a partir do dicionário com o índice especificado:")
    print(serie_de_vendas)
    
    # Observação sobre o que acontece com o mês de 'mar'
    print("\nObservação sobre o mês de 'mar':")
    print("A chave 'mar' não existia no dicionário original 'dicionario_de_vendas'. "
          "Sendo assim, o Pandas preencheu o valor correspondente a 'mar' com 'NaN' (Not a Number), "
          "que é o marcador padrão do Pandas para demonstrar dados ausentes ou nulos em uma Series que não possui um tipo puramente inteiro/string.")

if __name__ == "__main__":
    exercicio_4()
