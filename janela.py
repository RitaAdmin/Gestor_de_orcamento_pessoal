#importar a biblioteca tkinter
from tkinter import *
from tkinter import Tk, ttk

#importar pillow
from PIL import Image, ImageTk

#importar do ficheiro operacoes
from operacoes import ver_dados_categoria, inserir_receita, ver_dados_receita

#importar barra de progresso do tkinter
from tkinter.ttk import Progressbar

#importar matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure





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

#label (logo e titulo)
app_logo=Label(frameCima,image=app_img,text="Gestor de Finanças Pessoais", compound=LEFT, padx=10, anchor=NW, relief= "flat", font=('Verdana', 20, 'bold'), bg=co1, fg=co4) #custumizaçao
app_logo.place(relx=0.5,rely=0.5, anchor=CENTER) # dá as coordenada onde titulo deve ficar


#framemeio:
#barra de progesso do dinheiro gasto
def percentagem():
    label_nome= Label(frameMeio, text="Percentagem da Receita consumida", height=1, anchor=NW, font=('Verdana','12'),bg=co1, fg=co4)
    label_nome.place(x=7,y=5)
    
    bar=Progressbar(frameMeio, length=220)
    bar.place(x=10,y=35)
    bar['value']=50
    
    #style da barra de progressao
    style=ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background= 'col4')
    style.configure("TProgressbar",thickness=30)
    bar=Progressbar(frameMeio, length=220, style='black.Horizontal.TProgressbar')
    
    #label da percentagem
    valor=50 #provisorio
    label_percentagem= Label(frameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=('Verdana','12'),bg=co1, fg=co4)
    label_percentagem.place(x=235,y=35)




#para aparecer na janela
percentagem() #chamar a funcao para apacecer
janela.mainloop()