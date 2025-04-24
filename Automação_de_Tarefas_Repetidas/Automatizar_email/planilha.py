import pandas as pd
import os

# Criar diretório de anexos
os.makedirs("anexos", exist_ok=True)

# Criar arquivos PDF falsos para exemplo
with open("anexos/relatorio_joao.pdf", "wb") as f:
    f.write(b"%PDF-1.4 exemplo pdf joao\n%%EOF")

with open("anexos/relatorio_maria.pdf", "wb") as f:
    f.write(b"%PDF-1.4 exemplo pdf maria\n%%EOF")

# Dados de exemplo
dados = {
    "nome": ["João Silva", "Maria Lima"],
    "email": ["joao@email.com", "maria@email.com"],
    "assunto": ["Relatório Mensal", "Relatório Mensal"],
    "mensagem": [
        "Olá João, segue seu relatório.",
        "Olá Maria, veja o relatório em anexo."
    ],
    "anexo": [
        "anexos/relatorio_joao.pdf",
        "anexos/relatorio_maria.pdf"
    ]
}

df = pd.DataFrame(dados)
df.to_excel("emails.xlsx", index=False)

print("📁 Planilha criada: emails.xlsx")
