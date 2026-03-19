import pandas as pd

def exercicio_5():
    print("--- Nível 5: Estrutura Multidimensional (DataFrame) ---")
    
    # Escrevendo a sintaxe do construtor completo do DataFrame com os 5 principais parâmetros
    sintaxe_construtor = """
Sintaxe do construtor do DataFrame do Pandas:
=========================================================
pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=None)
=========================================================

Descrição dos 5 parâmetros principais:
1. data    : Representa os dados que irão compor o DataFrame. Pode receber diferentes tipos de estruturas, como numpy ndarray, dicionários, listas, Series, ou outro DataFrame.
2. index   : Refere-se aos rótulos dos eixos das linhas (índices). Se não for fornecido explicitamente, será utilizado um índice numérico sequencial (RangeIndex) começando em 0.
3. columns : Refere-se aos rótulos dos eixos das colunas. Assim como no index, se não especificado para arrays e listas, adotará inteiros a partir do 0 (no caso de dicionários puxará as chaves do dicionário para definir as colunas).
4. dtype   : Permite forçar um tipo de dado específico em todas as colunas. Caso seja definido como None (ou não especificado), infere os tipos a partir dos dados passados (data).
5. copy    : Parâmetro booleano utilizado para forçar a cópia dos dados de entrada 'data'. 
"""
    
    # Imprimindo a sintaxe construtora
    print(sintaxe_construtor)

if __name__ == "__main__":
    exercicio_5()
