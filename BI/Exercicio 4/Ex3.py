import pandas as pd
import numpy as np

def exercicio_3():
    print("--- Nível 3: Manipulação de Índices Personalizados ---")
    
    # Criando um array Numpy com os valores especificados
    array_de_valores = np.array([10, 20, 30, 40])
    
    # Definindo explicitamente a lista de índices personalizados
    indices_personalizados = ['A', 'B', 'C', 'D']
    
    # Criando a Series passando o array e atribuindo os índices definidos
    serie_com_indices_personalizados = pd.Series(array_de_valores, index=indices_personalizados)
    
    # Imprimindo a Series resultante
    print("Series resultante com os índices personalizados ('A', 'B', 'C', 'D'):")
    print(serie_com_indices_personalizados)

if __name__ == "__main__":
    exercicio_3()
