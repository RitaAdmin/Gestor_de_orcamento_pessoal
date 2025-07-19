#importar a biblioteca tkinter
from tkinter import *
from tkinter import Tk, ttk

#importar pillow
from PIL import Image, ImageTk


# Definicao das cores da interface (cores do colorpicker)
co0="#1b1b1c" #preto
co1="#f7f7fa" #branco
co2="#3a86ff" # Azul 
co3="#ffbe0b" # Amarelo
co4="#fa056f" # Rosa
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
app_logo=Label(frameCima,image=app_img,text="Gestor de Finanças Pessoais", width=900, compound=LEFT, padx=5, anchor=NW, relief= "flat", font=('Verdana', 20, 'bold'), bg=co1, fg=co4) #custumizaçao
app_logo.place(x=0,y=0)










janela.mainloop()