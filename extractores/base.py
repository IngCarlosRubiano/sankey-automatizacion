from abc import ABC, abstractmethod
import pandas as pd

class ExtractorBase(ABC):
    """Clase base abstracta para todos los extractores."""
    
    def __init__(self, nombre, url, tipo, reglas=None):
        self.nombre = nombre
        self.url = url
        self.tipo = tipo
        self.reglas = reglas or {}
    
    @abstractmethod
    def extraer(self) -> pd.DataFrame:
        """
        Extrae los datos desde la fuente y devuelve un DataFrame
        con columnas: origen, destino, valor, periodo, fuente.
        """
        pass