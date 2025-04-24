## Web Scraping do Mercado Livre

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-green) ![Webdriver Manager](https://img.shields.io/badge/Webdriver%20Manager-4.0%2B-orange) ![License](https://img.shields.io/badge/License-MIT-yellow)



Este projeto é um script de web scraping desenvolvido em Python para extrair informações de produtos (nome e preço) do site do Mercado Livre. Utiliza o Selenium para automação de navegação e o Webdriver Manager para gerenciar o ChromeDriver, garantindo compatibilidade com o Google Chrome.
✨ Funcionalidades

Navegação Automatizada: Acessa a página principal do Mercado Livre e simula a interação de um usuário.
Rolagem Dinâmica: Rola a página até o final para carregar todos os produtos, detectando o fim do conteúdo via JavaScript.
Extração de Dados: Coleta nome e preço dos produtos listados, armazenando-os em uma lista de dicionários.
Tratamento de Erros: Lida com falhas na extração de dados, exibindo mensagens de erro no console.
Saída de Resultados: Exibe os dados extraídos no console no formato: Nome do produto: <NOME>, Preço: <PREÇO>.
Gerenciamento do ChromeDriver: Usa o webdriver-manager para baixar e configurar automaticamente o ChromeDriver.

## 🎯 Finalidade
## O script foi projetado para:

Monitorar preços de produtos no Mercado Livre.
Realizar análises de mercado para comparação de preços.
Coletar dados para projetos de pesquisa ou ferramentas de e-commerce.

Ideal para desenvolvedores, analistas de dados ou entusiastas de automação que desejam extrair dados de forma eficiente.

## 📋 Pré-requisitos

Python 3.8+: Testado com Python 3.8 ou superior.
Google Chrome: Navegador necessário para o ChromeDriver.
Ambiente virtual (recomendado): Para isolar dependências.

## 🛠️ Dependências



Módulo
Versão
Descrição



selenium
4.0+
Automação de navegadores e interação com páginas web.


webdriver-manager
4.0+
Gerenciamento automático do ChromeDriver.


Badges das dependências:

## 🚀 Instalação

## Clone o repositório:
git clone https://github.com/<seu_usuario>/<seu_repositorio>.git
cd <seu_repositorio>


## Crie e ative um ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


## Instale as dependências:
pip install selenium webdriver-manager


## Verifique o Google Chrome:

Certifique-se de que o Chrome está instalado e atualizado (Menu > Ajuda > Sobre o Google Chrome).



## ▶️ Como Usar

Salve o script:

## Copie o código para um arquivo main.py no diretório do projeto.


Execute o script:
python main.py


Saída:

O script abrirá o Chrome, navegará até o Mercado Livre, rolará a página, extrairá os dados e exibirá no console:Nome do produto: <NOME>, Preço: <PREÇO>


Erros durante a extração serão registrados como: Erro ao extrair dados de um produto.



## 🧠 Estrutura do Código

Configuração: Inicializa o ChromeDriver via webdriver-manager.
Navegação: Acessa o Mercado Livre e rola a página dinamicamente.
Extração: Usa seletores CSS (.ui-search-result, .ui-search-item__title, .price-tag-amount) para coletar dados.
Finalização: Exibe os resultados e fecha o navegador.

## 🔧 Possíveis Melhorias

WebDriverWait: Substituir time.sleep por espera dinâmica de elementos.
Exportação: Salvar dados em CSV ou JSON.
Filtros: Adicionar filtros por categoria ou preço.
Manutenção: Automatizar atualização de seletores CSS.

## ⚠️ Limitações

Estrutura do Site: Os seletores CSS podem mudar com atualizações do Mercado Livre.
Performance: A rolagem pode ser lenta em páginas extensas.
Ética: Respeite os termos de serviço do Mercado Livre e evite sobrecarga no servidor.

## 📜 Licença
Distribuído sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
📬 Contato
Para dúvidas ou sugestões, abra uma issue ou envie um e-mail para eme7681@gmail.com

## ⭐ Gostou do projeto? Dê uma estrela no repositório!
