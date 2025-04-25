from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from operator import itemgetter

# Configurar o ChromeDriver
try:
    from selenium_stealth import stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("selenium-stealth não instalado. Instale com 'pip install selenium-stealth' para evitar detecção de bots.")

caminho_driver = "drivers/chromedriver.exe"  # Certifique-se de que o caminho está correto
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# Remova o comentário abaixo para rodar em modo headless
# options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(caminho_driver), options=options)

# Aplicar stealth, se disponível
if STEALTH_AVAILABLE:
    stealth(driver,
            languages=["pt-BR", "pt"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

# Função para buscar produtos
def search_products(search_term, url, max_products=10):
    driver.get(url)
    time.sleep(3)  # Aguarda o carregamento inicial

    # Verifica se a página carregou corretamente
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
    except Exception as e:
        print(f"Erro ao carregar a página inicial para '{search_term}': {e}")
        return []

    # Insere o termo de busca no campo de pesquisa
    try:
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'cb1-edit'))
        )
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.ENTER)
        time.sleep(7)  # Aguarda os resultados
    except Exception as e:
        print(f"Erro ao buscar '{search_term}': {e}. Possível CAPTCHA ou bloqueio.")
        return []

    # Simular rolagem para carregar mais produtos
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
        # Seletor para itens de resultado
        product_elements = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.ui-search-result__wrapper, li.ui-search-layout__item'))
        )
        print(f"Total de itens encontrados para '{search_term}': {len(product_elements)}")

        for index, item in enumerate(product_elements[:max_products]):
            try:
                # Logar HTML do item para depuração (apenas para o primeiro item)
                if index == 0:
                    print(f"HTML do primeiro item: {item.get_attribute('outerHTML')[:500]}...")

                # Nome do produto (priorizar atributo title da imagem)
                name = ""
                try:
                    img_element = item.find_element(By.CSS_SELECTOR, 'img.poly-component__picture')
                    name = img_element.get_attribute('title').strip()
                    if not name or len(name) < 10:  # Ignora títulos curtos
                        name = ""
                except:
                    # Fallback para seletores de texto
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
                if not name:
                    print(f"Erro ao extrair nome do produto para item {index}")

                # Preço
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
                if price == 0.0:
                    print(f"Erro ao extrair preço do produto para item {index}")

                # Link
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
                if not link:
                    print(f"Erro ao extrair link do produto para item {index}")

                # Adiciona produto mesmo se apenas um campo for válido
                if name or price > 0 or link:
                    products.append({
                        'name': name if name else "Nome não encontrado",
                        'price': price if price > 0 else None,
                        'link': link if link else None
                    })
                    print(f"Produto extraído: {name if name else 'Nome não encontrado'}, Preço: {price if price > 0 else 'Não encontrado'}, Link: {link if link else 'Não encontrado'}")
                else:
                    print(f"Produto ignorado para item {index} (nome: {name}, preço: {price}, link: {link})")
            except Exception as e:
                print(f"Erro ao extrair dados do produto {index}: {e}")
                continue
    except Exception as e:
        print(f"Erro ao extrair produtos: {e}")

    return products

# Função para salvar em CSV
def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'link'])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

# Busca por notebooks, celulares e palavras semelhantes
search_terms = [
    'notebook', 'laptop', 'ultrabook', 'computador portátil',
    'celular', 'smartphone', 'telefone', 'celular 5G'
]
url = 'https://www.mercadolivre.com.br'
all_products = []

for term in search_terms:
    print(f"Buscando {term}...")
    products = search_products(term, url, max_products=10)
    all_products.extend(products)
    time.sleep(5)  # Delay entre buscas para evitar bloqueios

# Ordena por preço (menor para maior, ignorando None)
all_products = sorted([p for p in all_products if p['price'] is not None], key=itemgetter('price'))

# Exibir resultados
for product in all_products:
    price_str = f"R${product['price']:.2f}" if product['price'] is not None else "Não disponível"
    link_str = product['link'] if product['link'] is not None else "Não disponível"
    print(f"Nome do produto: {product['name']}, Preço: {price_str}, Link: {link_str}")

# Salva os resultados em um CSV
if all_products:
    save_to_csv(all_products, 'precos_produtos_mercadolivre.csv')
    print("Resultados salvos em 'precos_produtos_mercadolivre.csv'")
else:
    print("Nenhum produto encontrado.")

# Fechar o navegador
driver.quit()