# periodo_1 trabalho de programação
# Lista de Tarefas com Tkinter(ttkbootstrap) e JSON 

import sys
import subprocess
ARQUIVO = "tarefas.json" # Define o nome do arquivo JSON onde as tarefas serão salvas
tarefas = []     

# Nesse bloco aqui, verificamos se os pacotes necessarios já estão instalado. Se não estiver, ele será instalado usando o pip. 
def instalar(pacote):
    try:
        __import__(pacote)
    except ImportError:
        print(f"Instalando {pacote}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

instalar('ttkbootstrap')
instalar('tkinter')
instalar('json')

from tkinter import Listbox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import json
import os

# Lembre-se de que a função OPEN() do tkinter possui 4 modos principais:
# "r" para leitura, "w" para escrita, "a" para anexar e "x" para criar um novo arquivo.

# vamos começar com as funçoes de carregar e salvar as tarefas.

def carregar_tarefas():
    if os.path.exists(ARQUIVO): # verifica se o arquivo existe
        with open(ARQUIVO, "r", encoding="utf-8") as f: # utiliza utf-8 para suportar caracteres especiais e "r" para leitura sendo a abreviação de read
            return json.load(f) # carrega as tarefas do arquivo JSON
    return [] 

tarefas = carregar_tarefas() 

def salvar_tarefas():
    with open(ARQUIVO, "w", encoding="utf-8") as f: # utiliza o "w" para escrita sendo a abreviação de write
        json.dump(tarefas, f, ensure_ascii=False, indent=2) # salva as tarefas no arquivo JSON
        # O ensure_ascii=False permite que caracteres especiais sejam salvos corretamente no JSON.
def adicionar_tarefa():
    texto = entrada.get().strip() # obtém o texto da entrada e remove espaços em branco no início e no final
    if texto:
        tarefas.append({"tarefa": texto, "feito": False}) # adiciona a tarefa com o status "feito" como False
        salvar_tarefas()
        atualizar_lista()
        entrada.delete(0, tb.END) # limpa a entrada após adicionar a tarefa

def marcar_concluida():
    selecionado = lista.curselection() # obtém o índice do item selecionado na lista
    if selecionado:
        idx = selecionado[0]  
        tarefas[idx]["feito"] = not tarefas[idx]["feito"]  # alterna o status "feito" da tarefa selecionado
        salvar_tarefas()
        atualizar_lista()

def remover_tarefa():
    selecionado = lista.curselection()
    if selecionado:
        idx = selecionado[0] 
        tarefas.pop(idx) # remove a tarefa selecionada da lista
        # pop() remove o item na posição especificada e retorna o valor removido
        salvar_tarefas()
        atualizar_lista()

def atualizar_lista(): 
    lista.delete(0, tb.END) # limpa a lista antes de atualizar
    for t in tarefas:
        status = "✔️" if t["feito"] else "❌" # Vai aplicar um emoji de "✔️" se a tarefa estiver concluída e "❌" se não estiver
        lista.insert(tb.END, f"{status} {t['tarefa']}") # insere cada tarefa na lista com seu status

        # tb.END é usado para adicionar o item no final da lista, enquanto tb.NEXT adicionaria no próximo item.

# Aqui é onde sera trabalhado o HUD com o tkinter e ttkbootstrap
# ttkbootstrap é uma biblioteca que fornece temas e estilos para tkinter, facilitando a criação de interfaces mais modernas e atraentes.

# Diferente do tkinter, que usa tk.Tk() para criar a janela principal, o ttkbootstrap usa tb.Window() para criar uma janela com tema.

root = tb.Window(themename="superhero") # Cria uma janela com o tema "superhero" do ttkbootstrap
root.title("Lista de Tarefas")  # Define o título da janela
root.geometry("400x400") # Define o tamanho da janela

# Cada tema tem um estilo diferente, o que pode mudar a aparência dos botões, entradas e outros widgets.
# Você pode escolher o tema que mais gostar, basta alterar o valor de "themename" na linha acima.
# Acesse o site https://ttkbootstrap.readthedocs.io para ver os temas disponíveis

# Diferente do tkinter, que usa a abreviação "tk" para importar os módulos, o ttkbootstrap usa a abreviação "tb" para facilitar a leitura do código.

# Aqui vamos criar os widgets (itens da interface) e organizá-los na janela.
tb.Label(root, text="Lista de tarefas", font=("Arial", 16, "bold")).pack(pady=10)

entrada = tb.Entry(root, width=30) # Cria uma entrada de texto para digitar as tarefas
entrada.pack(pady=5) 
entrada.focus() # Isso faz com que a entrada receba o foco automaticamente quando a janela é aberta, permitindo que o usuário comece a digitar 
#                 imediatamente.

#  os valores pad são usados para definir o espaçamento vertical (pady) e horizontal (padx) entre os widgets.
# e para definir o tamanho da entrada, usamos o parâmetro width, que define a largura em caracteres
#  e para altura usamos o parâmetro height, que define a altura em linhas.
botoes = tb.Frame(root) # Cria um frame para agrupar os botões
botoes.pack(pady=5)

tb.Button(botoes, text="Adicionar", bootstyle=SUCCESS, command=adicionar_tarefa).pack(side="left", padx=5)
tb.Button(botoes, text="Concluir", bootstyle=INFO, command=marcar_concluida).pack(side="left", padx=5)
tb.Button(botoes, text="Remover", bootstyle=DANGER, command=remover_tarefa).pack(side="left", padx=5)

# Esses termos (SUCESS, INFO, DANGER) correspondem aos estilos de botão do ttkbootstrap ao se aplicar o bootstyle.
# Eles são usados para definir a aparência do botão, como cor e estilo.
# Sendo SUCESS (verde), INFO (azul), DANGER (vermelho)
# Além desses, existem outros estilos como WARNING (amarelo), PRIMARY (azul claro), SECONDARY (cinza), LIGHT (branco) e DARK (preto).
# Lembre-se que essas cores apenas de aplicam ao tema "superhero" do ttkbootstrap, se você usar outro tema, as cores podem ser diferentes.


lista = Listbox(root, width=40, height=12, font=("Arial", 12)) # listbox é um comando do **tkinter** que permite exibir uma lista de itens
lista.pack(pady=10) # o método pack() é usado para organizar os itens na janela que fica logo abaixo dos botões



atualizar_lista()

root.mainloop()
