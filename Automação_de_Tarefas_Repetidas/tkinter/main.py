import os
import shutil

def organize_files_by_extension(directory):
    # Verifica se o diretório fornecido existe
    if not os.path.exists(directory):
        print(f"O diretório {directory} não existe.")
        return

    # Percorre os itens no diretório
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Ignora subdiretórios
        if os.path.isdir(item_path):
            continue

        # Extrai a extensão do arquivo e prepara o diretório de destino
        file_extension = item.split('.')[-1].lower()
        destination_dir = os.path.join(directory, file_extension)

        # Cria o diretório de destino, se não existir
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Move o arquivo
        shutil.move(item_path, destination_dir)
        print(f"Movido: {item} -> {destination_dir}/")

# Exemplo de uso
if __name__ == "__main__":
    target_directory = input("Digite o caminho do diretório que deseja organizar: ")
    organize_files_by_extension(target_directory)
