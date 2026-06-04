import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extractores.generico import extraer_fuente

def test_extraer_csv_local(tmp_path):
    """Prueba la extracción desde un CSV local simulado."""
    # Crear un CSV temporal
    csv_content = "tecnologia,combustible,generacion_gwh\nHidroeléctrica,Electricidad,195500\nSolar,Electricidad,11890"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content, encoding='utf-8')
    
    reglas = {
        "col_origen": "tecnologia",
        "col_destino": "combustible",
        "col_valor": "generacion_gwh",
        "factor_conversion": 3.6,
        "periodo": "2025-07",
        "nombre_fuente": "XM"
    }
    
    df = extraer_fuente(str(csv_file), 'csv', reglas)
    
    assert len(df) == 2
    assert df.iloc[0]['origen'] == 'Hidroeléctrica'
    assert df.iloc[0]['valor'] == 195500 * 3.6
    assert df.iloc[0]['periodo'] == '2025-07'
    assert df.iloc[0]['fuente'] == 'XM'

def test_extraer_xm_con_datos_locales(tmp_path):
    """Simula la extracción de XM con un CSV local de ejemplo."""
    from extractores.generico import extraer_fuente
    
    csv_content = "Tecnologia,Destino,Generacion_GWh\nHidroeléctrica,Electricidad SIN,195500\nSolar FV,Electricidad SIN,11890\nEólica,Electricidad SIN,560"
    csv_file = tmp_path / "xm_test.csv"
    csv_file.write_text(csv_content, encoding='utf-8')
    
    reglas = {
        "col_origen": "Tecnologia",
        "col_destino": "Destino",
        "col_valor": "Generacion_GWh",
        "factor_conversion": 3.6,
        "periodo": "2024",
        "nombre_fuente": "XM"
    }
    
    df = extraer_fuente(str(csv_file), 'csv', reglas)
    assert len(df) == 3
    assert df.iloc[0]['origen'] == 'Hidroeléctrica'
    assert df.iloc[0]['valor'] == 195500 * 3.6

def test_extraer_upme_con_datos_locales(tmp_path):
    """Simula la extracción de UPME con un Excel local de ejemplo."""
    from extractores.generico import extraer_fuente
    
    # Crear un Excel de prueba con pandas
    df_test = pd.DataFrame({
        'Origen': ['Hidroeléctrica', 'Gas Natural'],
        'Destino': ['Electricidad', 'Industria'],
        'Valor_TJ': [703800, 290000]
    })
    excel_file = tmp_path / "beco_test.xlsx"
    df_test.to_excel(excel_file, index=False)
    
    reglas = {
        "hoja": "Sheet1",
        "col_origen": "Origen",
        "col_destino": "Destino",
        "col_valor": "Valor_TJ",
        "factor_conversion": 1.0,
        "periodo": "2024",
        "nombre_fuente": "UPME"
    }
    
    df = extraer_fuente(str(excel_file), 'excel', reglas)
    assert len(df) == 2
    assert df.iloc[0]['origen'] == 'Hidroeléctrica'
    assert df.iloc[0]['valor'] == 703800