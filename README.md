# Lista de Tarefas Python - Explicação do Código

Este documento explica, passo a passo, o funcionamento do código da nossa Lista de Tarefas feita em Python com interface gráfica usando `ttkbootstrap` e `tkinter`.

---

## 1. Imports e Instalação de Bibliotecas (Heitor)

```python
import sys  # Permite acessar funções do sistema operacional
import subprocess  # Permite rodar comandos do sistema, como instalar pacotes

def instalar(pacote):
    """
    Tenta importar o pacote. Se não conseguir, instala automaticamente usando pip.
    """
    try:
        __import__(pacote)  # Tenta importar o pacote pelo nome
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])  # Instala o pacote

# Instala as bibliotecas necessárias, se não estiverem presentes
instalar("ttkbootstrap")
instalar("json")
instalar("tkinter")

from datetime import date, datetime  # Para trabalhar com datas
import json  # Para salvar e ler tarefas em arquivo
import os  # Para acessar funções do sistema, como verificar se um arquivo existe
from tkinter import Toplevel, Entry, Button, messagebox  # Widgets básicos do Tkinter
import ttkbootstrap as tb  # Biblioteca para deixar a interface mais bonita
from ttkbootstrap.constants import *  # Constantes de estilos do ttkbootstrap
from ttkbootstrap import DateEntry  # Campo especial para escolher datas

ARQUIVO = "tarefas.json"  # Nome do arquivo onde as tarefas serão salvas
```
- **O que faz:** Garante que todas as bibliotecas necessárias estejam instaladas e importadas.  
- **Por que:** Assim, o programa funciona em qualquer computador, mesmo que nunca tenha rodado python antes.

---

## 2. Classe Principal da Aplicação (Heitor)

```python
class ListaDeTarefasApp:
    def __init__(self, master):
        # Configuração da janela principal
        self.master = master  # Guarda a janela principal
        self.master.title("Lista de Tarefas")  # Define o título da janela
        self.master.geometry("560x540")  # Define o tamanho da janela
        self.master.resizable(False, True)  # Permite redimensionar só na vertical

        # Carrega tarefas do arquivo e inicializa interface
        self.lista_de_tarefas = self.carregar_tarefas()  # Carrega tarefas já salvas
        self._criar_widgets()  # Cria os botões, campos e caixas da interface
        self.atualizar_lista()  # Mostra as tarefas na tela
```
- **O que faz:** Cria a janela principal, carrega as tarefas já salvas e monta a interface.

---

## 3. Carregar e Salvar Tarefas (Heitor)

```python
def carregar_tarefas(self):
    """
    Carrega tarefas do arquivo JSON, se existir.
    """
    if os.path.exists(ARQUIVO):  # Verifica se o arquivo existe
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:  # Abre o arquivo para leitura
                return json.load(f)  # Lê as tarefas do arquivo
        except:
            messagebox.showwarning("Aviso", "Erro ao carregar tarefas.")  # Mostra aviso se der erro
            return []
    return []  # Se não existir, retorna lista vazia

def salvar_tarefas(self):
    """
    Salva as tarefas no arquivo JSON.
    """
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:  # Abre o arquivo para escrita
            json.dump(self.lista_de_tarefas, f, ensure_ascii=False, indent=2)  # Salva as tarefas
    except:
        messagebox.showerror("Erro", "Erro ao salvar tarefas.")  # Mostra erro se não conseguir salvar
```
- **O que faz:** Lê e salva as tarefas em um arquivo para não perder nada quando fechar o programa.

---

## 4. Interface Gráfica (Bernardo Franco)

```python
def _criar_widgets(self):
    # Cria os widgets principais da interface

    # Título da lista
    tb.Label(self.master, text="Minhas Tarefas", font=("Segoe UI", 18, "bold")).pack(pady=10)

    # Frame para os campos de entrada (data e tarefa)
    entrada_frame = tb.Frame(self.master)
    entrada_frame.pack(pady=5)
    
    # Campo para escolher a data (DateEntry é um calendário)
    self.campo_data = DateEntry(entrada_frame, width=12,  dateformat=r"%d/%m/%y")
    self.campo_data.pack(side="left", padx=(0, 10))
    # Quando digitar, formata a data automaticamente
    self.campo_data.entry.bind("<KeyRelease>", self.form_data)

    # Campo para digitar a tarefa
    self.campo_entrada = tb.Entry(entrada_frame, width=40)
    self.campo_entrada.pack(side="left", padx=(0, 10))
    self.campo_entrada.focus()  # Deixa o cursor pronto para digitar
    # Se apertar Enter, adiciona a tarefa
    self.campo_entrada.bind('<Return>', lambda event: self.adicionar_tarefa())

    # Botão para limpar a lista de tarefas
    tb.Button(entrada_frame, text="Limpar", bootstyle="danger", command=self.limpar_lista).pack(side="left")

    # Caixa onde as tarefas vão aparecer
    self.container_tarefas = tb.LabelFrame(self.master, borderwidth=2, relief="groove")
    self.container_tarefas.pack(pady=15, padx=10, fill="both", expand=True)
```
- **O que faz:** Monta a tela com campos para digitar tarefas, escolher datas e botões para interagir.

