import sqlite3

DB_NAME = "prayers.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prayers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            assunto TEXT NOT NULL,
            data_submissao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_prayer(nome, assunto):
    conn = get_db_connection()
    conn.execute('INSERT INTO prayers (nome, assunto) VALUES (?, ?)', (nome, assunto))
    conn.commit()
    conn.close()

def get_all_prayers():
    conn = get_db_connection()
    prayers = conn.execute('SELECT * FROM prayers ORDER BY data_submissao DESC').fetchall()
    conn.close()
    return prayers
