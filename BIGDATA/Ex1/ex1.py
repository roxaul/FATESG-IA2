import kagglehub

# Download latest version
path = kagglehub.dataset_download("claudiodavi/superhero-set")

print("Path to dataset files:", path)