import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db
import pandas as pd

def test_crear_bd_insertar_consultar():
    """Prueba la creación de la BD, inserción y consulta de flujos."""
    db.crear_bd()
    
    # Limpiar datos de pruebas anteriores para evitar acumulación
    conn = db.get_connection()
    conn.execute("DELETE FROM flujos")
    conn.commit()
    conn.close()
    
    # Insertar datos de prueba
    df_test = pd.DataFrame({
        'origen': ['Solar', 'Eólica'],
        'destino': ['Electricidad', 'Electricidad'],
        'valor': [100.0, 50.0],
        'periodo': ['2024', '2024'],
        'fuente': ['XM', 'XM']
    })
    insertados = db.insertar_flujos(df_test)
    assert insertados == 2
    
    # Consultar por periodo
    df = db.obtener_flujos(periodo='2024')
    assert len(df) == 2
    
    # Consultar periodos disponibles
    periodos = db.obtener_periodos()
    assert '2024' in periodos