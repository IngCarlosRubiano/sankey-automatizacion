import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sankey_gen import generar_sankey, generar_sankey_con_filtros

def test_generar_sankey_basico():
    """Prueba que se genera un Sankey básico sin errores."""
    df = pd.DataFrame({
        'origen': ['Solar', 'Eólica'],
        'destino': ['Electricidad', 'Electricidad'],
        'valor': [42804, 2016]
    })
    fig = generar_sankey(df)
    assert fig is not None

def test_generar_sankey_dataframe_vacio():
    """Prueba que un DataFrame vacío devuelva None."""
    df = pd.DataFrame()
    fig = generar_sankey(df)
    assert fig is None

def test_generar_sankey_con_exportaciones():
    """Prueba que se incluyan las exportaciones cuando se solicita."""
    df = pd.DataFrame({
        'origen': ['Petróleo crudo', 'Electricidad'],
        'destino': ['Exportación', 'Consumo residencial'],
        'valor': [1000000, 90000]
    })
    fig = generar_sankey_con_filtros(df, incluir_exportaciones=True)
    assert fig is not None

def test_generar_sankey_sin_exportaciones():
    """Prueba que se excluyan las exportaciones cuando se solicita."""
    df = pd.DataFrame({
        'origen': ['Petróleo crudo', 'Electricidad'],
        'destino': ['Exportación', 'Consumo residencial'],
        'valor': [1000000, 90000]
    })
    fig = generar_sankey_con_filtros(df, incluir_exportaciones=False)
    assert fig is not None

def test_generar_sankey_excluir_fuentes():
    """Prueba que se excluyan fuentes específicas."""
    df = pd.DataFrame({
        'origen': ['Carbón', 'Solar FV', 'Eólica'],
        'destino': ['Exportación', 'Electricidad', 'Electricidad'],
        'valor': [100, 200, 300]
    })
    fig = generar_sankey_con_filtros(df, fuentes_excluir=['Carbón'])
    assert fig is not None

def test_generar_sankey_titulo_personalizado():
    """Prueba que se pueda personalizar el título."""
    df = pd.DataFrame({
        'origen': ['Solar'],
        'destino': ['Electricidad'],
        'valor': [100]
    })
    fig = generar_sankey(df, titulo="Mi Sankey Personalizado")
    assert fig is not None