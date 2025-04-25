from fpdf import FPDF
from datetime import datetime
import uuid

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'FATURA', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 8, 'Minha Empresa S.A.', 0, 1, 'L')
        self.cell(0, 8, 'Rua Exemplo, 123, São Paulo, SP', 0, 1, 'L')
        self.cell(0, 8, 'CNPJ: 12.345.678/0001-99', 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_invoice(client_data, invoice_items, output_path):
    pdf = PDF()
    pdf.add_page()
    
    # Informações do cliente
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Dados do Cliente', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    for key, value in client_data.items():
        pdf.cell(0, 8, f'{key}: {value}', 0, 1)
    pdf.ln(10)
    
    # Informações da fatura
    invoice_number = str(uuid.uuid4())[:8]
    invoice_date = datetime.now().strftime('%d/%m/%Y')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Fatura #{invoice_number} - Data: {invoice_date}', 0, 1, 'L')
    pdf.ln(10)
    
    # Itens da fatura
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(100, 10, 'Descrição', 1, 0)
    pdf.cell(40, 10, 'Quantidade', 1, 0)
    pdf.cell(50, 10, 'Valor (R$)', 1, 1)
    
    pdf.set_font('Arial', '', 10)
    total = 0
    for item in invoice_items:
        pdf.cell(100, 10, item['description'], 1, 0)
        pdf.cell(40, 10, str(item['quantity']), 1, 0)
        item_total = item['price'] * item['quantity']
        pdf.cell(50, 10, f'{item_total:.2f}', 1, 1)
        total += item_total
    
    # Total
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(140, 10, 'Total', 1, 0)
    pdf.cell(50, 10, f'R$ {total:.2f}', 1, 1)
    
    pdf.output(output_path)

# Exemplo de uso
client_data = {
    'Nome': 'João Silva',
    'CPF': '123.456.789-00',
    'Endereço': 'Rua Cliente, 456, São Paulo, SP',
    'Email': 'joao.silva@email.com'
}

invoice_items = [
    {'description': 'Serviço A - Assinatura Mensal', 'quantity': 1, 'price': 100.00},
    {'description': 'Serviço B - Uso Adicional', 'quantity': 2, 'price': 75.00}
]

create_invoice(client_data, invoice_items, 'invoice.pdf')