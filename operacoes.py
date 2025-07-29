#importar SQLITE
import sqlite3 as lite
#importar data
from datetime import datetime

#criar conexao com banco de dados
con=lite.connect('dados.gestao-financeira-pessoal')

#Importar hashib (password usuario)
import hashlib





#Funcçoes para inserir dados-------------------------------------------------------------------------------------------------

#inserir categorias
def inserir_categoria(nome_categoria, tipo): 
    try:
        with con:
            cur=con.cursor()
            query="INSERT INTO Categoria (nome, tipo) VALUES (?,?)"
            cur.execute(query, (nome_categoria,tipo))
    except Exception as e:
        print("Erro! Existe um erro ao inserir a categoria",e)

#inserir receita
def inserir_receita(nome, categoria_id, descricao, valor): 
    
    data = datetime.now().strftime("%Y-%m-%d")
    
    with con:
        cur=con.cursor()
        query="INSERT INTO Receita (nome, categoria_id, descricao, adicionado_em, valor) VALUES (?,?,?,?,?)"
        cur.execute(query, (nome, categoria_id, descricao, data, valor))
    

#inserir gastos
def inserir_gastos(nome, categoria_id, descricao,valor): 
    
    data = datetime.now().strftime("%Y-%m-%d")
    
    with con:
        cur=con.cursor()
        query="INSERT INTO Gastos (nome, categoria_id, descricao, subtraido_em, valor) VALUES (?,?,?,?,?)"
        cur.execute(query, (nome, categoria_id, descricao, data, valor))

#Funcçoes para apagar dados---------------------------------------------------------------------------------------------

# Eliminar categoria
def eliminar_categoria(categoria_id):
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM Receita WHERE categoria_id = ?", (categoria_id,))
        receita = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Gastos WHERE categoria_id = ?", (categoria_id,))
        gastos = cur.fetchone()[0]

        if receita > 0 or gastos > 0:
            print("Não é possível eliminar a categoria pois ela está associada a receitas ou gastos.")
        else:
            query = "DELETE FROM Categoria WHERE ID = ?"
            cur.execute(query, (categoria_id,))

#Eliminar Receita
def eliminar_receita(receita_id):
    with con:
        cur=con.cursor()
        query="DELETE FROM Receita WHERE id= ?"
        cur. execute(query, (receita_id,))

#Eliminar gastos
def eliminar_gastos(gastos_id):
    with con:
        cur=con.cursor()
        query="DELETE FROM Gastos WHERE id= ?"
        cur. execute(query, (gastos_id,))

       
#Eliminar usuario
def eliminar_usuario(usuario_id):
    with con:
        cur=con.cursor()
        query="DELETE FROM Usuario WHERE id= ?"
        cur. execute(query, (usuario_id,))

#funcoes para ver dados----------------------------------------------------------------------------------------

#Categoria
def ver_dados_categoria():
    lista_itens=[]
    with con:
        cur= con.cursor()
        cur.execute("SELECT*FROM Categoria")
        linha=cur.fetchall()
        for l in linha: 
            lista_itens.append(l)
    
    return lista_itens
    
#Ver os dados das Receita
def ver_dados_receita():
    lista_itens=[]
    with con:
        cur= con.cursor()
        cur.execute("SELECT*FROM Receita")
        linha=cur.fetchall()
        for l in linha: 
            lista_itens.append(l)
    
    return lista_itens

#Ver os dados de Gastos
def ver_dados_gastos():
    lista_itens=[]
    with con:
        cur= con.cursor()
        cur.execute("SELECT*FROM Gastos")
        linha=cur.fetchall()
        for l in linha: 
            lista_itens.append(l)
    
    return lista_itens

#Atualizar os registos---------------------------------------------------------------------------
#atualizar categoria
def atualizar_categoria(categoria_id, novo_nome, novo_tipo):
    with con:
        cur = con.cursor()
        query = ("UPDATE Categoria SET nome = ?, tipo = ? WHERE ID = ?")
        cur.execute(query, (novo_nome, novo_tipo, categoria_id))
        
