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
            telemovel TEXT,
            assunto TEXT NOT NULL,
            data_submissao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Simple migration: check if telemovel column exists
    cursor = conn.execute('PRAGMA table_info(prayers)')
    columns = [column[1] for column in cursor.fetchall()]
    if 'telemovel' not in columns:
        conn.execute('ALTER TABLE prayers ADD COLUMN telemovel TEXT')
        
    conn.commit()
    conn.close()

def add_prayer(nome, telemovel, assunto):
    conn = get_db_connection()
    conn.execute('INSERT INTO prayers (nome, telemovel, assunto) VALUES (?, ?, ?)', (nome, telemovel, assunto))
    conn.commit()
    conn.close()

def get_all_prayers():
    conn = get_db_connection()
    prayers = conn.execute('SELECT * FROM prayers ORDER BY data_submissao DESC').fetchall()
    conn.close()
    return prayers
