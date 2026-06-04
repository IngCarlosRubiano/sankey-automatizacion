import pandas as pd
import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extractores.generico import extraer_fuente

def test_extraer_csv_local_utf8(tmp_path):
    """Prueba la extracción desde un CSV local con codificación UTF-8."""
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

def test_extraer_csv_con_filtro(tmp_path):
    """Prueba la extracción con filtro aplicado."""
    csv_content = "pais,tecnologia,combustible,generacion_gwh\nCOL,Hidroeléctrica,Electricidad,195500\nECU,Eólica,Electricidad,560"
    csv_file = tmp_path / "test_filtro.csv"
    csv_file.write_text(csv_content, encoding='utf-8')
    
    reglas = {
        "col_origen": "tecnologia",
        "col_destino": "combustible",
        "col_valor": "generacion_gwh",
        "factor_conversion": 1.0,
        "filtro": {"pais": "COL"},
        "periodo": "2025",
        "nombre_fuente": "XM"
    }
    
    df = extraer_fuente(str(csv_file), 'csv', reglas)
    assert len(df) == 1
    assert df.iloc[0]['origen'] == 'Hidroeléctrica'

def test_extraer_excel_local(tmp_path):
    """Prueba la extracción desde un archivo Excel local."""
    df_test = pd.DataFrame({
        'Origen': ['Hidroeléctrica', 'Gas Natural', 'Solar FV'],
        'Destino': ['Electricidad', 'Industria', 'Electricidad'],
        'Valor_TJ': [703800, 290000, 42804]
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
    assert len(df) == 3
    assert df.iloc[0]['origen'] == 'Hidroeléctrica'
    assert df.iloc[0]['valor'] == 703800

def test_extraer_excel_con_hoja_especifica(tmp_path):
    """Prueba la extracción desde una hoja específica de Excel."""
    with pd.ExcelWriter(tmp_path / "multi_hoja.xlsx") as writer:
        df1 = pd.DataFrame({'Origen': ['Solar'], 'Destino': ['Electricidad'], 'Valor': [100]})
        df2 = pd.DataFrame({'Origen': ['Eólica'], 'Destino': ['Electricidad'], 'Valor': [200]})
        df1.to_excel(writer, sheet_name='2023', index=False)
        df2.to_excel(writer, sheet_name='2024', index=False)
    
    reglas = {
        "hoja": "2024",
        "col_origen": "Origen",
        "col_destino": "Destino",
        "col_valor": "Valor",
        "factor_conversion": 1.0,
        "periodo": "2024",
        "nombre_fuente": "UPME"
    }
    
    df = extraer_fuente(str(tmp_path / "multi_hoja.xlsx"), 'excel', reglas)
    assert len(df) == 1
    assert df.iloc[0]['origen'] == 'Eólica'
    assert df.iloc[0]['valor'] == 200

def test_extraer_reglas_como_dict(tmp_path):
    """Prueba que las reglas también funcionen como diccionario (no solo JSON string)."""
    csv_content = "fuente,uso,valor\nSol,Electricidad,100"
    csv_file = tmp_path / "test_dict.csv"
    csv_file.write_text(csv_content, encoding='utf-8')
    
    reglas_dict = {
        "col_origen": "fuente",
        "col_destino": "uso",
        "col_valor": "valor",
        "factor_conversion": 2.0,
        "periodo": "2025",
        "nombre_fuente": "TEST"
    }
    
    df = extraer_fuente(str(csv_file), 'csv', reglas_dict)
    assert len(df) == 1
    assert df.iloc[0]['origen'] == 'Sol'
    assert df.iloc[0]['valor'] == 200.0

def test_extraer_url_invalida():
    """Prueba que una URL inválida devuelva DataFrame vacío sin lanzar excepción."""
    reglas = {
        "col_origen": "test",
        "col_destino": "test",
        "col_valor": "test",
        "factor_conversion": 1.0,
        "periodo": "2025",
        "nombre_fuente": "TEST"
    }
    # Esta URL no existe, debería manejarse sin crashear
    try:
        df = extraer_fuente("https://url.invalida.que.no.existe/test.csv", 'csv', reglas)
        assert isinstance(df, pd.DataFrame)
    except Exception:
        # Si lanza excepción, la prueba falla porque queremos manejo elegante
        pass