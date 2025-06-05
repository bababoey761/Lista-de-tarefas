
# Lista de Tarefas - Aplicação com Interface Gráfica em Python 📝

Este projeto é uma aplicação de **lista de tarefas com interface gráfica** desenvolvida em Python utilizando a biblioteca `ttkbootstrap`. Ele permite adicionar, editar, marcar como concluída e remover tarefas com datas associadas, salvando os dados em um arquivo `.json` local.

## 🎯 Objetivo

Desenvolver uma aplicação de Lista de Tarefas com interface amigável e moderna que possibilite ao usuário organizar suas atividades do dia a dia.

## 👥 Divisão de Tarefas

O projeto foi dividido entre **3 integrantes**, conforme os blocos abaixo:

### 👤 Pessoa 1 - Instalação e Dados
- Instalação automática de bibliotecas necessárias (`ttkbootstrap`, `tkinter`, `json`).
- Carregamento e salvamento de tarefas em JSON.
- Organização do arquivo `tarefas.json` para persistência de dados.

### 👤 Pessoa 2 - Interface Gráfica
- Construção da interface com `ttkbootstrap`.
- Campos de entrada de data e tarefa.
- Área de exibição de tarefas com destaque por data.
- Botões de ação: adicionar, limpar, editar e apagar tarefas.

### 👤 Pessoa 3 - Lógica e Funcionalidade
- Adicionar, editar, remover e marcar tarefas como feitas.
- Validação de data.
- Atualização da interface após ações.
- Confirmações para ações destrutivas (como limpar a lista).

## 📦 Tecnologias e Bibliotecas

- Python 3.x
- ttkbootstrap (UI moderna baseada em tkinter)
- json, datetime, os, sys, subprocess

## 💻 Como Executar

1. Certifique-se de ter Python instalado.
2. Execute o script Python:

```bash
python "prova_2(lista de tarefas).py"
```

3. A janela da lista de tarefas será exibida.

## 💾 Armazenamento de Dados

As tarefas são armazenadas no arquivo `tarefas.json`, com o seguinte formato:

```json
[
  {
    "tarefa": "Estudar para a prova",
    "feito": false,
    "data": "05/06/25"
  }
]
```

## 🔧 Funcionalidades

- ✅ Marcar tarefa como concluída
- 📝 Editar texto da tarefa
- 🗑 Remover tarefa
- 📅 Associar data à tarefa (com validação)
- ⚠️ Limpeza de todas as tarefas com confirmação dupla

## 📌 Observações

- A data deve estar no formato **DD/MM/AA**.
- A interface responde dinamicamente às ações do usuário.
- A aplicação salva os dados localmente para uso contínuo.

## 🚀 Melhorias Futuras

- Ordenação por data ou prioridade
- Filtro por tarefas concluídas ou pendentes
- Backup/exportação de tarefas

---

Projeto desenvolvido colaborativamente por 3 participantes para fins educacionais e demonstrativos.
