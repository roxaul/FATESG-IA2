class Pilha:
    def __init__(self):
        self.itens = []

    def is_empty(self):
        """Verifica se a pilha está vazia."""
        return len(self.itens) == 0

    def push(self, item):
        """Insere um item no topo da pilha."""
        self.itens.append(item)

    def pop(self):
        """Remove e retorna o item do topo da pilha."""
        if not self.is_empty():
            return self.itens.pop()
        else:
            print("Erro: A pilha está vazia!")
            return None

    def peek(self):
        """Retorna o item do topo da pilha sem removê-lo."""
        if not self.is_empty():
            return self.itens[-1]
        else:
            print("Erro: A pilha está vazia!")
            return None

    def size(self):
        """Retorna o número de itens na pilha."""
        return len(self.itens)

    def __str__(self):
        """Retorna a representação em string da pilha."""
        return str(self.itens)

# Testando a implementação
if __name__ == "__main__":
    print("--- Testando a estrutura de Pilha ---")
    minha_pilha = Pilha()
    
    print(f"Pilha está vazia? {minha_pilha.is_empty()}")
    
    # Inserindo elementos
    minha_pilha.push(10)
    minha_pilha.push(20)
    minha_pilha.push(30)
    print(f"Pilha após inserir 10, 20, 30: {minha_pilha}")
    
    # Verificando tamanho e topo
    print(f"Tamanho da pilha: {minha_pilha.size()}")
    print(f"Elemento no topo (peek): {minha_pilha.peek()}")
    
    # Removendo elementos
    removido = minha_pilha.pop()
    print(f"Elemento removido (pop): {removido}")
    print(f"Pilha após remoção: {minha_pilha}")
    
    # Esvaziando a pilha
    minha_pilha.pop()
    minha_pilha.pop()
    print(f"Pilha após remover todos: {minha_pilha}")
    
    # Tentando remover de uma pilha vazia
    minha_pilha.pop()
