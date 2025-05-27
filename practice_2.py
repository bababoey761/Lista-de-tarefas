import sys
import subprocess

# Função para instalar pacotes se necessário
def instalar(pacote):
    try:
        __import__(pacote)
    except ImportError:
        print(f"Instalando {pacote}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

# Instala as bibliotecas necessárias
instalar('requests')
instalar('ttkbootstrap')

from datetime import date
import random
import requests
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

# Baixa a lista de palavras
url = "https://raw.githubusercontent.com/bababoey761/exercicios/refs/heads/main/palavras_portugues_comuns.dic"
try:
    resposta = requests.get(url)
    palavras = []
except requests.exceptions.RequestException as e:
    print(f"Erro ao baixar a lista de palavras: {e}")
    exit(1)
for linha in resposta.text.splitlines():
    linha = linha.strip()
    if not linha or linha.startswith("#") or "/" in linha:
        continue
    palavras.append(linha.lower())

def abrir_jogos():
    def iniciar_forca():
        palavra = random.choice(palavras)
        letras_descobertas = ["_" for _ in palavra]
        tentativas = 7
        letras_erradas = []

        def atualizar_tela():
            forca_label.config(text="Palavra: " + " ".join(letras_descobertas))
            tentativas_label.config(text=f"Tentativas restantes: {tentativas}")
            erradas_label.config(text="Letras erradas: " + " ".join(letras_erradas))

        def tentar_letra():
            nonlocal tentativas
            letra = entrada_letra.get().lower()
            entrada_letra.delete(0, tb.END)
            if not letra or len(letra) != 1 or not letra.isalpha():
                resultado_forca.config(text="Digite apenas uma letra!")
                return
            if letra in letras_descobertas or letra in letras_erradas:
                resultado_forca.config(text="Letra já usada!")
                return
            if letra in palavra:
                for i, l in enumerate(palavra):
                    if l == letra:
                        letras_descobertas[i] = letra
                resultado_forca.config(text="Acertou!")
            else:
                tentativas -= 1
                letras_erradas.append(letra)
                resultado_forca.config(text="Errou!")
            atualizar_tela()
            if "_" not in letras_descobertas:
                resultado_forca.config(text=f"Parabéns! Você ganhou! Palavra: {palavra}")
                btn_tentar.config(state=tb.DISABLED)
                janela_forca.after(5000, janela_forca.destroy)
            elif tentativas == 0:
                resultado_forca.config(text=f"Você perdeu! Palavra era: {palavra}")
                btn_tentar.config(state=tb.DISABLED)
                janela_forca.after(5000, janela_forca.destroy)

        # Nova janela para o jogo da forca
        janela_forca = tb.Toplevel(root)
        janela_forca.title("Jogo da Forca")
        janela_forca.geometry("350x300")

        forca_label = tb.Label(janela_forca, text="", font=("Arial", 16))
        forca_label.pack(pady=5)
        tentativas_label = tb.Label(janela_forca, text="", font=("Arial", 12))
        tentativas_label.pack()
        erradas_label = tb.Label(janela_forca, text="", font=("Arial", 12))
        erradas_label.pack()
        entrada_letra = tb.Entry(janela_forca, width=5, font=("Arial", 14))
        entrada_letra.pack(pady=5)
        btn_tentar = tb.Button(janela_forca, text="Tentar letra", bootstyle=PRIMARY, command=tentar_letra)
        btn_tentar.pack()
        resultado_forca = tb.Label(janela_forca, text="", font=("Arial", 12))
        resultado_forca.pack(pady=5)

        atualizar_tela()

    # Abre o jogo da forca ao clicar em "Jogos"
    iniciar_forca()

def abrir_calculos():
    resultado_label.config(text="em desenvolvimento!")

def abrir_tempo_de_vida():
    resultado_label.config(text="em desenvolvimento!")

def abrir_sinais():
    resultado_label.config(text="em desenvolvimento!")

def sair():
    root.destroy()

root = tb.Window(themename="superhero")
root.title("Menu de Prática")
root.geometry("350x400")

tb.Label(root, text="MENU DE PRÁTICA", font=("Arial", 16, "bold")).pack(pady=10)

tb.Button(root, text="Jogos", width=25, bootstyle=SUCCESS, command=abrir_jogos).pack(pady=5)
tb.Button(root, text="Cálculos em geral", width=25, bootstyle=INFO, command=abrir_calculos).pack(pady=5)
tb.Button(root, text="Tempo de vida", width=25, bootstyle=WARNING, command=abrir_tempo_de_vida).pack(pady=5)
tb.Button(root, text="Ordem crescente com sinais", width=25, bootstyle=PRIMARY, command=abrir_sinais).pack(pady=5)
tb.Button(root, text="Sair", width=25, bootstyle=DANGER, command=sair).pack(pady=5)

resultado_label = tb.Label(root, text="", font=("Arial", 12))
resultado_label.pack(pady=10)

root.mainloop()