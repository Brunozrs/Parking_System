import sqlite3

DB_PATH = "data.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn

def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT NOT NULL,
                phone_number TEXT,
                email        TEXT,
                document     TEXT,
                address      TEXT,
                type         TEXT NOT NULL  -- 'client' or 'worker'
            );

            CREATE TABLE IF NOT EXISTS workers (
                id     INTEGER PRIMARY KEY REFERENCES users(id),
                salary REAL NOT NULL,
                password TEXT NOT NULL,
                role     TEXT NOT NULL DEFAULT 'worker' 
            );

            CREATE TABLE IF NOT EXISTS clients (
                id        INTEGER PRIMARY KEY REFERENCES users(id),
                arrival   TIMESTAMP,
                departure TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS vehicles (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                plate     TEXT NOT NULL UNIQUE,
                color     TEXT,
                size      TEXT,
                client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
                image_b64 TEXT,
                space_id INTEGER REFERENCES parking_spaces(id)
            );

            CREATE TABLE IF NOT EXISTS parking_spaces (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                number    INTEGER NOT NULL UNIQUE,
                size      TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1
            );
        """)