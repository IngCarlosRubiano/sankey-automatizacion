import pandas as pd
import requests
from io import StringIO
from datetime import datetime
from extractores.base import ExtractorBase

class ExtractorXM(ExtractorBase):
    """Extractor para datos de generación eléctrica de XM."""
    
    def __init__(self):
        super().__init__(
            nombre="XM Generación Mensual",
            url="https://www.xm.com.co/consumo/datos-abiertos",
            tipo="csv",
            reglas={
                "col_origen": "Tecnologia",
                "col_destino": "Destino",
                "col_valor": "Generacion_GWh",
                "factor_conversion": 3.6,
                "nombre_fuente": "XM"
            }
        )
    
    def extraer(self) -> pd.DataFrame:
        """
        Extrae los datos de generación eléctrica desde XM.
        Nota: la URL exacta del CSV puede cambiar. 
        Por ahora usamos una función que intenta obtener el CSV más reciente.
        """
        try:
            # Intentar URL directa del CSV (ajustar según el portal real)
            url_csv = "https://www.xm.com.co/.../generacion_mensual.csv"
            response = requests.get(url_csv)
            if response.status_code == 200:
                df = pd.read_csv(StringIO(response.text))
                df_out = pd.DataFrame()
                df_out['origen'] = df[self.reglas['col_origen']]
                df_out['destino'] = 'Electricidad SIN'
                df_out['valor'] = df[self.reglas['col_valor']] * self.reglas['factor_conversion']
                df_out['periodo'] = datetime.now().strftime('%Y-%m')
                df_out['fuente'] = self.reglas['nombre_fuente']
                return df_out[['origen', 'destino', 'valor', 'periodo', 'fuente']]
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error al extraer de XM: {e}")
            return pd.DataFrame()