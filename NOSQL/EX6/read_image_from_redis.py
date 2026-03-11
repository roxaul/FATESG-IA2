import os
import redis
import base64

# Conectar ao Redis
r = redis.Redis(host='localhost', port=6379, db=0)

redis_key = "imagem:exercicio"

# Caminho absoluto para salvar a imagem lida com base na localização deste script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_image_path = os.path.join(script_dir, "ExercicioRedi_lido_do_redis.png")

try:
    # Ler a string base64 do Redis
    encoded_string = r.get(redis_key)
    
    if encoded_string:
        # Decodificar de base64 para bytes
        image_data = base64.b64decode(encoded_string.decode('utf-8'))
        
        # Salvar os bytes como uma imagem
        with open(output_image_path, "wb") as image_file:
            image_file.write(image_data)
            
        print(f"Imagem lida com sucesso do Redis e salva em '{output_image_path}'.")
    else:
        print(f"Chave '{redis_key}' não encontrada no Redis.")

except redis.ConnectionError:
    print("Erro: Não foi possível conectar ao Redis. Certifique-se de que o container está rodando.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
