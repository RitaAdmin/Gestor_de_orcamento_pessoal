#importar a biblioteca tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk, Toplevel,Frame,Label,Entry,Button
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import DateEntry

#importar pillow
from PIL import Image, ImageTk
from PIL import ImageDraw

#importar do ficheiro operacoes
from operacoes import inserir_receita, inserir_gastos, ver_dados_gastos, ver_dados_receita, saldo_atual, total_gastos_por_categoria, ver_dados_categoria, inserir_categoria, saldo_por_periodo, atualizar_receita, editar_gasto, eliminar_receita, eliminar_gastos


#importar barra de progresso do tkinter
from tkinter.ttk import Progressbar

#importar matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

#importar pandas
import pandas as pd

#importar datas
from datetime import datetime
from operacoes import saldo_por_periodo


# Definicao das cores da interface (cores do colorpicker)
co0="#1b1b1c" #preto
co1="#f7f7fa" #branco
co2="#3a86ff" # Azul 
co3="#ffbe0b" # Amarelo
co4="#163338" # Rosa
co5="#8338ec" # Roxo
co6="#fb5607" # Laranja 
co7="#219ebc" # Azul claro
co8="#8ecae6" # Azul pastel
co9="#ea70a5" # Rosa claro

colours=["#2e2e2f",  "#d9dbdf", "#265ea6","#e0a800", "#b33a5a", "#6829b0","#d15406",  "#1b7287", "#7bb2d9", "#c96192"]


