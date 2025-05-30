
import sys
import subprocess
def instalar(pacote):
    try:
        __import__(pacote)
    except ImportError:
        print(f"Instalando {pacote}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

instalar('ttkbootstrap')
instalar('tkinter')
instalar('json')

import ttkbootstrap as tb
from tkinter import Toplevel, Entry, Button, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import os

ARQUIVO = "tarefas.json"

class ListaDeTarefasApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Lista de Tarefas")
        self.master.geometry("520x500")
        self.master.resizable(False, False)

        self.lista_de_tarefas = self.carregar_tarefas()

        self._criar_widgets()
        self.atualizar_lista()

    def carregar_tarefas(self):
        if os.path.exists(ARQUIVO):
            try:
                with open(ARQUIVO, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                messagebox.showwarning("Aviso", "Erro ao carregar tarefas. O arquivo será recriado.")
                return []
        return []

    def salvar_tarefas(self):
        try:
            with open(ARQUIVO, "w", encoding="utf-8") as f:
                json.dump(self.lista_de_tarefas, f, ensure_ascii=False, indent=2)
        except IOError:
            messagebox.showerror("Erro", "Falha ao salvar as tarefas.")

    def _criar_widgets(self):
        tb.Label(self.master, text="Minhas Tarefas", font=("Arial", 18, "bold")).pack(pady=10)

        entrada_frame = tb.Frame(self.master)
        entrada_frame.pack(pady=5)

        self.campo_entrada = tb.Entry(entrada_frame, width=40)
        self.campo_entrada.pack(side="left", padx=(0, 10))
        self.campo_entrada.focus()
        self.campo_entrada.bind('<Return>', lambda event: self.adicionar_tarefa())

        self.btn_adicionar = tb.Button(entrada_frame, text="Limpar", bootstyle="danger", command=self.limpar_lista)
        self.btn_adicionar.pack(side="left")

        self.container_tarefas = tb.Frame(self.master)
        self.container_tarefas.pack(pady=10, fill="both", expand=True)

    def atualizar_lista(self):
        for widget in self.container_tarefas.winfo_children():
            widget.destroy()

        for indice, item in enumerate(self.lista_de_tarefas):
            self._adicionar_linha(item, indice)

    def _adicionar_linha(self, item, indice):
        frame = tb.Frame(self.container_tarefas)
        frame.pack(fill="x", pady=2, padx=10)

        status = "☑" if item["feito"] else "☐"
        tarefa_label = tb.Label(frame, text=f"{status} {item['tarefa']}", font=("Arial", 12), anchor="w")
        tarefa_label.pack(side="left", fill="x", expand=True)
        tarefa_label.bind("<Button-1>", lambda e, i=indice: self.toggle_feito(i))

        btn_editar = tb.Button(frame, text="✏️", width=2, bootstyle="secondary", command=lambda i=indice: self.editar_tarefa(i))
        btn_editar.pack(side="right", padx=2)

        btn_excluir = tb.Button(frame, text="🗑️", width=2, bootstyle="danger", command=lambda i=indice: self.apagar_tarefa(i))
        btn_excluir.pack(side="right", padx=2)

    def adicionar_tarefa(self):
        texto = self.campo_entrada.get().strip()
        if texto:
            self.lista_de_tarefas.append({"tarefa": texto, "feito": False})
            self.salvar_tarefas()
            self.atualizar_lista()
            self.campo_entrada.delete(0, tb.END)
        else:
            messagebox.showinfo("Atenção", "Digite algo para adicionar.")

    def toggle_feito(self, indice):
        self.lista_de_tarefas[indice]["feito"] = not self.lista_de_tarefas[indice]["feito"]
        self.salvar_tarefas()
        self.atualizar_lista()

    def editar_tarefa(self, indice):
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
                if janela_editar.winfo_exists():
                    janela_editar.destroy()
            else:
                messagebox.showwarning("Aviso", "O texto não pode ficar vazio.")

        Button(janela_editar, text="salvar", command=salvar).pack()
        
    def apagar_tarefa(self, indice):
        resposta = messagebox.askyesno("Confirmar", "Deseja apagar essa tarefa?")
        if resposta:
            self.lista_de_tarefas.pop(indice)
            self.salvar_tarefas()
            self.atualizar_lista()
    
    def limpar_lista(self,):
        resposta = messagebox.askyesno("Confirmar", "Deseja limpar a lista de tarefas?")
        if resposta:
            resposta2 = messagebox.askyesno("confirmar", "essa ação sera INREVERSIVEL, tem certeza absoluta???")
            if resposta2:
                self.lista_de_tarefas = []
                self.salvar_tarefas()
                self.atualizar_lista()

if __name__ == "__main__":
    janela = tb.Window(themename="superhero")
    app = ListaDeTarefasApp(janela)
    janela.mainloop()