#atualizar receita
def atualizar_receita(receita_id, novo_nome, nova_categoria_id, nova_descricao, novo_valor):
    with con:
        cur = con.cursor()
        query = ("UPDATE Receita SET nome = ?, categoria_id = ?, descricao = ?, valor = ? WHERE ID = ?")
        cur.execute(query, (novo_nome, nova_categoria_id, nova_descricao, novo_valor, receita_id))

#atualizar gastos
def editar_gasto(gasto_id, novo_nome, nova_categoria_id, nova_descricao, novo_valor):
    with con:
        cur = con.cursor()
        query = ("UPDATE Gastos SET nome = ?, categoria_id = ?, descricao = ?, valor = ? WHERE ID = ?")
        cur.execute(query, (novo_nome, nova_categoria_id, nova_descricao, novo_valor, gasto_id))

#atualizar usuario
def editar_usuario(usuario_id, novo_nome, novo_email, nova_senha=None):
    with con:
        cur = con.cursor()
        if nova_senha:
            senha_cripto = hash_senha(nova_senha)
            query = "UPDATE Usuario SET nome = ?, email = ?, senha = ? WHERE ID = ?"
            cur.execute(query, (novo_nome, novo_email, senha_cripto, usuario_id))
        else:
            query = "UPDATE Usuario SET nome = ?, email = ? WHERE ID = ?"
            cur.execute(query, (novo_nome, novo_email, usuario_id))

#Filtros--------------------------------------------------------------------------------------------------------------------

# Gastos por categoria
def filtrar_gastos_por_categoria(categoria_id):
    with con:
        cur = con.cursor()
        query = ("SELECT nome, descricao, valor, subtraido_em FROM Gastos WHERE categoria_id = ?")
        cur.execute(query, (categoria_id,))
        return cur.fetchall()

# Gastos por data
def filtrar_gastos_por_periodo(data_inicio, data_fim):
    with con:
        cur = con.cursor()
        query = ("SELECT nome, descricao, valor, subtraido_em FROM Gastos WHERE subtraido_em BETWEEN ? AND ?")
        cur.execute(query, (data_inicio, data_fim))
        return cur.fetchall()
    
# Total de gastos por categoria
def total_gastos_por_categoria():
    with con:
        cur = con.cursor()
        query = ("SELECT Categoria.nome, SUM(Gastos.valor) as total FROM Gastos JOIN Categoria ON Gastos.categoria_id = Categoria.ID GROUP BY Categoria.nome ")
        cur.execute(query)
        return cur.fetchall()
    
#Saldo entre duas datas
def saldo_por_periodo(data_inicio, data_fim):
    with con:
        cur = con.cursor()
        cur.execute("SELECT SUM(valor) FROM Receita WHERE adicionado_em BETWEEN ? AND ?", (data_inicio, data_fim))
        total_receita = cur.fetchone()[0] or 0

        cur.execute("SELECT SUM(valor) FROM Gastos WHERE subtraido_em BETWEEN ? AND ?", (data_inicio, data_fim))
        total_gastos = cur.fetchone()[0] or 0

        return { "receita": total_receita, "gastos": total_gastos,"saldo": total_receita - total_gastos}

# Ver saldo atual
def saldo_atual():
    hoje = datetime.now().strftime("%Y-%m-%d")
    return saldo_por_periodo("2000-01-01", hoje)

#USUARIO----------------------------------------------------------------------------------
#Encriptar senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

#Criar usuario
def criar_usuario(nome, email, senha):
    senha_cripto = hash_senha(senha)
    try:
        with con:
            cur = con.cursor()
            query = ("INSERT INTO Usuario (nome, email, senha) VALUES (?, ?, ?)")
            cur.execute(query, (nome, email, senha_cripto))
            
    except lite.IntegrityError as e:
        print("Erro: Email já cadastrado.")

# login de usuario com senha
def verificar_login(email, senha):
    senha_cripto = hash_senha(senha)
    with con:
        cur = con.cursor()
        query = ("SELECT * FROM Usuario WHERE email = ? AND senha = ?")
        cur.execute(query, (email, senha_cripto))
        return cur.fetchone()  # retorna a tupla completa