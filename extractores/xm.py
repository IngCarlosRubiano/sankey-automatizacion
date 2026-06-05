import pandas as pd
import requests
from io import StringIO
from datetime import datetime

def extraer_xm():
    """
    Extrae generación eléctrica por tecnología desde la API de datos abiertos de XM.
    URL: https://www.xm.com.co/consumo/datos-abiertos
    """
    try:
        # URL del CSV de generación mensual (ajustar según el portal)
        url = "https://www.xm.com.co/consumo/sites/default/files/datos-abiertos/generacion_mensual.csv"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text), encoding='latin1')
            # Filtrar solo Colombia si existe columna de país
            if 'CodigoPais' in df.columns:
                df = df[df['CodigoPais'] == 'COL']
            
            df_out = pd.DataFrame()
            df_out['origen'] = df['Tecnologia']
            df_out['destino'] = 'Electricidad SIN'
            # Convertir GWh a TJ (1 GWh = 3.6 TJ)
            df_out['valor'] = pd.to_numeric(df['Generacion_GWh'], errors='coerce') * 3.6
            df_out['periodo'] = datetime.now().strftime('%Y-%m')
            df_out['fuente'] = 'XM'
            return df_out.dropna()
        else:
            print(f"Error XM: status {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error extrayendo XM: {e}")
        return pd.DataFrame()