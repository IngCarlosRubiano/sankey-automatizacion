import pandas as pd
import requests
from io import StringIO
from datetime import datetime

def extraer_fuente(url, tipo, reglas_json):
    """
    Extrae datos de una fuente genérica según su tipo y reglas.
    
    Args:
        url: str, URL o ruta del archivo.
        tipo: str, 'csv' o 'excel'.
        reglas_json: str o dict, reglas de extracción en formato JSON con:
            - col_origen: nombre de la columna de origen.
            - col_destino: nombre de la columna de destino.
            - col_valor: nombre de la columna de valor.
            - factor_conversion: float, factor para convertir a TJ.
            - filtro (opcional): dict con condiciones {columna: valor}.
            - periodo: str, período fijo (si no se obtiene de los datos).
    
    Returns:
        DataFrame con columnas [origen, destino, valor, periodo, fuente]
    """
    import json
    if isinstance(reglas_json, str):
        reglas = json.loads(reglas_json)
    else:
        reglas = reglas_json
    
    # Descargar o leer archivo
    if url.startswith('http'):
        response = requests.get(url)
        if tipo == 'csv':
            df = pd.read_csv(StringIO(response.text))
        elif tipo == 'excel':
            df = pd.read_excel(response.content)
        else:
            raise ValueError(f"Tipo no soportado: {tipo}")
    else:
        # Archivo local
        if tipo == 'csv':
            df = pd.read_csv(url, encoding='utf-8')
        elif tipo == 'excel':
            df = pd.read_excel(url)
    
    # Aplicar filtro si existe
    if 'filtro' in reglas:
        for col, val in reglas['filtro'].items():
            df = df[df[col] == val]
    
    # Seleccionar y renombrar columnas
    df_out = pd.DataFrame()
    df_out['origen'] = df[reglas['col_origen']]
    df_out['destino'] = df[reglas['col_destino']]
    df_out['valor'] = df[reglas['col_valor']] * reglas.get('factor_conversion', 1)
    
    # Periodo
    if 'periodo' in reglas:
        df_out['periodo'] = reglas['periodo']
    elif 'col_periodo' in reglas:
        df_out['periodo'] = df[reglas['col_periodo']]
    else:
        df_out['periodo'] = datetime.now().strftime('%Y')
    
    df_out['fuente'] = reglas.get('nombre_fuente', 'Desconocida')
    
    return df_out[['origen', 'destino', 'valor', 'periodo', 'fuente']]