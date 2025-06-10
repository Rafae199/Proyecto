import sqlite3
from sqlite3 import Row
import os

def get_db():
    """Conexión a la base de datos SQLite"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'DB_PPAL.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = Row  # Resultados como diccionarios
    conn.execute("PRAGMA foreign_keys = ON")  # Habilita claves foráneas
    return conn