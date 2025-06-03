# --- IMPORTS E CONFIGURAÇÕES INICIAIS ---
import sys
import subprocess

def instalar(pacote):
    try:
        __import__(pacote)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

instalar("ttkbootstrap")
instalar("tkcalendar")

from datetime import date, datetime
import json
import os
from tkinter import Toplevel, Entry, Button, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap import DateEntry

ARQUIVO = "tarefas.json"

# --- CLASSE PRINCIPAL DA APLICAÇÃO ---
class ListaDeTarefasApp:
    def __init__(self, master):
        # Configuração da janela principal
        self.master = master
        self.master.title("Lista de Tarefas")
        self.master.geometry("520x500")
        self.master.resizable(False, False)

        # Carrega tarefas do arquivo e inicializa interface
        self.lista_de_tarefas =self.carregar_tarefas()
        self._criar_widgets()
        self.atualizar_lista()

    # --- BLOCO 1: FUNÇÕES DE ARQUIVO E DADOS (Pessoa 1) ---
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

    # --- BLOCO 2: INTERFACE GRÁFICA (Pessoa 2) ---
    def _criar_widgets(self):
        # Cria os widgets principais da interface
        tb.Label(self.master, text="Minhas Tarefas", font=("Arial", 18, "bold")).pack(pady=10)

        entrada_frame = tb.Frame(self.master)
        entrada_frame.pack(pady=5)
        
        # Campo para selecionar a data
        self.campo_data = DateEntry(entrada_frame, width=12,  dateformat=r"%d/%m/%y")
        self.campo_data.pack(side="left", padx=(0, 10))

        # Campo para digitar a tarefa
        self.campo_entrada = tb.Entry(entrada_frame, width=40)
        self.campo_entrada.pack(side="left", padx=(0, 10))
        self.campo_entrada.focus()
        self.campo_entrada.bind('<Return>', lambda event: self.adicionar_tarefa())

        # Botão para limpar a lista
        tb.Button(entrada_frame, text="Limpar", bootstyle="danger", command=self.limpar_lista).pack(side="left")

        # Frame onde as tarefas serão exibidas
        self.container_tarefas = tb.Frame(self.master)
        self.container_tarefas.pack(pady=10, fill="both", expand=True)

    def atualizar_lista(self):
        # Atualiza a lista de tarefas na interface
        for widget in self.container_tarefas.winfo_children():
            widget.destroy()
        for indice, item in enumerate(self.lista_de_tarefas):
            self._adicionar_linha(item, indice)

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
        
        # Destaca tarefa do dia
        if data_tarefa == date.today():
            tarefa_label = tb.Label(frame, text= item['tarefa'] , font=("Arial", 12, "bold"), borderwidth=2,anchor="w" )
        else:
            tarefa_label = tb.Label(frame, text=item['tarefa'], font=("Arial", 12), anchor="w")
        tarefa_label.pack(side="left", fill="x", expand=True)
        tarefa_label.bind("<Button-1>", lambda e, i=indice: self.toggle_feito(i))

        # Botões de editar e apagar
        tb.Button(frame, text="✏", width=2, bootstyle="secondary", command=lambda i=indice: self.editar_tarefa(i)).pack(side="right", padx=2)
        tb.Button(frame, text="🗑", width=2, bootstyle="danger", command=lambda i=indice: self.apagar_tarefa(i)).pack(side="right", padx=2)

        # Exibe a data da tarefa
        tb.Label(frame, text=item["data"], font=("Arial", 10)).pack(side="right", padx=8)

    # --- BLOCO 3: FUNÇÕES DE INTERAÇÃO (Pessoa 3) ---
    def adicionar_tarefa(self):
        # Adiciona uma nova tarefa à lista
        texto = self.campo_entrada.get().strip()
        if texto:
            try:
                data = datetime.strptime(self.campo_data.entry.get(), "%d/%m/%y").strftime("%d/%m/%y")
            except ValueError:
                messagebox.showerror("Data invalída", "Porfavor, insira uma data valída")
                data= ""
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

# --- INICIALIZAÇÃO DA JANELA PRINCIPAL ---
if __name__ == "__main__":
    janela = tb.Window(themename="superhero")
    app = ListaDeTarefasApp(janela)
    janela.mainloop()
