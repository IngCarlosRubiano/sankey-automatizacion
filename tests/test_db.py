import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db
import pandas as pd
import json

def limpiar_tablas():
    """Limpia todas las tablas para empezar pruebas desde cero."""
    conn = db.get_connection()
    conn.execute("DELETE FROM flujos")
    conn.execute("DELETE FROM fuentes")
    conn.commit()
    conn.close()

def test_crear_bd():
    """Prueba que la BD se cree sin errores."""
    db.crear_bd()
    # Si no lanza excepción, la prueba pasa

def test_insertar_flujos():
    """Prueba la inserción de flujos."""
    limpiar_tablas()
    df_test = pd.DataFrame({
        'origen': ['Solar', 'Eólica'],
        'destino': ['Electricidad', 'Electricidad'],
        'valor': [100.0, 50.0],
        'periodo': ['2024', '2024'],
        'fuente': ['XM', 'XM']
    })
    insertados = db.insertar_flujos(df_test)
    assert insertados == 2

def test_insertar_dataframe_vacio():
    """Prueba que insertar un DataFrame vacío devuelva 0."""
    limpiar_tablas()
    df_vacio = pd.DataFrame()
    insertados = db.insertar_flujos(df_vacio)
    assert insertados == 0

def test_obtener_flujos_sin_filtros():
    """Prueba obtener flujos sin filtros."""
    limpiar_tablas()
    df_test = pd.DataFrame({
        'origen': ['Hidroeléctrica'],
        'destino': ['Electricidad'],
        'valor': [703800],
        'periodo': ['2024'],
        'fuente': ['XM']
    })
    db.insertar_flujos(df_test)
    df = db.obtener_flujos()
    assert len(df) >= 1

def test_obtener_flujos_por_periodo():
    """Prueba filtrar flujos por período."""
    limpiar_tablas()
    df_test = pd.DataFrame({
        'origen': ['Solar', 'Eólica', 'Térmica'],
        'destino': ['Electricidad', 'Electricidad', 'Electricidad'],
        'valor': [100, 50, 200],
        'periodo': ['2024', '2024', '2023'],
        'fuente': ['XM', 'XM', 'XM']
    })
    db.insertar_flujos(df_test)
    df_2024 = db.obtener_flujos(periodo='2024')
    assert len(df_2024) == 2

def test_obtener_flujos_por_fuente():
    """Prueba filtrar flujos por fuente."""
    limpiar_tablas()
    df_test = pd.DataFrame({
        'origen': ['Solar', 'Gas natural'],
        'destino': ['Electricidad', 'Industria'],
        'valor': [100, 200],
        'periodo': ['2024', '2024'],
        'fuente': ['XM', 'UPME']
    })
    db.insertar_flujos(df_test)
    df_xm = db.obtener_flujos(fuentes=['XM'])
    assert len(df_xm) == 1
    assert df_xm.iloc[0]['fuente'] == 'XM'

def test_obtener_periodos():
    """Prueba que se devuelvan los períodos ordenados."""
    limpiar_tablas()
    df_test = pd.DataFrame({
        'origen': ['A', 'B', 'C'],
        'destino': ['D', 'E', 'F'],
        'valor': [1, 2, 3],
        'periodo': ['2023', '2024', '2025'],
        'fuente': ['XM', 'XM', 'XM']
    })
    db.insertar_flujos(df_test)
    periodos = db.obtener_periodos()
    assert periodos == ['2025', '2024', '2023']

def test_agregar_fuente():
    """Prueba agregar una fuente a la BD."""
    limpiar_tablas()
    reglas = json.dumps({"col_origen": "Tecnologia", "col_destino": "Destino", "col_valor": "Generacion_GWh"})
    db.agregar_fuente("XM Test", "https://xm.com/test.csv", "csv", reglas, activo=1)
    fuentes = db.obtener_fuentes_activas()
    assert len(fuentes) == 1
    assert fuentes[0]['nombre'] == "XM Test"
    assert fuentes[0]['tipo'] == "csv"

def test_editar_fuente():
    """Prueba editar una fuente existente."""
    limpiar_tablas()
    reglas = json.dumps({"test": True})
    db.agregar_fuente("Fuente Original", "https://test.com", "csv", reglas, activo=1)
    fuentes = db.obtener_fuentes_activas()
    id_fuente = fuentes[0]['id']
    
    db.editar_fuente(id_fuente, nombre="Fuente Editada")
    fuentes = db.obtener_fuentes_activas()
    assert fuentes[0]['nombre'] == "Fuente Editada"

def test_eliminar_fuente():
    """Prueba eliminar una fuente."""
    limpiar_tablas()
    reglas = json.dumps({"test": True})
    db.agregar_fuente("Fuente a Eliminar", "https://test.com", "csv", reglas, activo=1)
    fuentes = db.obtener_fuentes_activas()
    id_fuente = fuentes[0]['id']
    
    db.eliminar_fuente(id_fuente)
    fuentes = db.obtener_fuentes_activas()
    assert len(fuentes) == 0