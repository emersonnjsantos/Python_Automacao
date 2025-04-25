import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import sys
import platform
import os
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import urllib.parse

# Inicializar reconhecedor de voz e mecanismo de fala
r = sr.Recognizer()
engine = pyttsx3.init()

# Configurar voz em português, se disponível
voices = engine.getProperty('voices')
for voice in voices:
    if "brazil" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150)

# Inicializar banco de dados SQLite
conn = sqlite3.connect('sites.db')
cursor = conn.cursor()

# Criar tabela ou atualizar esquema
cursor.execute('''CREATE TABLE IF NOT EXISTS sites
                 (name TEXT PRIMARY KEY, url TEXT, voice_command TEXT)''')
# Verificar se a coluna voice_command existe e adicionar se necessário
cursor.execute("PRAGMA table_info(sites)")
columns = [col[1] for col in cursor.fetchall()]
if 'voice_command' not in columns:
    cursor.execute("ALTER TABLE sites ADD COLUMN voice_command TEXT")
conn.commit()

# Carregar sites iniciais no banco de dados
initial_sites = {
    "youtube": ("https://www.youtube.com", "youtube"),
    "mercado livre": ("https://www.mercadolivre.com.br", "mercado livre"),
    "google": ("https://www.google.com", "google"),
    "facebook": ("https://www.facebook.com", "facebook"),
    "twitter": ("https://www.twitter.com", "twitter"),
    "netflix": ("https://www.netflix.com", "netflix"),
    "amazon": ("https://www.amazon.com.br", "amazon"),
    "instagram": ("https://www.instagram.com", "instagram"),
    "linkedin": ("https://www.linkedin.com", "linkedin"),
    "whatsapp": ("https://web.whatsapp.com", "whatsapp"),
    "spotify": ("https://open.spotify.com", "spotify")
}

for name, (url, voice_command) in initial_sites.items():
    cursor.execute("INSERT OR IGNORE INTO sites (name, url, voice_command) VALUES (?, ?, ?)", 
                   (name, url, voice_command))
conn.commit()

def load_sites():
    cursor.execute("SELECT name, url, voice_command FROM sites")
    return {row[0]: {"url": row[1], "voice_command": row[2]} for row in cursor.fetchall()}

def add_site(name, url, voice_command):
    cursor.execute("INSERT OR REPLACE INTO sites (name, url, voice_command) VALUES (?, ?, ?)", 
                   (name.lower(), url, voice_command.lower() if voice_command else name.lower()))
    conn.commit()

def delete_site(name):
    cursor.execute("DELETE FROM sites WHERE name = ?", (name,))
    conn.commit()

def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Ouvindo...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            print("Nenhum comando detectado.")
            return ""
        except sr.UnknownValueError:
            print("Não entendi o comando.")
            return ""
        except sr.RequestError:
            print("Erro de conexão com o serviço de reconhecimento.")
            return ""

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def open_spotify():
    speak("Abrindo Spotify!")
    system = platform.system()
    if system == "Windows":
        spotify_path = os.path.expanduser(r"~\AppData\Roaming\Spotify\Spotify.exe")
        if os.path.exists(spotify_path):
            try:
                subprocess.Popen([spotify_path], shell=False)
            except Exception:
                webbrowser.open("https://open.spotify.com")
        else:
            webbrowser.open("https://open.spotify.com")
    elif system == "Darwin":
        try:
            subprocess.Popen(["open", "-a", "Spotify"])
        except Exception:
            webbrowser.open("https://open.spotify.com")
    elif system == "Linux":
        try:
            subprocess.Popen(["spotify"])
        except Exception:
            webbrowser.open("https://open.spotify.com")
    else:
        webbrowser.open("https://open.spotify.com")

def process_command(command, sites):
    if not command:
        return True
    if "sair" in command:
        speak("Encerrando o programa. Até logo!")
        return False
    if "hora" in command:
        current_time = datetime.now().strftime("%H:%M")
        speak(f"Agora são {current_time}.")
        return True
    if "tocar música" in command or "spotify" in command or "abrir spotify" in command:
        open_spotify()
        return True
    for site_name, data in sites.items():
        voice_command = data["voice_command"]
        if voice_command and (voice_command in command or f"abrir {voice_command}" in command):
            speak(f"Abrindo {site_name}!")
            webbrowser.open(data["url"])
            return True
    speak("Comando não reconhecido. Tente dizer o nome de um site, 'tocar música' ou 'sair'.")
    return True

