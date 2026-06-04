import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "sankey.db"

def get_connection():
    """Devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_bd():
    """Crea las tablas necesarias si no existen."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flujos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origen TEXT NOT NULL,
        destino TEXT NOT NULL,
        valor REAL NOT NULL,
        periodo TEXT NOT NULL,
        fuente TEXT NOT NULL,
        fecha_extraccion TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fuentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        url TEXT NOT NULL,
        tipo TEXT NOT NULL,
        activo INTEGER DEFAULT 1,
        reglas_extraccion TEXT DEFAULT '{}'
    )
    """)
    
    conn.commit()
    conn.close()
    print("Base de datos creada correctamente.")

def insertar_flujos(df):
    """
    Inserta un DataFrame con columnas [origen, destino, valor, periodo, fuente]
    en la tabla de flujos. Agrega la fecha de extracción automáticamente.
    """
    if df.empty:
        return 0
    
    df = df.copy()
    df['fecha_extraccion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_connection()
    df.to_sql('flujos', conn, if_exists='append', index=False)
    conn.close()
    return len(df)

def obtener_flujos(periodo=None, fuentes=None):
    """
    Devuelve un DataFrame con los flujos filtrados por período y/o fuentes.
    Si periodo es None, devuelve todos los períodos.
    Si fuentes es None, devuelve todas las fuentes.
    """
    conn = get_connection()
    query = "SELECT origen, destino, valor, periodo, fuente FROM flujos WHERE 1=1"
    params = []
    
    if periodo:
        query += " AND periodo = ?"
        params.append(periodo)
    
    if fuentes:
        placeholders = ','.join('?' * len(fuentes))
        query += f" AND fuente IN ({placeholders})"
        params.extend(fuentes)
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def obtener_periodos():
    """Devuelve una lista de períodos únicos ordenados descendentemente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT periodo FROM flujos ORDER BY periodo DESC")
    periodos = [row['periodo'] for row in cursor.fetchall()]
    conn.close()
    return periodos

def obtener_fuentes_activas():
    """Devuelve una lista de diccionarios con las fuentes activas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fuentes WHERE activo = 1")
    fuentes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return fuentes

def agregar_fuente(nombre, url, tipo, reglas_extraccion="{}", activo=1):
    """Agrega una nueva fuente a la tabla de fuentes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO fuentes (nombre, url, tipo, activo, reglas_extraccion)
    VALUES (?, ?, ?, ?, ?)
    """, (nombre, url, tipo, activo, reglas_extraccion))
    conn.commit()
    conn.close()

def editar_fuente(id_fuente, **kwargs):
    """Actualiza los campos de una fuente. kwargs puede incluir nombre, url, tipo, activo, reglas_extraccion."""
    conn = get_connection()
    cursor = conn.cursor()
    for campo, valor in kwargs.items():
        cursor.execute(f"UPDATE fuentes SET {campo} = ? WHERE id = ?", (valor, id_fuente))
    conn.commit()
    conn.close()

def eliminar_fuente(id_fuente):
    """Elimina una fuente por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fuentes WHERE id = ?", (id_fuente,))
    conn.commit()
    conn.close()