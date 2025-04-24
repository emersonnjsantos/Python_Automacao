import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import smtplib
import email
from email.message import EmailMessage


def selecionar_planilha():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
    if caminho:
        entrada_planilha.delete(0, tk.END)
        entrada_planilha.insert(0, caminho)

def selecionar_pdf():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho:
        entrada_pdf.delete(0, tk.END)
        entrada_pdf.insert(0, caminho)

def enviar_emails():
    try:
        planilha = entrada_planilha.get()
        anexo = entrada_pdf.get()
        email_remetente = entrada_email.get()
        senha = entrada_senha.get()

        if not all([planilha, anexo, email_remetente, senha]):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
            return

        dados = pd.read_excel(planilha)

        for _, linha in dados.iterrows():
            msg = EmailMessage()
            msg['Subject'] = linha['assunto']
            msg['From'] = email_remetente
            msg['To'] = linha['email']
            msg.set_content(linha['mensagem'])

            with open(anexo, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(anexo)
                msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_remetente, senha)
                smtp.send_message(msg)

        messagebox.showinfo("Sucesso", "Todos os e-mails foram enviados com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# ========== INTERFACE GRÁFICA ==========
janela = tk.Tk()
janela.title("Envio Automático de E-mails")
janela.geometry("500x370")
janela.resizable(False, False)

# Arquivo Excel
tk.Label(janela, text="Planilha Excel (.xlsx):").pack(anchor='w', padx=10, pady=(10,0))
entrada_planilha = tk.Entry(janela, width=60)
entrada_planilha.pack(padx=10)
tk.Button(janela, text="Selecionar Arquivo", command=selecionar_planilha).pack(padx=10, pady=5)

# PDF Anexo
tk.Label(janela, text="Arquivo PDF para anexar:").pack(anchor='w', padx=10, pady=(10,0))
entrada_pdf = tk.Entry(janela, width=60)
entrada_pdf.pack(padx=10)
tk.Button(janela, text="Selecionar PDF", command=selecionar_pdf).pack(padx=10, pady=5)

# E-mail remetente
tk.Label(janela, text="E-mail do remetente:").pack(anchor='w', padx=10, pady=(10,0))
entrada_email = tk.Entry(janela, width=60)
entrada_email.pack(padx=10)

# Senha do e-mail
tk.Label(janela, text="Senha do e-mail:").pack(anchor='w', padx=10, pady=(10,0))
entrada_senha = tk.Entry(janela, width=60, show="*")
entrada_senha.pack(padx=10)

# Explicação da senha
tk.Label(janela, text="(Se você usa Gmail com verificação em duas etapas, insira aqui a senha de app)", fg="gray").pack(anchor='w', padx=10, pady=(0,10))

# Botão enviar
tk.Button(janela, text="Enviar E-mails", command=enviar_emails, bg="blue", fg="white", height=3).pack(pady=10)

janela.mainloop()