---

## 5. Formatação Automática da Data (Bernardo Franco)

```python
def form_data(self, event):
    """
    Formata o que foi digitado na caixa de data para o formato dd/mm/yy automaticamente.
    """
    valor = self.campo_data.entry.get().replace("/", "")  # Remove todas as barras do que foi digitado (ex: '120624')
    novo = ""
    if len(valor) > 0:
        novo += valor[:2]  # Pega os dois primeiros dígitos (dia)
    if len(valor) > 2:
        novo += "/" + valor[2:4]  # Depois dos dois primeiros, pega os próximos dois (mês) e adiciona uma barra antes
    if len(valor) > 4:
        novo += "/" + valor[4:6]  # Depois do mês, pega os próximos dois (ano) e adiciona outra barra antes
    self.campo_data.entry.delete(0, tb.END)  # Limpa o campo de data para inserir o texto formatado
    self.campo_data.entry.insert(0, novo)  # Insere o texto já formatado
    self.campo_data.entry.icursor(tb.END)  # Coloca o cursor no final do texto, para facilitar a digitação
```
- **O que faz:** Ajuda o usuário a digitar a data no formato correto, colocando as barras automaticamente.

---

## 6. Atualizar a Lista de Tarefas (Bernardo Franco)

```python
def atualizar_lista(self):
    """
    Atualiza a lista de tarefas na interface.
    """
    self.lista_de_tarefas.sort(key=lambda item: datetime.strptime(item["data"], "%d/%m/%y"), reverse=True) # Ordena as tarefas por data
    for widget in self.container_tarefas.winfo_children():
        widget.destroy()  # Remove tudo que está na tela
    for indice, item in enumerate(self.lista_de_tarefas):
        self._adicionar_linha(item, indice)  # Adiciona cada tarefa de novo
```
- **O que faz:** Limpa e mostra todas as tarefas na tela, sempre atualizadas.

---

## 7. Adicionar Linha de Tarefa (Bernardo Franco)

```python
def _adicionar_linha(self, item, indice):
    """
    Adiciona uma linha (tarefa) na interface.
    """
    frame = tb.Frame(self.container_tarefas)
    frame.pack(fill="x", pady=2, padx=10)

    data_tarefa = datetime.strptime(item["data"], "%d/%m/%y").date()  # Converte a data de texto para data

    def checkin():
        # Marca/desmarca tarefa como feita
        self.lista_de_tarefas[indice]["feito"] = feito.get()
        self.salvar_tarefas()
        self.atualizar_lista()

    feito = tb.BooleanVar(value=item["feito"])  # Variável booleana para o checkbox
    if data_tarefa < date.today():
        status = tb.Checkbutton(frame, variable=feito, command=checkin, state="disabled") # Caso tenha passado a data, a checkbox é desativada
    else:
        status = tb.Checkbutton(frame, variable=feito, command=checkin) # Checkbox para marcar como feita
    status.pack(side="left")
    
    # Label da tarefa, quebra linha se for muito grande
    tarefa_label = tb.Label(frame, text=item['tarefa'], font=("Arial", 12), wraplength=340, anchor="w")
    tarefa_label.pack(side="left", fill="x", expand=True)
    # Se clicar no texto, alterna entre feito/não feito
    tarefa_label.bind("<Button-1>", lambda e, i=indice: self.toggle_feito(i))

    # Botões de editar e apagar
    tb.Button(frame, text="✏", width=2, bootstyle="secondary", command=lambda i=indice: self.editar_tarefa(i)).pack(side="right", padx=2)
    tb.Button(frame, text="🗑", width=2, bootstyle="danger", command=lambda i=indice: self.apagar_tarefa(i)).pack(side="right", padx=2)

    # Exibe a data da tarefa, com cor diferente se for hoje ou atrasada
    if item['feito']: # Deixa a data verde se ja foi feita
        tb.Label(frame, text=item["data"], font=("Arial", 10), foreground="#00f91d").pack(side="right", padx=8)
    else:
        # Exibe a data da tarefa
        if data_tarefa == date.today(): # Verifica se a data da tarefa corresponde a data atual
            tb.Label(frame, text=item["data"], font=("Arial", 10), foreground="#f1e905").pack(side="right", padx=8)
        elif data_tarefa < date.today(): # Verifica se ja passou a data da tarefa
            tb.Label(frame, text=item["data"], font=("Arial", 10), foreground="#e91010").pack(side="right", padx=8)
        else:
            tb.Label(frame, text=item["data"], font=("Arial", 10)).pack(side="right", padx=8)
```
- **O que faz:** Mostra cada tarefa na tela, com botões para marcar como feita, editar ou apagar, e destaca a data.

