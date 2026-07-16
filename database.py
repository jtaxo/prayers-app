import os
import sqlite3

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = "prayers.db"

def is_postgres():
    return DATABASE_URL is not None and DATABASE_URL.startswith("postgres")

def get_db_connection():
    if is_postgres():
        if psycopg2 is None:
            raise Exception("psycopg2-binary is not installed, but DATABASE_URL is set.")
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn

def execute_query(query, params=(), commit=False, fetchall=False):
    conn = get_db_connection()
    
    if is_postgres():
        # Replace SQLite specific syntax with Postgres syntax
        pg_query = query.replace('?', '%s')
        if "AUTOINCREMENT" in pg_query:
            pg_query = pg_query.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
            
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(pg_query, params)
    else:
        cursor = conn.cursor()
        cursor.execute(query, params)

    result = None
    if fetchall:
        result = cursor.fetchall()
        
    if commit:
        conn.commit()
        
    cursor.close()
    conn.close()
    return result

def init_db():
    query = '''
        CREATE TABLE IF NOT EXISTS prayers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telemovel TEXT,
            assunto TEXT NOT NULL,
            data_submissao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''
    execute_query(query, commit=True)
    
    # Simple migration: check if telemovel column exists
    if is_postgres():
        check_query = "SELECT column_name FROM information_schema.columns WHERE table_name='prayers'"
        columns_rows = execute_query(check_query, fetchall=True)
        columns = [row[0] for row in columns_rows]
    else:
        conn = get_db_connection()
        cursor = conn.execute('PRAGMA table_info(prayers)')
        columns = [column[1] for column in cursor.fetchall()]
        conn.close()
        
    if 'telemovel' not in columns:
        execute_query('ALTER TABLE prayers ADD COLUMN telemovel TEXT', commit=True)

def add_prayer(nome, telemovel, assunto):
    execute_query('INSERT INTO prayers (nome, telemovel, assunto) VALUES (?, ?, ?)', (nome, telemovel, assunto), commit=True)

def get_all_prayers():
    return execute_query('SELECT * FROM prayers ORDER BY data_submissao DESC', fetchall=True)

def delete_prayer(prayer_id):
    execute_query('DELETE FROM prayers WHERE id = ?', (prayer_id,), commit=True)
