# Explicação do Código: Lista de Tarefas Python

Este documento explica, passo a passo, o funcionamento do código da nossa Lista de Tarefas feita em Python com interface gráfica.

---

## 1. Instalação e Importação de Bibliotecas

```python
import sys
import subprocess

def instalar(pacote):
    try:
        __import__(pacote)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

instalar("ttkbootstrap")
instalar("json")
instalar("tkinter")

from datetime import date, datetime
import json
import os
from tkinter import Toplevel, Entry, Button, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap import DateEntry
```

- **O que faz:** Garante que todas as bibliotecas necessárias estejam instaladas e importadas.
- **Por que:** Assim, o programa funciona em qualquer computador, mesmo que nunca tenha rodado Python antes.

---

## 2. Arquivo de Dados

```python
ARQUIVO = "tarefas.json"
```
- **O que faz:** Define o nome do arquivo onde as tarefas serão salvas.

---

## 3. Classe Principal da Aplicação

```python
class ListaDeTarefasApp:
    def __init__(self, master):
        # Configuração da janela principal
        self.master = master
        self.master.title("Lista de Tarefas")
        self.master.geometry("560x540")
        self.master.resizable(False, True)

        # Carrega tarefas do arquivo e inicializa interface
        self.lista_de_tarefas = self.carregar_tarefas()
        self._criar_widgets()
        self.atualizar_lista()
```
- **O que faz:** Cria a janela principal, carrega as tarefas já salvas e monta a interface.

---

## 4. Carregar e Salvar Tarefas

```python
def carregar_tarefas(self):
    # Carrega tarefas do arquivo JSON, se existir
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            messagebox.showwarning("Aviso", "Erro ao carregar tarefas.")
            return []
    return []

def salvar_tarefas(self):
    # Salva as tarefas no arquivo JSON
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(self.lista_de_tarefas, f, ensure_ascii=False, indent=2)
    except:
        messagebox.showerror("Erro", "Erro ao salvar tarefas.")
```
- **O que faz:** Lê e salva as tarefas em um arquivo para não perder nada quando fechar o programa.

---

## 5. Interface Gráfica

```python
def _criar_widgets(self):
    # Cria os widgets principais da interface
    tb.Label(self.master, text="Minhas Tarefas", font=("Segoe UI", 18, "bold")).pack(pady=10)

    entrada_frame = tb.Frame(self.master)
    entrada_frame.pack(pady=5)
    
    # Campo para escolher a data
    self.campo_data = DateEntry(entrada_frame, width=12,  dateformat=r"%d/%m/%y")
    self.campo_data.pack(side="left", padx=(0, 10))
    self.campo_data.entry.bind("<KeyRelease>", self.form_data)

    # Campo para digitar a tarefa
    self.campo_entrada = tb.Entry(entrada_frame, width=40)
    self.campo_entrada.pack(side="left", padx=(0, 10))
    self.campo_entrada.focus()
    self.campo_entrada.bind('<Return>', lambda event: self.adicionar_tarefa())

    # Botão para limpar a lista
    tb.Button(entrada_frame, text="Limpar", bootstyle="danger", command=self.limpar_lista).pack(side="left")

    # Frame onde as tarefas serão exibidas
    self.container_tarefas = tb.LabelFrame(self.master, borderwidth=2, relief="groove")
    self.container_tarefas.pack(pady=15,padx=10, fill="both", expand=True)
```
- **O que faz:** Monta a tela com campos para digitar tarefas, escolher datas e botões para interagir.

---

## 6. Formatação Automática da Data

```python
def form_data(self, event):
    # Deixa oque foi inserido na caixa de data no formato dd/mm/yy automaticamente
    valor = self.campo_data.entry.get().replace("/", "")
    novo = ""
    if len(valor) > 0:
        novo += valor[:2]
    if len(valor) > 2:
        novo += "/" + valor[2:4]
    if len(valor) > 4:
        novo += "/" + valor[4:6]
    self.campo_data.entry.delete(0, tb.END)
    self.campo_data.entry.insert(0, novo)
    self.campo_data.entry.icursor(tb.END)
```
- **O que faz:** Ajuda o usuário a digitar a data no formato correto, colocando as barras automaticamente.

---

## 7. Atualizar a Lista de Tarefas

```python
def atualizar_lista(self):
    # Atualiza a lista de tarefas na interface
    for widget in self.container_tarefas.winfo_children():
        widget.destroy()
    for indice, item in enumerate(self.lista_de_tarefas):
        self._adicionar_linha(item, indice)
```
- **O que faz:** Limpa e mostra todas as tarefas na tela, sempre atualizadas.

---

## 8. Adicionar Linha de Tarefa

