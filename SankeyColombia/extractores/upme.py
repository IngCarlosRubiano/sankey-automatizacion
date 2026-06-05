import pandas as pd
import requests
from datetime import datetime

def extraer_upme():
    """
    Descarga el Balance Energético Colombiano (BECO) desde la UPME.
    URL base: https://www1.upme.gov.co/DemandayEficiencia
    """
    try:
        # URL del archivo Excel del BECO más reciente (ajustar año si es necesario)
        url = "https://www1.upme.gov.co/DemandayEficiencia/Documents/BECO/BECO_2024.xlsx"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Guardar copia local
            with open('datos/beco_2024.xlsx', 'wb') as f:
                f.write(response.content)
            
            # Leer hoja de flujos
            df = pd.read_excel('datos/beco_2024.xlsx', sheet_name='Flujos')
            
            df_out = pd.DataFrame()
            df_out['origen'] = df['Origen']
            df_out['destino'] = df['Destino']
            df_out['valor'] = pd.to_numeric(df['Valor_TJ'], errors='coerce')
            df_out['periodo'] = '2024'  # Ajustar según el archivo descargado
            df_out['fuente'] = 'UPME'
            return df_out.dropna()
        else:
            print(f"Error UPME: status {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error extrayendo UPME: {e}")
        return pd.DataFrame()