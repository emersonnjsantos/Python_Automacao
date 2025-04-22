import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def organize():
    directory = filedialog.askdirectory()
    if not directory:
        return
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            continue
        file_extension = item.split('.')[-1].lower()
        destination_dir = os.path.join(directory, file_extension)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        shutil.move(item_path, os.path.join(destination_dir, item))
    
    messagebox.showinfo("Pronto!", "Arquivos organizados com sucesso!")

# Cria a janela
root = tk.Tk()
root.title("Organizador de Arquivos")

# Botão para executar
btn = tk.Button(root, text="Selecionar Pasta e Organizar", command=organize, width=30)
btn.pack(pady=100, padx=100)# tamanho da caixa 

# Inicia a interface
root.mainloop()
