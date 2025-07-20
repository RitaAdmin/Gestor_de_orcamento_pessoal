#importar a biblioteca tkinter
from tkinter import *
from tkinter import Tk, ttk

#importar pillow
from PIL import Image, ImageTk

#importar do ficheiro operacoes
from operacoes import ver_dados_categoria, inserir_receita, ver_dados_receita


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

#criar janela do interface
janela=Tk()
janela.title("Gestor de finaças pessoais")
janela.geometry('1100x750')
janela.configure(background="#d9dbdf")
janela.resizable(width=False, height=False)

style=ttk.Style(janela)
style.theme_use("clam") # escolhi clam por ser o mais versatil de todos

#criar frames da janela---------------------------------------------------------------------------------------------
#titulo
frameCima = Frame(janela, width=1100, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

#Meio - Inserir dados
frameMeio = Frame(janela, width=1100, height=200, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

#baixo_filtros ?

frameBaixo = Frame(janela, width=1100, height=500, bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=1, padx=0, sticky=NSEW)


#Conteudo dos frames
#framecima: adicionei pip install pillow
#ADICIONAR LOGO
app_img=Image.open('logo3.png')
app_img = app_img.resize((60, 45)) #para redimensionar o logo
app_img=ImageTk.PhotoImage(app_img)

#label
app_logo=Label(frameCima,image=app_img,text="Gestor de Finanças Pessoais", compound=LEFT, padx=10, anchor=NW, relief= "flat", font=('Verdana', 20, 'bold'), bg=co1, fg=co4) #custumizaçao
app_logo.place(relx=0.5,rely=0.5, anchor=CENTER) # dá as coordenada onde titulo deve ficar

#ajajajaja 
# ---- Labels e Entradas para Receita ----
Label(frameMeio, text="Nome:", bg=co1).place(x=10, y=10)
entry_nome = Entry(frameMeio, width=25)
entry_nome.place(x=100, y=10)

Label(frameMeio, text="Categoria:", bg=co1).place(x=10, y=40)
combo_categoria = ttk.Combobox(frameMeio, width=22)
combo_categoria.place(x=100, y=40)
combo_categoria['values'] = [cat[1] for cat in ver_dados_categoria()]  # Exibe nomes

Label(frameMeio, text="Descrição:", bg=co1).place(x=10, y=70)
entry_descricao = Entry(frameMeio, width=25)
entry_descricao.place(x=100, y=70)

Label(frameMeio, text="Valor:", bg=co1).place(x=10, y=100)
entry_valor = Entry(frameMeio, width=25)
entry_valor.place(x=100, y=100)

def adicionar_receita():
    nome = entry_nome.get()
    categoria_nome = combo_categoria.get()
    descricao = entry_descricao.get()
    valor = entry_valor.get()

    # Obter o ID da categoria com base no nome
    categorias = ver_dados_categoria()
    categoria_id = next((c[0] for c in categorias if c[1] == categoria_nome), None)

    if nome and categoria_id and valor:
        try:
            inserir_receita(nome, categoria_id, descricao, float(valor))
            atualizar_tabela()
        except:
            print("Erro ao adicionar receita.")

btn_receita = Button(frameMeio, text="Adicionar Receita", command=adicionar_receita, bg=co3, fg=co0)
btn_receita.place(x=100, y=140)

tabela = ttk.Treeview(frameBaixo, columns=('ID', 'Nome', 'Categoria', 'Descrição', 'Data', 'Valor'), show='headings')
tabela.heading('ID', text='ID')
tabela.heading('Nome', text='Nome')
tabela.heading('Categoria', text='Categoria')
tabela.heading('Descrição', text='Descrição')
tabela.heading('Data', text='Data')
tabela.heading('Valor', text='Valor')
tabela.place(x=0, y=0, width=1100, height=480)
#Função para atualizar tabela
def atualizar_tabela():
    for i in tabela.get_children():
        tabela.delete(i)

    dados = ver_dados_receita()
    categorias = {c[0]: c[1] for c in ver_dados_categoria()}

    for item in dados:
        id_, nome, categoria_id, descricao, data, valor = item
        nome_categoria = categorias.get(categoria_id, "Desconhecido")
        tabela.insert('', 'end', values=(id_, nome, nome_categoria, descricao, data, valor))

#Estilo visual melhorado (opcional)
style.configure("Treeview.Heading", font=('Verdana', 10, 'bold'), background=co2, foreground=co1)
style.configure("Treeview", font=('Verdana', 9), background=co1, foreground=co0, rowheight=25)


#gastos
# ---- Labels e Entradas para Gastos ----
Label(frameMeio, text="Nome:", bg=co1).place(x=400, y=10)
entry_nome_gasto = Entry(frameMeio, width=25)
entry_nome_gasto.place(x=490, y=10)

Label(frameMeio, text="Categoria:", bg=co1).place(x=400, y=40)
combo_categoria_gasto = ttk.Combobox(frameMeio, width=22)
combo_categoria_gasto.place(x=490, y=40)
combo_categoria_gasto['values'] = [cat[1] for cat in ver_dados_categoria() if cat[2] == 'despesa']

Label(frameMeio, text="Descrição:", bg=co1).place(x=400, y=70)
entry_descricao_gasto = Entry(frameMeio, width=25)
entry_descricao_gasto.place(x=490, y=70)

Label(frameMeio, text="Valor:", bg=co1).place(x=400, y=100)
entry_valor_gasto = Entry(frameMeio, width=25)
entry_valor_gasto.place(x=490, y=100)

def adicionar_gasto():
    nome = entry_nome_gasto.get()
    categoria_nome = combo_categoria_gasto.get()
    descricao = entry_descricao_gasto.get()
    valor = entry_valor_gasto.get()

    # Obter o ID da categoria com base no nome
    categorias = ver_dados_categoria()
    categoria_id = next((c[0] for c in categorias if c[1] == categoria_nome), None)

    if nome and categoria_id and valor:
        try:
            inserir_gasto(nome, categoria_id, descricao, float(valor))
            atualizar_tabela()
        except Exception as e:
            print("Erro ao adicionar gasto:", e)

btn_gasto = Button(frameMeio, text="Adicionar Gasto", command=adicionar_gasto, bg=co4, fg=co1)
btn_gasto.place(x=490, y=140)




janela.mainloop()