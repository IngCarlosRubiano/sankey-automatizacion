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