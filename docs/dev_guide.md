# Guía de Desarrollo - Sankey Sistema Energético Colombiano

## Configuración del entorno

1. Clona el repositorio y crea un entorno virtual.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Instala las dependencias de desarrollo: `pip install pytest pytest-cov`

## Estructura del código

- **`db.py`**: todas las funciones de base de datos (SQLite).
- **`extractores/generico.py`**: extractor dinámico que interpreta reglas JSON para leer CSV/Excel.
- **`extractores/base.py`**: clase abstracta para crear nuevos extractores específicos.
- **`sankey_gen.py`**: generación del diagrama Sankey con Plotly.
- **`app.py`**: interfaz de usuario con Streamlit.

## Cómo agregar un nuevo extractor específico

1. Crea un archivo en `extractores/` (ej. `extractores/nueva_fuente.py`).
2. Hereda de `ExtractorBase` e implementa el método `extraer()`.
3. Registra la fuente en `inicializar_fuentes.py` o desde la interfaz web.

Ejemplo mínimo:

```python
from extractores.base import ExtractorBase
import pandas as pd

class ExtractorNuevaFuente(ExtractorBase):
    def __init__(self):
        super().__init__(
            nombre="Nueva Fuente",
            url="https://...",
            tipo="csv",
            reglas={...}
        )
    
    def extraer(self) -> pd.DataFrame:
        # Leer datos y devolver DataFrame con columnas:
        # origen, destino, valor, periodo, fuente
        ...

Ejecutar pruebas

pytest tests/ -v --cov=. --cov-report=term-missing