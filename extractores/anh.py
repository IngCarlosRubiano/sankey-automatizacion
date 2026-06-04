import pandas as pd
import requests
from datetime import datetime
from extractores.base import ExtractorBase

class ExtractorANH(ExtractorBase):
    """Extractor para estadísticas de producción de hidrocarburos de la ANH."""
    
    def __init__(self):
        super().__init__(
            nombre="ANH Producción Hidrocarburos",
            url="https://www.anh.gov.co/estadisticas-del-sector",
            tipo="excel",
            reglas={
                "col_origen": "Tipo_Hidrocarburo",
                "col_destino": "Uso",
                "col_valor": "Produccion",
                "factor_conversion": 1.0,
                "nombre_fuente": "ANH"
            }
        )
    
    def extraer(self) -> pd.DataFrame:
        """
        Extrae datos de producción de petróleo y gas desde la ANH.
        Por ahora devuelve un DataFrame vacío hasta que tengamos la URL exacta del Excel.
        """
        try:
            # Intentar descargar Excel de estadísticas (la URL exacta puede variar)
            url_excel = "https://www.anh.gov.co/.../estadisticas_produccion.xlsx"
            response = requests.get(url_excel)
            if response.status_code == 200:
                df = pd.read_excel(response.content)
                df_out = pd.DataFrame()
                df_out['origen'] = 'Producción Nacional'
                df_out['destino'] = df[self.reglas['col_destino']]
                df_out['valor'] = df[self.reglas['col_valor']] * self.reglas['factor_conversion']
                df_out['periodo'] = datetime.now().strftime('%Y')
                df_out['fuente'] = self.reglas['nombre_fuente']
                return df_out[['origen', 'destino', 'valor', 'periodo', 'fuente']]
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error al extraer de ANH: {e}")
            return pd.DataFrame()