---

## 8. Funções de Interação (Luis Davi)

```python
def adicionar_tarefa(self):
    """
    Adiciona uma nova tarefa à lista.
    """
    texto = self.campo_entrada.get().strip()  # Pega o texto digitado, sem espaços extras
    if texto:
        try:  # Verifica se a data inserida é válida
            data = datetime.strptime(self.campo_data.entry.get(), "%d/%m/%y").strftime("%d/%m/%y")
        except ValueError:
            messagebox.showerror("Data invalída", "Por favor, insira uma data valída no formato: DD/MM/AA")
            self.campo_data.entry.delete(0, tb.END)
            self.campo_data.entry.insert(0, date.today().strftime("%d/%m/%y"))
            self.campo_data.entry.focus()
            return
        # Adiciona a tarefa na lista
        self.lista_de_tarefas.append({"tarefa": texto, "feito": False, "data": str(data)})
        self.salvar_tarefas()
        self.atualizar_lista()
        self.campo_entrada.delete(0, tb.END)  # Limpa o campo de texto
    else:
        messagebox.showinfo("Atenção", "Digite algo para adicionar.")

def toggle_feito(self, indice):
    """
    Alterna o status de feito/não feito.
    """
    self.lista_de_tarefas[indice]["feito"] = not self.lista_de_tarefas[indice]["feito"]
    self.salvar_tarefas()
    self.atualizar_lista()

def editar_tarefa(self, indice):
    """
    Abre janela para editar o texto da tarefa.
    """
    texto_atual = self.lista_de_tarefas[indice]["tarefa"]

    janela_editar = Toplevel(self.master)  # Cria uma nova janela
    janela_editar.title("Editar Tarefa")
    janela_editar.geometry("340x130")
    janela_editar.resizable(False, False)

    entrada_editar = Entry(janela_editar, width=40)  # Campo para editar o texto
    entrada_editar.insert(0, texto_atual)
    entrada_editar.pack(pady=20)
    entrada_editar.focus()

    def salvar():
        novo_texto = entrada_editar.get().strip()
        if novo_texto:
            self.lista_de_tarefas[indice]["tarefa"] = novo_texto
            self.salvar_tarefas()
            self.atualizar_lista()
            janela_editar.destroy()  # Fecha a janela de edição
        else:
            messagebox.showwarning("Aviso", "Texto não pode ficar vazio.")

    Button(janela_editar, text="Salvar", command=salvar).pack()

def apagar_tarefa(self, indice):
    """
    Remove uma tarefa da lista, após confirmação.
    """
    if messagebox.askyesno("Confirmar", "Deseja apagar esta tarefa?"):
        self.lista_de_tarefas.pop(indice)
        self.salvar_tarefas()
        self.atualizar_lista()

def limpar_lista(self):
    """
    Limpa todas as tarefas da lista (com confirmação dupla).
    """
    if messagebox.askyesno("Confirmar", "Deseja limpar a lista de tarefas?"):
        if messagebox.askyesno("Confirmar", "Essa ação é IRREVERSÍVEL. Tem certeza?"):
            self.lista_de_tarefas.clear()
            self.salvar_tarefas()
            self.atualizar_lista()
```
- **O que faz:** Permite adicionar, marcar como feita, editar, apagar e limpar tarefas.

---

## 9. Inicialização da Janela Principal (Luis Davi)

```python
# --- INICIALIZAÇÃO DA JANELA PRINCIPAL ---
# Cria a janela principal com o tema "superhero"
janela = tb.Window(themename="superhero")
app = ListaDeTarefasApp(janela)  # Cria o aplicativo
janela.mainloop()  # Mantém a janela aberta esperando ações do usuário
```
- **O que faz:** Cria a janela principal, inicia o aplicativo e mantém a janela aberta até o usuário fechar.

---

## **Resumo**

- O código cria uma lista de tarefas com interface gráfica.
- Permite adicionar, marcar como feita, editar, apagar e limpar tarefas.
- Salva tudo em um arquivo para não perder as tarefas.
- Usa bibliotecas para deixar a interface mais bonita e fácil de usar.
