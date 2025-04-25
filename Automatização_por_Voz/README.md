# 🗣️ Assistente de Voz em Python

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()
[![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-Enabled-success)]()
[![GUI](https://img.shields.io/badge/Interface%20Gráfica-Tkinter-blueviolet)]()

Um assistente de voz em Python que permite abrir sites por comandos de voz ou via interface gráfica. Os sites são armazenados em um banco de dados SQLite e você ainda pode gerar um executável (.exe) para rodar o programa de forma independente.

---




## 🚀 Funcionalidades

- 🎙️ **Comandos de voz**: Diga "YouTube", "Spotify", "hora", "pause", "sair" e muito mais.
- 🖼️ **Interface gráfica (Tkinter)**: Adicione, pesquise e gerencie sites com praticidade.
- 🧠 **Banco de dados SQLite**: Sites são salvos dinamicamente.
- 🎵 **Integração com Spotify**: Abre o app ou site ao dizer "Spotify" ou "tocar música".
- 🧾 **Compilação para .exe**: Transforme o programa em um executável com `PyInstaller`.

---

## 🧰 Requisitos

### 📦 Pacotes Python


pip install speechrecognition pyttsx3 PyAudio pyinstaller



speechrecognition: Reconhecimento de voz via API do Google

pyttsx3: Síntese de voz (text-to-speech)

PyAudio: Captura de áudio do microfone

pyinstaller: Compilação para .exe

tkinter: Interface gráfica (incluso no Python)

sqlite3: Banco de dados (incluso no Python)

### 💻 Outros ###
Microfone: Para entrada de comandos de voz

Internet: Necessária para o reconhecimento de voz (Google API)

Spotify (opcional): Instale o app para abrir localmente

Sistema operacional: Testado no Windows; compatível com macOS e Linux

## 🛠️ Como Gerar o Executável .exe
Salve o código em voz.py

Instale o PyInstaller

bash
Copiar
Editar
pip install pyinstaller
Gere o .exe

bash
Copiar
Editar
pyinstaller --onefile --windowed voz.py
O .exe será gerado na pasta dist.

Execute o .exe

Mova para um local com permissões de escrita (ex: Desktop)

Ao executar, o banco sites.db será criado automaticamente

## 📌 Como Usar
## ▶️ Iniciar o programa
Execute o voz.exe — a janela principal será aberta.

## 🌐 Adicionar um site
Digite o nome do site (ex: shoppy)

Digite a URL ou pesquisa no Google

Use o botão "Pesquisar no Google" (opcional)

Clique em "Adicionar Site e Gravar Voz" e diga o comando

## 🗑️ Apagar um site
Vá em "Gerenciar Sites"

Selecione o site e clique em "Apagar Site Selecionado"

## 🎤 Usar comandos de voz
Clique em "Ouvir Comando" e fale:

"abrir [nome]", ex: abrir YouTube

"Spotify" ou "tocar música"

"hora" — ouve a hora atual

"pause" — pausa o assistente

"volte" — retoma

"sair" — encerra o programa

## 🧩 Solução de Problemas
Erro no banco de dados: Delete o sites.db e reinicie o app

Spotify não abre:

Verifique o caminho: C:\Users\[SeuUsuário]\AppData\Roaming\Spotify\Spotify.exe

Comando de voz não reconhecido:

Fale com clareza e tenha boa conexão de internet

.exe não funciona:

Execute em um diretório com permissões de escrita

## 📄 Licença
Distribuído sob a licença MIT.

## 🤝 Contribuições
Contribuições são bem-vindas!
Abra uma issue ou envie um pull request ✨

