import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
from operator import itemgetter

# Configurar selenium-stealth
try:
    from selenium_stealth import stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("selenium-stealth não instalado. Instale com 'pip install selenium-stealth'.")

# Função para buscar produtos
def search_products(search_term, url, max_products=10, log_widget=None):
    driver = None
    try:
        # Configurar o ChromeDriver
        caminho_driver = "drivers/chromedriver.exe"  # Ajuste o caminho se necessário
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(caminho_driver), options=options)

        # Aplicar stealth
        if STEALTH_AVAILABLE:
            stealth(driver,
                    languages=["pt-BR", "pt"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True)

        # Log
        if log_widget:
            log_widget.insert(tk.END, f"Buscando {search_term}...\n")
            log_widget.see(tk.END)

        driver.get(url)
        time.sleep(3)

        # Verifica se a página carregou
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
        except Exception as e:
            if log_widget:
                log_widget.insert(tk.END, f"Erro ao carregar a página para '{search_term}': {e}\n")
            return []

        # Insere o termo de busca
        try:
            search_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, 'cb1-edit'))
            )
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.ENTER)
            time.sleep(7)
        except Exception as e:
            if log_widget:
                log_widget.insert(tk.END, f"Erro ao buscar '{search_term}': {e}. Possível CAPTCHA.\n")
            return []

        # Simular rolagem
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extrair produtos
        products = []
        try:
            product_elements = WebDriverWait(driver, 20).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.ui-search-result__wrapper, li.ui-search-layout__item'))
            )
            if log_widget:
                log_widget.insert(tk.END, f"Total de itens encontrados para '{search_term}': {len(product_elements)}\n")
            
            for index, item in enumerate(product_elements[:max_products]):
                try:
                    name = ""
                    try:
                        img_element = item.find_element(By.CSS_SELECTOR, 'img.poly-component__picture')
                        name = img_element.get_attribute('title').strip()
                        if not name or len(name) < 10:
                            name = ""
                    except:
                        for name_selector in [
                            'span.ui-search-item__title',
                            'h2.ui-search-item__title',
                            'div.ui-search-item__title',
                            'a.poly-component__title > span',
                            'span.poly-component__title'
                        ]:
                            try:
                                name_elements = item.find_elements(By.CSS_SELECTOR, name_selector)
                                for elem in name_elements:
                                    text = elem.text.strip()
                                    if text and len(text) > 10 and 'R$' not in text and 'Avaliação' not in text:
                                        name = text
                                        break
                                if name:
                                    break
                            except:
                                continue
                    if not name and log_widget:
                        log_widget.insert(tk.END, f"Erro ao extrair nome do produto para item {index}\n")

                    price = 0.0
                    for price_selector in [
                        'span.andes-money-amount__fraction',
                        'span.andes-money-amount',
                        'span.price-tag-fraction',
                        'span.ui-search-price__part'
                    ]:
                        try:
                            price_element = item.find_element(By.CSS_SELECTOR, price_selector)
                            price_text = price_element.text.replace('.', '').replace(',', '.').replace('R$', '').strip()
                            price = float(price_text) if price_text else 0.0
                            break
                        except:
                            continue
                    if price == 0.0 and log_widget:
                        log_widget.insert(tk.END, f"Erro ao extrair preço do produto para item {index}\n")

                    link = ""
                    for link_selector in [
                        'a.poly-component__title',
                        'a.ui-search-link',
                        'a.ui-search-link__title-card',
                        'a.ui-search-result__link',
                        'a[href*="produto.mercadolivre.com.br"]'
                    ]:
                        try:
                            link = item.find_element(By.CSS_SELECTOR, link_selector).get_attribute('href')
                            break
                        except:
                            continue
                    if not link and log_widget:
                        log_widget.insert(tk.END, f"Erro ao extrair link do produto para item {index}\n")

                    if name or price > 0 or link:
                        products.append({
                            'name': name if name else "Nome não encontrado",
                            'price': price if price > 0 else None,
                            'link': link if link else None
                        })
                        if log_widget:
                            log_widget.insert(tk.END, f"Produto extraído: {name if name else 'Nome não encontrado'}, Preço: {price if price > 0 else 'Não encontrado'}, Link: {link if link else 'Não encontrado'}\n")
                    else:
                        if log_widget:
                            log_widget.insert(tk.END, f"Produto ignorado para item {index} (nome: {name}, preço: {price}, link: {link})\n")
                except Exception as e:
                    if log_widget:
                        log_widget.insert(tk.END, f"Erro ao extrair dados do produto {index}: {e}\n")
        except Exception as e:
            if log_widget:
                log_widget.insert(tk.END, f"Erro ao extrair produtos: {e}\n")
        
        return products
    finally:
        if driver:
            driver.quit()

# Função para salvar em CSV
def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'link'])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

# Função para gerar nome de arquivo incremental
def get_unique_csv_filename(folder):
    base_name = "arquivo"
    index = 1
    while True:
        filename = os.path.join(folder, f"{base_name}_{index}.csv")
        if not os.path.exists(filename):
            return filename
        index += 1

# Interface Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Busca de Produtos")
        self.root.geometry("600x400")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="URL do site:").pack(anchor="w")
        self.url_entry = tk.Entry(frame, width=50)
        self.url_entry.insert(0, "https://www.mercadolivre.com.br")
        self.url_entry.pack(fill=tk.X, pady=5)

        tk.Label(frame, text="Pasta para salvar o CSV:").pack(anchor="w")
        self.folder_entry = tk.Entry(frame, width=50)
        self.folder_entry.pack(fill=tk.X, pady=5)
        tk.Button(frame, text="Escolher pasta", command=self.choose_folder).pack(anchor="w", pady=5)

        tk.Button(frame, text="Iniciar busca", command=self.start_search).pack(pady=10)

        tk.Label(frame, text="Log:").pack(anchor="w")
        self.log_text = tk.Text(frame, height=10, width=60)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_text.config(state=tk.NORMAL)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def start_search(self):
        url = self.url_entry.get().strip()
        folder = self.folder_entry.get().strip()
        
        if not url:
            messagebox.showerror("Erro", "Por favor, insira o URL do site.")
            return
        if not folder:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta para salvar o CSV.")
            return

        self.log_text.delete(1.0, tk.END)

        search_terms = [
            'notebook', 'laptop', 'ultrabook', 'computador portátil',
            'celular', 'smartphone', 'telefone', 'celular 5G'
        ]
        all_products = []

        for term in search_terms:
            products = search_products(term, url, max_products=10, log_widget=self.log_text)
            all_products.extend(products)
            self.root.update()
            time.sleep(5)

        all_products = sorted([p for p in all_products if p['price'] is not None], key=itemgetter('price'))

        if all_products:
            csv_filename = get_unique_csv_filename(folder)
            save_to_csv(all_products, csv_filename)
            self.log_text.insert(tk.END, f"Resultados salvos em '{csv_filename}'\n")
        else:
            self.log_text.insert(tk.END, "Nenhum produto encontrado.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
