
#fica para fazer o login do usuario

#importar a biblioteca tkinter
from tkinter import *
from tkinter import Tk, ttk

#importar pillow
from PIL import Image, ImageTk

#importar do ficheiro operacoes ou basedados(usuario) (((VERRRRRRRRRRRRR)))
from operacoes import ver_dados_categoria, inserir_receita, ver_dados_receita



# Definicao das cores da interface (cores do colorpicker)
co0="#1b1b1c" #preto
co1="#f7f7fa" #branco
co2="#3a86ff" # Azul 
co3="#ffbe0b" # Amarelo
co4="#163338" # VERDE LOGO
co5="#415B60" # VERDE LOGO
co6="#fb5607" # Laranja 
co7="#219ebc" # Azul claro
co8="#8ecae6" # Azul pastel
co9="#ea70a5" # Rosa claro

colours=["#2e2e2f",  "#d9dbdf", "#265ea6","#e0a800", "#b33a5a", "#6829b0","#d15406",  "#1b7287", "#7bb2d9", "#c96192"]

#criar janela do interface
janela=Tk()
janela.title("Gestor de finaças pessoais")
janela.geometry('1100x750')
janela.configure(background=co1)
janela.resizable(width=False, height=False)

style=ttk.Style(janela)
style.theme_use("clam") # escolhi clam por ser o mais versatil de todos


##criar frames da janela---------------------------------------------------------------------------------------------
frameCima = Frame(janela, width=1100, height=50, bg=co5, relief="flat")
frameCima.grid(row=0, column=0)

#baixo_filtros ?
frameBaixo = Frame(janela, width=1100, height=500, bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=1, padx=0, sticky=NSEW)









janela.mainloop()