```python
def _adicionar_linha(self, item, indice):
    # Adiciona uma linha (tarefa) na interface
    frame = tb.Frame(self.container_tarefas)
    frame.pack(fill="x", pady=2, padx=10)

    data_tarefa = datetime.strptime(item["data"], "%d/%m/%y").date()

    def checkin():
        # Marca/desmarca tarefa como feita
        self.lista_de_tarefas[indice]["feito"] = feito.get()
        self.salvar_tarefas()
        self.atualizar_lista()

    feito = tb.BooleanVar(value=item["feito"])
    status = tb.Checkbutton(frame, variable=feito, command=checkin)
    status.pack(side="left")
    
    tarefa_label = tb.Label(frame, text=item['tarefa'], font=("Arial", 12),wraplength=340, anchor="w")
    tarefa_label.pack(side="left", fill="x", expand=True)
    tarefa_label.bind("<Button-1>", lambda e, i=indice: self.toggle_feito(i))

    # Botões de editar e apagar
    tb.Button(frame, text="✏", width=2, bootstyle="secondary", command=lambda i=indice: self.editar_tarefa(i)).pack(side="right", padx=2)
    tb.Button(frame, text="🗑", width=2, bootstyle="danger", command=lambda i=indice: self.apagar_tarefa(i)).pack(side="right", padx=2)

    # Exibe a data da tarefa
    if data_tarefa == date.today():
        tb.Label(frame, text=item["data"], font=("Arial", 10), foreground="#f1e905").pack(side="right", padx=8)
    elif data_tarefa <= date.today():
        tb.Label(frame, text=item["data"], font=("Arial", 10), foreground="#e91010").pack(side="right", padx=8)
    else:
         tb.Label(frame, text=item["data"], font=("Arial", 10)).pack(side="right", padx=8)
```
- **O que faz:** Mostra cada tarefa na tela, com botões para marcar como feita, editar ou apagar, e destaca a data.

---

## 9. Funções de Interação

```python
def adicionar_tarefa(self):
    # Adiciona uma nova tarefa à lista
    texto = self.campo_entrada.get().strip()
    if texto:
        try: # Verifica se a data inserida é valída
            data = datetime.strptime(self.campo_data.entry.get(), "%d/%m/%y").strftime("%d/%m/%y")
        except ValueError:
            messagebox.showerror("Data invalída", "Por favor, insira uma data valída no formato: DD/MM/AA")
            self.campo_data.entry.delete(0, tb.END)
            self.campo_data.entry.insert(0, date.today().strftime("%d/%m/%y"))
            self.campo_data.entry.focus()
            return
        self.lista_de_tarefas.append({"tarefa": texto, "feito": False, "data": str(data)})
        self.salvar_tarefas()
        self.atualizar_lista()
        self.campo_entrada.delete(0, tb.END)
    else:
        messagebox.showinfo("Atenção", "Digite algo para adicionar.")

def toggle_feito(self, indice):
    # Alterna o status de feito/não feito
    self.lista_de_tarefas[indice]["feito"] = not self.lista_de_tarefas[indice]["feito"]
    self.salvar_tarefas()
    self.atualizar_lista()

def editar_tarefa(self, indice):
    # Abre janela para editar o texto da tarefa
    texto_atual = self.lista_de_tarefas[indice]["tarefa"]

    janela_editar = Toplevel(self.master)
    janela_editar.title("Editar Tarefa")
    janela_editar.geometry("340x130")
    janela_editar.resizable(False, False)

    entrada_editar = Entry(janela_editar, width=40)
    entrada_editar.insert(0, texto_atual)
    entrada_editar.pack(pady=20)
    entrada_editar.focus()

    def salvar():
        novo_texto = entrada_editar.get().strip()
        if novo_texto:
            self.lista_de_tarefas[indice]["tarefa"] = novo_texto
            self.salvar_tarefas()
            self.atualizar_lista()
            janela_editar.destroy()
        else:
            messagebox.showwarning("Aviso", "Texto não pode ficar vazio.")

    Button(janela_editar, text="Salvar", command=salvar).pack()

def apagar_tarefa(self, indice):
    # Remove uma tarefa da lista
    if messagebox.askyesno("Confirmar", "Deseja apagar esta tarefa?"):
        self.lista_de_tarefas.pop(indice)
        self.salvar_tarefas()
        self.atualizar_lista()

def limpar_lista(self):
    # Limpa todas as tarefas da lista (com confirmação dupla)
    if messagebox.askyesno("Confirmar", "Deseja limpar a lista de tarefas?"):
        if messagebox.askyesno("Confirmar", "Essa ação é IRREVERSÍVEL. Tem certeza?"):
            self.lista_de_tarefas.clear()
            self.salvar_tarefas()
            self.atualizar_lista()
```
- **O que faz:** Permite adicionar, marcar como feita, editar, apagar e limpar tarefas.

---

## 10. Inicialização da Janela Principal

```python
# --- INICIALIZAÇÃO DA JANELA PRINCIPAL ---
janela = tb.Window(themename="superhero")
app = ListaDeTarefasApp(janela)
janela.mainloop()
```
- **O que faz:** Cria a janela principal, inicia o aplicativo e mantém a janela aberta até o usuário fechar.

---

## **Resumo**

- O código cria uma lista de tarefas com interface gráfica.
- Permite adicionar, marcar como feita, editar, apagar e limpar tarefas.
- Salva tudo em um arquivo para não perder as tarefas.
- Usa bibliotecas para deixar a interface mais bonita e fácil de usar.

---

**Dica:**  
Se o grupo quiser entender melhor qualquer parte, procure pelo nome da função ou variável neste documento!
