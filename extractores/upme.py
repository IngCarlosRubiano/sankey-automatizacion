import pandas as pd
import requests
from datetime import datetime
from extractores.base import ExtractorBase

class ExtractorUPME(ExtractorBase):
    """Extractor para el Balance Energético Colombiano (BECO) de la UPME."""
    
    def __init__(self):
        super().__init__(
            nombre="UPME BECO",
            url="https://www1.upme.gov.co/DemandayEficiencia/Documents/BECO/BECO_2024.xlsx",
            tipo="excel",
            reglas={
                "hoja": "Flujos",
                "col_origen": "Origen",
                "col_destino": "Destino",
                "col_valor": "Valor_TJ",
                "factor_conversion": 1.0,
                "nombre_fuente": "UPME"
            }
        )
    
    def extraer(self) -> pd.DataFrame:
        """
        Descarga el archivo Excel del BECO y extrae los flujos energéticos.
        """
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                # Leer el Excel desde la respuesta HTTP
                df = pd.read_excel(response.content, sheet_name=self.reglas['hoja'])
                
                df_out = pd.DataFrame()
                df_out['origen'] = df[self.reglas['col_origen']]
                df_out['destino'] = df[self.reglas['col_destino']]
                df_out['valor'] = df[self.reglas['col_valor']] * self.reglas['factor_conversion']
                
                # Extraer año del nombre del archivo o usar año actual
                df_out['periodo'] = '2024'  # Ajustar según el archivo
                df_out['fuente'] = self.reglas['nombre_fuente']
                return df_out[['origen', 'destino', 'valor', 'periodo', 'fuente']]
            else:
                print(f"Error al descargar BECO: status {response.status_code}")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error al extraer de UPME: {e}")
            return pd.DataFrame()