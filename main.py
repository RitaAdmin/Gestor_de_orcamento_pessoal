#importar a biblioteca tkinter
from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox #importar mensagebox
import tkinter as tk

#importar pillow(para imagem do logo)
from PIL import Image, ImageTk
from PIL import ImageDraw


#importar do ficheiro operacoes ou basedados(usuario) 
from operacoes import verificar_login,criar_usuario
from dashboard import abrir_dashboard


#Customizaçaão---------------------------------------------------------------------..............................................
# Definicao das cores da interface (cores do colorpicker).
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
janela.title("Gestor de Finanças Pessoais")
janela.geometry('400x500')
janela.configure(background=co1)
janela.resizable(width=False, height=False)

style=ttk.Style(janela)
style.theme_use("clam") # escolhi clam por ser o mais versatil de todos

# ENTRADA login-------................................................................................................................................
# Login
login_email_entry = Entry(janela, width=35)
login_senha_entry = Entry(janela, show="*", width=35)

# Registro
registo_nome_entry = Entry(janela, width=35)
registo_email_entry = Entry(janela, width=35)
registo_senha_entry = Entry(janela, show="*", width=35)
registo_confirma_entry = Entry(janela, show="*", width=35)

#funçao para mostrar logo
def mostrar_logo():
    try:
        # Carregar a imagem
        imagem_logo = Image.open("logo3.png").convert("RGBA")
        imagem_logo = imagem_logo.resize((150, 150), Image.LANCZOS)

        # Criar uma máscara circular
        mask = Image.new("L", (150, 150), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 150, 150), fill=255)

        # Aplicar a máscara circular
        imagem_logo.putalpha(mask)

        # Converter para formato que o Tkinter entende
        logo = ImageTk.PhotoImage(imagem_logo)

        # Exibir a imagem
        logo_label = Label(janela, image=logo, bg=co1)
        logo_label.image = logo  # Prevenir que o garbage collector apague
        logo_label.pack(pady=5)

    except Exception as e:
        print(f"Erro ao carregar o logotipo: {e}")


#Funçao para limpar janela----------------------------------......................................................................
def limpar_tela():
    for widget in janela.winfo_children():
        widget.pack_forget()

#T
#Campo de entrada
def fazer_login():
    email = login_email_entry.get()
    senha = login_senha_entry.get()

    usuario = verificar_login(email, senha)
    if usuario:
        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        janela.destroy()
        abrir_dashboard_com_usuario(usuario[1])  # Nome do usuário
    else:
        messagebox.showerror("Erro", "Email ou senha inválidos!")
        
def registrar():
    nome = registo_nome_entry.get()
    email = registo_email_entry.get()
    senha = registo_senha_entry.get()
    confirma = registo_confirma_entry.get()

    if not nome or not email or not senha or not confirma:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    if senha != confirma:
        messagebox.showerror("Erro", "As senhas não coincidem.")
        return

    try:
        criar_usuario(nome, email, senha)
        messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
        mostrar_login()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao registrar: {e}")

#funcao abrir dashboard
def abrir_dashboard_com_usuario(nome_usuario):
    try:
        abrir_dashboard(nome_usuario)
    except ImportError:
        messagebox.showwarning("Erro!", "O Dashboard ainda não está instalado")
        
    
# janelas...........................................................................................................................
#login
def mostrar_login():
    limpar_tela()
    mostrar_logo()  # Adiciona logo no topo da tela

    Label(janela, text="Login", font=('Verdana', 18), bg=co1).pack(pady=10)

    Label(janela, text="Email:", bg=co1).pack()
    login_email_entry.pack()

    Label(janela, text="Senha:", bg=co1).pack()
    login_senha_entry.pack()

    Button(janela, text="Entrar", command=fazer_login, bg=co2, fg="white", width=20).pack(pady=10)
    Button(janela, text="Criar Conta", command=mostrar_registro, bg=co7, fg="white", width=20).pack()

#janela de registo
def mostrar_registro():
    limpar_tela()
    mostrar_logo()  # Também mostra logo na tela de registro

    Label(janela, text="Criar Conta", font=('Verdana', 18), bg=co1).pack(pady=10)

    Label(janela, text="Nome:", bg=co1).pack()
    registo_nome_entry.pack()

    Label(janela, text="Email:", bg=co1).pack()
    registo_email_entry.pack()

    Label(janela, text="Senha:", bg=co1).pack()
    registo_senha_entry.pack()

    Label(janela, text="Confirmar Senha:", bg=co1).pack()
    registo_confirma_entry.pack()

    Button(janela, text="Registrar", command=registrar, bg=co2, fg="white", width=20).pack(pady=10)
    Button(janela, text="Voltar ao Login", command=mostrar_login, bg="#aaa", width=20).pack()


# INICIAR----------------------------------
mostrar_login()
janela.mainloop()     

