import sqlite3

conn = sqlite3.connect("JunkyardFollowUP.db")
cursor = conn.cursor()

createTable = """CREATE TABLE IF NOT EXISTS clients(
    Cod_Cliente INTEGER PRIMARY KEY,
    Cod_Entrega INTEGER,
    Nome_Cliente TEXT,
    CPF INTEGER,
    Email TEXT,
    Logradouro TEXT,
    Contato TEXT,
    Data_Homol TEXT,
    Data_Atualiz TEXT,
    Status INTEGER,
    FOREIGN KEY(Cod_Entrega) REFERENCES Entrega_Roupa (Cod_Entrega))"""
cursor.execute(createTable)

createClient = """INSERT INTO clients VALUES(
    '248',
    '1224459',
    'Henrique R. M. Pincelli',
    '44062112841',
    'pincellihenrique9@gmail.com',
    'Avenida Parada Pinto, 2511 - 02611-003 - São Paulo, SP',
    '(11)94665-3230',
    '08/06/2023',
    '08/06/2023',
    1)"""
cursor.execute(createClient)

conn.commit()
conn.close()
