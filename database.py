import sqlite3
from dieta import Alimento, Usuario

DB_NAME = 'dieta_database.db'

def conectar():
    """Conecta ao banco de dados SQLite e retorna a conexão e o cursor."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def criar_tabelas():
    """Cria as tabelas do banco de dados se elas não existirem."""
    conn = conectar()
    cursor = conn.cursor()

    # tabela de alimentos

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            calorias REAL NOT NULL,
            proteinas REAL NOT NULL,
            carboidratos REAL NOT NULL,
            gordura REAL NOT NULL
        )
    ''')

    # tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            genero TEXT NOT NULL,
            idade INTEGER NOT NULL,
            peso REAL NOT NULL,
            altura REAL NOT NULL,
            objetivo TEXT
        )
    ''')


    conn.commit()
    conn.close()

def salvar_alimento(alimento: Alimento):
    """Salva um objeto Alimento no banco de dados."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO alimentos (nome, calorias, proteinas, carboidratos, gordura)
        VALUES (?, ?, ?, ?, ?)
    ''', (alimento.nome, alimento.calorias_por_100g, alimento.proteinas, alimento.carboidratos, alimento.gordura))

    conn.commit()
    conn.close()

def carregar_todos_alimentos() -> list[Alimento]:
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT nome, calorias, proteinas, carboidratos, gordura FROM alimentos')
    
    lista_de_alimentos = []
    for row in cursor.fetchall():
        nome, calorias, proteinas, carboidratos, gordura = row
        alimento_obj = Alimento(nome, calorias, proteinas, carboidratos, gordura)
        lista_de_alimentos.append(alimento_obj)
    
    conn.close()
    return lista_de_alimentos

def salvar_usuario(usuario: Usuario):
    """Salva um objeto Usuario no banco de dados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, genero, idade, peso, altura, objetivo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (usuario.nome, usuario.genero, usuario.idade, usuario.peso, usuario.altura, usuario.objetivo))
    conn.commit()
    conn.close()

def carregar_todos_usuarios() -> list[Usuario]:
    """Carrega todos os usuários do banco de dados e retorna uma lista de objetos Usuario."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome, genero, idade, peso, altura, objetivo FROM usuarios')
    
    lista_de_usuarios = []
    for row in cursor.fetchall():
        nome, genero, idade, peso, altura, objetivo = row
        usuario_obj = Usuario(nome, genero, idade, peso, altura, objetivo)
        lista_de_usuarios.append(usuario_obj)
        
    conn.close()
    return lista_de_usuarios