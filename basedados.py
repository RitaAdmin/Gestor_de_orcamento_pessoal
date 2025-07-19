#importar SQLITE
import sqlite3 as lite

#criar conexao com banco de dados
con=lite.connect('dados.gestao-financeira-pessoal')

#criar tabela da categoria
with con:
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Categoria (ID INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT NOT NULL, tipo TEXT CHECK (tipo IN ('receita', 'despesa'))NOT NULL)")


#criar tabela de receita
with con:
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Receita (ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, categoria_id INTEGER NOT NULL, descricao TEXT, adicionado_em DATE DEFAULT CURRENT_DATE, valor REAL NOT NULL, FOREIGN KEY (categoria_id) REFERENCES Categoria (ID))")


#criar tabelas dE Gastos
with con:
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Gastos(ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, categoria_id INTEGER NOT NULL, descricao TEXT, subtraido_em DATE DEFAULT CURRENT_DATE, valor REAL NOT NULL, FOREIGN KEY (categoria_id) REFERENCES Categoria(ID))")


#criar tabela USUARIO 
with con:
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Usuario (ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, email text UNIQUE NOT NULL)")

    
