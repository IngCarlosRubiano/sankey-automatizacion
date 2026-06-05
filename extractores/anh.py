import pandas as pd
import requests
from datetime import datetime

def extraer_anh():
    """
    Extrae producción de hidrocarburos desde la ANH.
    URL: https://www.anh.gov.co/estadisticas-del-sector
    """
    try:
        # URL del Excel de producción (ajustar según portal)
        url = "https://www.anh.gov.co/estadisticas-del-sector/Produccion/Produccion_mensual.xlsx"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Guardar copia local
            with open('datos/produccion_anh.xlsx', 'wb') as f:
                f.write(response.content)
            
            df = pd.read_excel('datos/produccion_anh.xlsx', sheet_name='Produccion')
            
            df_out = pd.DataFrame()
            df_out['origen'] = 'Petróleo crudo'
            df_out['destino'] = 'Exportación / Refinación'
            # Valor en barriles, convertir a TJ aprox (1 barril ~ 6.12 GJ = 0.00612 TJ)
            df_out['valor'] = pd.to_numeric(df['Produccion_barriles'], errors='coerce') * 0.00612
            df_out['periodo'] = datetime.now().strftime('%Y')
            df_out['fuente'] = 'ANH'
            return df_out.dropna()
        else:
            print(f"Error ANH: status {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error extrayendo ANH: {e}")
        return pd.DataFrame()