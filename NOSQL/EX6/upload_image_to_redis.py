import os
import redis
import base64

# Conectar ao Redis (assumindo que está rodando na porta padrão do localhost)
r = redis.Redis(host='localhost', port=6379, db=0)

# Caminho absoluto da imagem com base na localização deste script
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "imagens-malucas.jpg")
redis_key = "imagem:exercicio"

try:
    # Ler a imagem e converter para base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Salvar no Redis
    r.set(redis_key, encoded_string)
    
    print(f"Imagem '{image_path}' convertida para base64 e salva no Redis com a chave '{redis_key}'.")
    
    # Para verificar se deu certo, podemos recuperar e mostrar os primeiros 50 caracteres
    recovered_string = r.get(redis_key).decode('utf-8')
    print(f"Primeiros 50 caracteres recuperados do Redis: {recovered_string[:50]}...")

except redis.ConnectionError:
    print("Erro: Não foi possível conectar ao Redis. Certifique-se de que o container está rodando.")
except FileNotFoundError:
    print(f"Erro: O arquivo '{image_path}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
