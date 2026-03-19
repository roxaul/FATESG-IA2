import pandas as pd

def exercicio_2():
    print("--- Nível 2: Criação de Series a partir de Listas ---")
    
    # Criando uma lista com nomes de cinco frutas (variável com nome explicativo)
    lista_de_frutas = ['Maçã', 'Banana', 'Manga', 'Morango', 'Uva']
    
    # Convertendo a lista em uma Series do Pandas
    # O Python/Pandas atribuirá os índices numéricos automáticos de 0 a 4
    serie_das_frutas = pd.Series(lista_de_frutas)
    
    # Imprimindo a Series resultante
    print("Series criada a partir da lista de frutas:")
    print(serie_das_frutas)

if __name__ == "__main__":
    exercicio_2()