class ManageSitesWindow:
    def __init__(self, parent, sites, update_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Sites")
        self.window.geometry("600x400")
        self.sites = sites
        self.update_callback = update_callback

        # Treeview para listar sites
        columns = ("Nome", "URL", "Comando de Voz")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("URL", text="URL")
        self.tree.heading("Comando de Voz", text="Comando de Voz")
        self.tree.column("Nome", width=150)
        self.tree.column("URL", width=250)
        self.tree.column("Comando de Voz", width=150)
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Preencher Treeview com sites
        for name, data in sites.items():
            self.tree.insert("", tk.END, values=(name, data["url"], data["voice_command"]))

        # Botão para apagar site selecionado
        tk.Button(self.window, text="Apagar Site Selecionado", command=self.delete_selected).pack(pady=10)

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um site para apagar!")
            return
        name = self.tree.item(selected_item)["values"][0]
        if messagebox.askyesno("Confirmação", f"Deseja apagar o site '{name}'?"):
            delete_site(name)
            self.tree.delete(selected_item)
            self.update_callback()
            messagebox.showinfo("Sucesso", f"Site '{name}' apagado!")

class VoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente de Voz")
        self.root.geometry("400x450")

        # Caixa de texto para nome do site
        tk.Label(root, text="Nome do site:").pack(pady=5)
        self.site_name_entry = tk.Entry(root, width=30)
        self.site_name_entry.pack(pady=5)

        # Caixa de texto para URL ou pesquisa
        tk.Label(root, text="URL ou Pesquisa Google:").pack(pady=5)
        self.site_url_entry = tk.Entry(root, width=30)
        self.site_url_entry.pack(pady=5)

        # Botão para pesquisar no Google
        tk.Button(root, text="Pesquisar no Google", command=self.search_google).pack(pady=5)

        # Botão para adicionar site e gravar comando de voz
        tk.Button(root, text="Adicionar Site e Gravar Voz", command=self.add_site).pack(pady=10)

        # Botão para gerenciar sites
        tk.Button(root, text="Gerenciar Sites", command=self.open_manage_sites).pack(pady=5)

        # Botão para ouvir comandos gerais
        tk.Button(root, text="Ouvir Comando", command=self.listen_command).pack(pady=10)

        # Status
        self.status_label = tk.Label(root, text="Pronto para ouvir...")
        self.status_label.pack(pady=10)

        self.paused = False
        self.sites = load_sites()

    def search_google(self):
        query = self.site_url_entry.get().strip()
        if query:
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(search_url)
            messagebox.showinfo("Instrução", "Copie a URL do site desejado nos resultados e cole na caixa de URL.")
        else:
            messagebox.showerror("Erro", "Digite um termo para pesquisar!")

    def add_site(self):
        name = self.site_name_entry.get().strip().lower()
        url = self.site_url_entry.get().strip()
        if name and url:
            if not url.startswith("http"):
                url = "https://" + url
            speak("Diga o comando de voz para este site.")
            self.status_label.config(text="Gravando comando de voz...")
            voice_command = listen()
            if voice_command:
                add_site(name, url, voice_command)
                self.sites = load_sites()
                messagebox.showinfo("Sucesso", f"Site '{name}' adicionado com comando '{voice_command}'!")
                self.site_name_entry.delete(0, tk.END)
                self.site_url_entry.delete(0, tk.END)
                self.status_label.config(text="Pronto para ouvir...")
            else:
                messagebox.showerror("Erro", "Nenhum comando de voz detectado!")
        else:
            messagebox.showerror("Erro", "Preencha nome e URL!")

    def open_manage_sites(self):
        ManageSitesWindow(self.root, self.sites, self.update_sites)

    def update_sites(self):
        self.sites = load_sites()

    def listen_command(self):
        if self.paused:
            command = listen()
            if "volte" in command:
                speak("Sistema retomado.")
                self.paused = False
                self.status_label.config(text="Pronto para ouvir...")
            else:
                speak("Sistema pausado. Diga 'volte' para continuar.")
            return

        command = listen()
        self.status_label.config(text=f"Comando: {command}" if command else "Nenhum comando detectado")
        
        if "pause" in command:
            speak("Pausando o sistema. Diga 'volte' para retomar.")
            self.paused = True
            self.status_label.config(text="Sistema pausado")
        else:
            if not process_command(command, self.sites):
                self.root.quit()

def main():
    root = tk.Tk()
    app = VoiceApp(root)
    root.mainloop()
    conn.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Programa interrompido. Até logo!")
        sys.exit(0)