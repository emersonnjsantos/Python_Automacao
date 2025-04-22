import os
import shutil

# Define o diretório a ser organizado
directory = "D:/"  # Substitua pelo caminho desejado

# Percorre cada arquivo no diretório
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        # Extrai a extensão do arquivo e cria o nome do novo diretório
        file_extension = filename.split('.')[-1]
        new_directory = os.path.join(directory, file_extension)

        # Cria o diretório se não existir
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

        # Move o arquivo para o novo diretório
        shutil.move(os.path.join(directory, filename), os.path.join(new_directory, filename))