# Arredondar logo--------------------------------------------- ---
def imagem_arredondada(path, tamanho):
    imagem = Image.open(path).resize(tamanho).convert("RGBA")
    mascara = Image.new("L", tamanho, 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((0, 0, tamanho[0], tamanho[1]), fill=255)
    imagem.putalpha(mascara)
    return ImageTk.PhotoImage(imagem)

# Função para adicionar receitas ou gastos ---
def janela_adicionar(janela_principal, tipo):
    win = Toplevel(janela_principal)
    win.title(f"Adicionar {tipo.capitalize()}")
    win.geometry("300x300")

    Label(win, text="Nome:").pack()
    nome_entry = tk.Entry(win)
    nome_entry.pack()

    Label(win, text="Categoria:").pack()
    combo_categoria = ttk.Combobox(win)
    combo_categoria.pack()

    categorias_dict = {}

    def atualizar_categorias():
        nonlocal categorias_dict
        tipo_categoria = "despesa" if tipo == "gasto" else "receita"
        categorias = [c for c in ver_dados_categoria() if c[2] == tipo_categoria]
        categorias_dict = {f"{c[1]} (ID: {c[0]})": c[0] for c in categorias}
        combo_categoria['values'] = list(categorias_dict.keys())
        if categorias:
            combo_categoria.current(0)

    atualizar_categorias()

    Label(win, text="Descrição:").pack()
    descricao_entrada = Entry(win)
    descricao_entrada.pack()

    Label(win, text="Valor (€):").pack()
    valor_entrada = Entry(win)
    valor_entrada.pack()

    def salvar():
        nome = nome_entry.get()
        categoria_nome = combo_categoria.get()
        descricao = descricao_entrada.get()
        valor = valor_entrada.get()

        if not nome or not categoria_nome or not descricao or not valor:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios.")
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showwarning("Valor inválido", "O valor deve ser numérico.")
            return

        if categoria_nome not in categorias_dict:
            messagebox.showwarning("Erro", "Selecione uma categoria válida.")
            return

        categoria_id = categorias_dict[categoria_nome]

        if tipo == "receita":
            inserir_receita(nome, categoria_id, descricao, valor)
        else:
            inserir_gastos(nome, categoria_id, descricao, valor)

        messagebox.showinfo("Sucesso", f"{tipo.capitalize()} adicionada com sucesso!")
        win.destroy()

    Button(win, text="Salvar", command=salvar).pack(pady=10)

# Adicionar nova categoria ---
def janela_adicionar_categoria():
    win = Toplevel()
    win.title("Adicionar Categoria")
    win.geometry("300x200")

    Label(win, text="Nome da categoria:").pack()
    entry_nome = tk.Entry(win)
    entry_nome.pack()
    
    Label(win,text="Tipo").pack()
    tipo_combo=ttk.Combobox(win, values=["receita","despesa"])
    tipo_combo.pack()

    def salvar_categoria():
        nome = entry_nome.get()
        tipo=tipo_combo.get()
        if not nome or not tipo:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        inserir_categoria(nome, tipo)
        messagebox.showinfo("Sucesso", "Categoria adicionada com sucesso!")
        win.destroy()

    Button(win, text="Salvar", command=salvar_categoria).pack(pady=10)
# Calculo estatistico
def calcular_estatisticas_mensais():
    dados_receitas = ver_dados_receita()
    dados_gastos = ver_dados_gastos()

    df_receitas = pd.DataFrame(dados_receitas, columns=["ID", "Nome", "Categoria", "Descrição", "Data", "Valor"])
    df_gastos = pd.DataFrame(dados_gastos, columns=["ID", "Nome", "Categoria", "Descrição", "Data", "Valor"])

    # Converter coluna Data para datetime
    df_receitas["Data"] = pd.to_datetime(df_receitas["Data"])
    df_gastos["Data"] = pd.to_datetime(df_gastos["Data"])

    # Agrupar por mês
    receitas_mensais = df_receitas.resample("M", on="Data")["Valor"].sum()
    gastos_mensais = df_gastos.resample("M", on="Data")["Valor"].sum()

    # Últimos 3 meses
    ultimos_3_receitas = receitas_mensais.last("3M")
    media_receita = ultimos_3_receitas.mean() if not ultimos_3_receitas.empty else 0

    ultimos_3_gastos = gastos_mensais.last("3M")
    media_gasto = ultimos_3_gastos.mean() if not ultimos_3_gastos.empty else 0

    # Mês com maior gasto
    if not gastos_mensais.empty:
        mes_maior_gasto = gastos_mensais.idxmax().strftime("%B %Y")
        valor_maior_gasto = gastos_mensais.max()
    else:
        mes_maior_gasto = "N/D"
        valor_maior_gasto = 0

    # Tendência de gasto
    if len(gastos_mensais) >= 2:
        tendencia = "Aumentou" if gastos_mensais.iloc[-1] > gastos_mensais.iloc[-2] else "Reduziu"
    else:
        tendencia = "N/D"

    return {
        "media_receita": media_receita,
        "media_gasto": media_gasto,
        "maior_gasto_mes": mes_maior_gasto,
        "maior_gasto_valor": valor_maior_gasto,
        "tendencia": tendencia
    }


#Dashboard principal ---
def abrir_dashboard(nome_usuario):
    janela = Toplevel()
    janela.title("Dashboard - Gestão Financeira Pessoal")
    janela.geometry("1000x700")
    janela.configure(bg=co1)

    topo = Frame(janela, height=80, bg=co4)
    topo.pack(fill=tk.X)

    try:
        logo = imagem_arredondada("logo3.png", (50, 50))
        logo_label = tk.Label(topo, image=logo, bg=co4)
        logo_label.image = logo
        logo_label.pack(side=tk.LEFT, padx=10, pady=15)
    except:
        print("Erro ao carregar logo")

    Label(topo, text=f"Bem-vindo, {nome_usuario}!", font=("Verdana", 14), bg=co4, fg="white").pack(side=tk.LEFT, padx=10)

    notebook = ttk.Notebook(janela)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    frame_home = Frame(notebook, bg="white")
    frame_grafico = Frame(notebook, bg="white")
    frame_grafico_barra = Frame(notebook, bg="white")
    frame_estatisticas = Frame(notebook, bg="white")
    frame_exportar = Frame(notebook, bg="white")

    notebook.add(frame_home, text="Inserir dados")
    notebook.add(frame_grafico, text="Gráfico de Gastos")
    notebook.add(frame_grafico_barra, text="Gráfico por Categoria (Barras)")
    notebook.add(frame_estatisticas, text="Estatística")
    notebook.add(frame_exportar, text="Importar/Exportar")

    # Aba Resumo
    saldo = saldo_atual()
    Label(frame_home, text=f"Saldo Atual: €{saldo['saldo']:.2f}", bg="white", fg="green", font=("Verdana", 14)).pack(pady=10)
    Label(frame_home, text=f"Total em Receitas: €{saldo['receita']:.2f}", bg="white").pack()
    Label(frame_home, text=f"Total em Gastos: €{saldo['gastos']:.2f}", bg="white").pack()

    Button(frame_home, text="Adicionar Receita", command=lambda: janela_adicionar(janela, "receita")).pack(pady=5)
    Button(frame_home, text="Adicionar Gasto", command=lambda: janela_adicionar(janela, "gasto")).pack(pady=5)
    Button(frame_home, text="Adicionar Categoria", command=janela_adicionar_categoria).pack(pady=5)
    Button(frame_home, text="Gerir Lançamentos", command=janela_gerir_dados).pack(pady=5)
    

    # Aba Gráfico
    def desenhar_grafico():
        dados = total_gastos_por_categoria()
        if not dados:
            Label(frame_grafico, text="Nenhum dado para exibir o gráfico.", bg="white").pack(pady=20)
            return

        categorias = [linha[0] for linha in dados]
        valores = [linha[1] for linha in dados]

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(valores, labels=categorias, autopct='%1.1f%%')
        ax.set_title("Distribuição de Gastos por Categoria")

        grafico = FigureCanvasTkAgg(fig, master=frame_grafico)
        grafico.draw()
        grafico.get_tk_widget().pack()

    desenhar_grafico()
    plt.tight_layout()
    
     # Aba Gráfico de Barras
    def desenhar_grafico_barras():
        dados = total_gastos_por_categoria()
        if not dados:
            Label(frame_grafico_barra, text="Nenhum dado para exibir o gráfico.", bg="white").pack(pady=20)
            return

        categorias = [linha[0] for linha in dados]
        valores = [linha[1] for linha in dados]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(categorias, valores, color=co2)
        ax.set_ylabel("Valor (€)")
        ax.set_title("Total de Gastos por Categoria")
        ax.tick_params(axis='x', rotation=45)

        grafico = FigureCanvasTkAgg(fig, master=frame_grafico_barra)
        grafico.draw()
        grafico.get_tk_widget().pack()

    desenhar_grafico_barras()
    plt.tight_layout()
    
    # Aba Estatística ---
    def mostrar_estatisticas():
        stats = calcular_estatisticas_mensais()
        Label(frame_estatisticas, text="Estatística dos últimos 3 meses", font=("Verdana", 13, "bold"), bg="white").pack(pady=10)

        Label(frame_estatisticas, text=f"Média de Receitas: €{stats['media_receita']:.2f}", bg="white", font=("Verdana", 12)).pack(pady=3)
        Label(frame_estatisticas, text=f"Média de Gastos: €{stats['media_gasto']:.2f}", bg="white", font=("Verdana", 12)).pack(pady=3)
        Label(frame_estatisticas, text=f"Mês com Maior Gasto: {stats['maior_gasto_mes']} (€{stats['maior_gasto_valor']:.2f})", bg="white", font=("Verdana", 12)).pack(pady=3)
        Label(frame_estatisticas, text=f"Tendência de Gastos: {stats['tendencia']}", bg="white", font=("Verdana", 12)).pack(pady=3)
    mostrar_estatisticas()
       
    def mostrar_tendencia():
        df_r = pd.DataFrame(ver_dados_receita(), columns=["ID", "Nome", "Categoria", "Descrição", "Data", "Valor"])
        df_g = pd.DataFrame(ver_dados_gastos(), columns=["ID", "Nome", "Categoria", "Descrição", "Data", "Valor"])

        df_r["Data"] = pd.to_datetime(df_r["Data"])
        df_g["Data"] = pd.to_datetime(df_g["Data"])

        receitas_mensais = df_r.resample("M", on="Data")["Valor"].sum()
        gastos_mensais = df_g.resample("M", on="Data")["Valor"].sum()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(receitas_mensais.index, receitas_mensais.values, label="Receitas", marker="o", color=co2)
        ax.plot(gastos_mensais.index, gastos_mensais.values, label="Gastos", marker="o", color=co6)
        ax.set_title("Tendência de Receitas e Gastos Mensais")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Valor (€)")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=frame_estatisticas)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    mostrar_tendencia()
    plt.tight_layout()
    
    # Aba Exportar
    def exportar_excel():
        dados = ver_dados_gastos()
        df = pd.DataFrame(dados, columns=["ID", "Nome", "Categoria", "Descrição", "Data", "Valor"])
        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if file:
            df.to_excel(file, index=False)
            messagebox.showinfo("Sucesso", "Dados exportados com sucesso!")

    ttk.Button(frame_exportar, text="Exportar Gastos para Excel", command=exportar_excel).pack(pady=20)
    
    # ABA FILTRO POR DATA ---
    frame_filtro = Frame(notebook, bg="white")
    notebook.add(frame_filtro, text="Filtrar por Data")

    Label(frame_filtro, text="Data de Início (YYYY-MM-DD):", bg="white").pack(pady=5)
    data_inicio_entry = Entry(frame_filtro)
    data_inicio_entry.pack()

    Label(frame_filtro, text="Data de Fim (YYYY-MM-DD):", bg="white").pack(pady=5)
    data_fim_entry = Entry(frame_filtro)
    data_fim_entry.pack()

    resultado_label = Label(frame_filtro, text="", bg="white", font=("Verdana", 12))
    resultado_label.pack(pady=10)

    def aplicar_filtro():
        inicio = data_inicio_entry.get()
        fim = data_fim_entry.get()
        try:
            datetime.strptime(inicio, "%Y-%m-%d")
            datetime.strptime(fim, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use YYYY-MM-DD.")
            return

        resumo = saldo_por_periodo(inicio, fim)
        resultado_label.config(text=f"Receitas: €{resumo['receita']:.2f}\nGastos: €{resumo['gastos']:.2f}\nSaldo: €{resumo['saldo']:.2f}")

    Button(frame_filtro, text="Aplicar Filtro", command=aplicar_filtro).pack(pady=10)

#EXPORTAR RECEITAS PARA EXCEL ---
    def exportar_receitas_excel():
        from operacoes import ver_dados_receita
        dados = ver_dados_receita()
        df = pd.DataFrame(dados, columns=["ID", "Nome", "Categoria", "Descrição", "Data", "Valor"])
        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if file:
            df.to_excel(file, index=False)
            messagebox.showinfo("Sucesso", "Receitas exportadas com sucesso!")

    Button(frame_exportar, text="Exportar Receitas para Excel", command=exportar_receitas_excel).pack(pady=10)

# RESUMO POR CATEGORIA ---
    frame_resumo = Frame(notebook, bg="white")
    notebook.add(frame_resumo, text="Resumo por Categoria")

    def mostrar_resumo():
        dados = total_gastos_por_categoria()
        if not dados:
            Label(frame_resumo, text="Nenhum gasto registrado.", bg="white").pack()
            return
        for nome, valor in dados:
            Label(frame_resumo, text=f"{nome}: €{valor:.2f}", bg="white").pack(anchor='w', padx=20)

    mostrar_resumo()

#ffff
# Arredondar logo

def imagem_arredondada(path, tamanho):
    imagem = Image.open(path).resize(tamanho).convert("RGBA")
    mascara = Image.new("L", tamanho, 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((0, 0, tamanho[0], tamanho[1]), fill=255)
    imagem.putalpha(mascara)
    return ImageTk.PhotoImage(imagem)

# Edição e exclusão ---
def janela_gerir_dados():
    win = Toplevel()
    win.title("Gerir Lançamentos")
    win.geometry("800x450")

    aba = ttk.Notebook(win)
    frame_receitas = Frame(aba)
    frame_gastos = Frame(aba)
    aba.add(frame_receitas, text="Receitas")
    aba.add(frame_gastos, text="Gastos")
    aba.pack(expand=True, fill="both")

    def atualizar_tree(tree, tipo):
        tree.delete(*tree.get_children())
        dados = sorted(ver_dados_receita(), key=lambda x: x[4], reverse=True) if tipo == "receita" else sorted(ver_dados_gastos(), key=lambda x: x[4], reverse=True)
        for item in dados:
            tree.insert("", "end", values=item)

    def editar_lancamento(tree, tipo):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um item para editar.")
            return

        valores = tree.item(item, "values")
        edit_win = Toplevel()
        edit_win.title("Editar")

        Label(edit_win, text="Nome:").pack()
        entry_nome = Entry(edit_win)
        entry_nome.insert(0, valores[1])
        entry_nome.pack()

        Label(edit_win, text="Descrição:").pack()
        entry_desc = Entry(edit_win)
        entry_desc.insert(0, valores[3])
        entry_desc.pack()

        Label(edit_win, text="Valor:").pack()
        entry_valor = Entry(edit_win)
        entry_valor.insert(0, valores[5])
        entry_valor.pack()

        def salvar():
            nome = entry_nome.get()
            desc = entry_desc.get()
            try:
                valor = float(entry_valor.get())
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido.")
                return

            if tipo == "receita":
                atualizar_receita(valores[0], nome, valores[2], desc, valor)
            else:
                editar_gasto(valores[0], nome, valores[2], desc, valor)

            messagebox.showinfo("Sucesso", "Atualizado!")
            atualizar_tree(tree, tipo)
            edit_win.destroy()

        ttk.Button(edit_win, text="Salvar", command=salvar).pack(pady=10)

    def deletar_lancamento(tree, tipo):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            return

        valores = tree.item(item, "values")
        if not messagebox.askyesno("Confirmação", "Deseja realmente excluir este lançamento?"):
            return

        if tipo == "receita":
            eliminar_receita(valores[0])
        else:
            eliminar_gastos(valores[0])

        atualizar_tree(tree, tipo)
        messagebox.showinfo("Sucesso", "Excluído com sucesso.")

    #RECEITAS ---
    Label(frame_receitas, text="Buscar por nome ou descrição:").pack(pady=5)
    busca_r_entry = Entry(frame_receitas)
    busca_r_entry.pack()

    def filtrar_receitas():
        filtro = busca_r_entry.get().lower()
        tree_r.delete(*tree_r.get_children())
        dados = sorted(ver_dados_receita(), key=lambda x: x[4], reverse=True)
        for item in dados:
            if filtro in item[1].lower() or filtro in item[3].lower():
                tree_r.insert("", "end", values=item)

    ttk.Button(frame_receitas, text="Buscar", command=filtrar_receitas).pack(pady=5)

    container_r = Frame(frame_receitas)
    container_r.pack(fill="both", expand=True)

    tree_r = ttk.Treeview(container_r, columns=("ID", "Nome", "Categoria", "Descrição", "Data", "Valor"), show="headings")
    for col in tree_r["columns"]:
        tree_r.heading(col, text=col)
    tree_r.pack(side=LEFT, fill="both", expand=True)

    scrollbar_r = Scrollbar(container_r, orient="vertical", command=tree_r.yview)
    scrollbar_r.pack(side=RIGHT, fill=Y)
    tree_r.configure(yscrollcommand=scrollbar_r.set)

    btns_r = Frame(frame_receitas)
    btns_r.pack(pady=5)
    ttk.Button(btns_r, text="Editar", command=lambda: editar_lancamento(tree_r, "receita")).pack(side=LEFT, padx=5)
    ttk.Button(btns_r, text="Excluir", command=lambda: deletar_lancamento(tree_r, "receita")).pack(side=LEFT, padx=5)

    atualizar_tree(tree_r, "receita")

    # GASTOS ---
    Label(frame_gastos, text="Buscar por nome ou descrição:").pack(pady=5)
    busca_g_entry = Entry(frame_gastos)
    busca_g_entry.pack()

    def filtrar_gastos():
        filtro = busca_g_entry.get().lower()
        tree_g.delete(*tree_g.get_children())
        dados = sorted(ver_dados_gastos(), key=lambda x: x[4], reverse=True)
        for item in dados:
            if filtro in item[1].lower() or filtro in item[3].lower():
                tree_g.insert("", "end", values=item)

    ttk.Button(frame_gastos, text="Buscar", command=filtrar_gastos).pack(pady=5)

    container_g = Frame(frame_gastos)
    container_g.pack(fill="both", expand=True)

    tree_g = ttk.Treeview(container_g, columns=("ID", "Nome", "Categoria", "Descrição", "Data", "Valor"), show="headings")
    for col in tree_g["columns"]:
        tree_g.heading(col, text=col)
    tree_g.pack(side=LEFT, fill="both", expand=True)

    scrollbar_g = Scrollbar(container_g, orient="vertical", command=tree_g.yview)
    scrollbar_g.pack(side=RIGHT, fill=Y)
    tree_g.configure(yscrollcommand=scrollbar_g.set)

    btns_g = Frame(frame_gastos)
    btns_g.pack(pady=5)
    ttk.Button(btns_g, text="Editar", command=lambda: editar_lancamento(tree_g, "gasto")).pack(side=LEFT, padx=5)
    ttk.Button(btns_g, text="Excluir", command=lambda: deletar_lancamento(tree_g, "gasto")).pack(side=LEFT, padx=5)

    atualizar_tree(tree_g, "gasto")
   
    