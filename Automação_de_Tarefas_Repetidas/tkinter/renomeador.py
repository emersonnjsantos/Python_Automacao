import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

original_filenames = {}

def escolher_diretorio():
    path = filedialog.askdirectory()
    if path:
        entrada_diretorio.delete(0, tk.END)
        entrada_diretorio.insert(0, path)

def renomear_arquivos():
    diretorio = entrada_diretorio.get()
    tipo_arquivo = entrada_tipo.get()
    prefixo = entrada_prefixo.get()

    if not Path(diretorio).exists():
        messagebox.showerror("Erro", "Diretório inválido.")
        return

    caminho = Path(diretorio)
    arquivos = list(caminho.glob(f'*{tipo_arquivo}'))
    if not arquivos:
        messagebox.showinfo("Nenhum arquivo", f"Nenhum arquivo com '{tipo_arquivo}' encontrado.")
        return

    original_filenames.clear()
    for i, arquivo in enumerate(arquivos, start=1):
        nome_original = arquivo.name
        novo_nome = f"{prefixo}{i}{tipo_arquivo}"
        novo_caminho = caminho / novo_nome

        try:
            arquivo.rename(novo_caminho)
            original_filenames[novo_nome] = nome_original
            status.insert(tk.END, f"✔ {nome_original} → {novo_nome}\n")
        except Exception as e:
            status.insert(tk.END, f"Erro ao renomear {nome_original}: {e}\n")

def desfazer_renomeacao():
    diretorio = entrada_diretorio.get()
    caminho = Path(diretorio)

    if not original_filenames:
        messagebox.showinfo("Nada a desfazer", "Nenhuma renomeação para desfazer.")
        return

    for novo_nome, nome_original in original_filenames.items():
        try:
            caminho_novo = caminho / novo_nome
            caminho_original = caminho / nome_original

            if caminho_novo.exists():
                caminho_novo.rename(caminho_original)
                status.insert(tk.END, f"↩ {novo_nome} → {nome_original}\n")
            else:
                status.insert(tk.END, f"Arquivo {novo_nome} não encontrado.\n")
        except Exception as e:
            status.insert(tk.END, f"Erro ao restaurar {novo_nome}: {e}\n")

    original_filenames.clear()

# GUI Tkinter framework nativo do python
# Criação da janela principal
janela = tk.Tk()
janela.title("Renomeador de Arquivos com Desfazer")
janela.geometry("600x400")

tk.Label(janela, text="Diretório:").pack()
frame_dir = tk.Frame(janela)
frame_dir.pack(fill="x", padx=10)
entrada_diretorio = tk.Entry(frame_dir)
entrada_diretorio.pack(side="left", fill="x", expand=True)
tk.Button(frame_dir, text="📂", command=escolher_diretorio).pack(side="left")

tk.Label(janela, text="Extensão do arquivo (ex: .jpg):").pack(pady=(10, 0))
entrada_tipo = tk.Entry(janela)
entrada_tipo.pack(fill="x", padx=10)

tk.Label(janela, text="Prefixo do novo nome:").pack(pady=(10, 0))
entrada_prefixo = tk.Entry(janela)
entrada_prefixo.pack(fill="x", padx=10)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)
tk.Button(frame_botoes, text="Renomear", command=renomear_arquivos).pack(side="left", padx=10)
tk.Button(frame_botoes, text="Desfazer", command=desfazer_renomeacao).pack(side="left", padx=10)

status = tk.Text(janela, height=10)
status.pack(fill="both", padx=10, pady=10, expand=True)

janela.mainloop()
