# Guía de Usuario - Sankey Sistema Energético Colombiano

## Inicio rápido

1. Ejecuta `streamlit run app.py` en la terminal.
2. Abre tu navegador en `http://localhost:8501`.
3. Usa el menú lateral para navegar entre las secciones.

## Secciones de la aplicación

### 📥 Extraer Datos

- **Extraer ahora**: descarga los datos desde las fuentes configuradas y los guarda en la base de datos.
- **Programador**: en esta versión, la extracción automática diaria está preconfigurada. Puedes iniciarla manualmente.

### 📊 Generar Gráfico

- Selecciona el **período** (año) que deseas visualizar.
- Usa los **checkboxes** para mostrar u ocultar exportaciones, importaciones y pérdidas.
- Puedes **excluir fuentes específicas** (hidroeléctrica, solar, etc.) para filtrar el gráfico.
- Haz clic en **"Generar Diagrama Sankey"** para visualizarlo.
- Puedes **descargar los datos** en formato CSV desde la misma sección.

### ⚙️ Administrar Fuentes

- **Ver fuentes**: lista las fuentes configuradas con su URL y estado.
- **Agregar fuente**: completa el formulario con el nombre, URL, tipo (CSV o Excel) y las reglas de extracción en formato JSON.
- **Eliminar fuente**: desde la vista de detalle de cada fuente.

### Formato de reglas de extracción (JSON)

Al agregar una nueva fuente, debes especificar cómo leer los datos. El JSON debe tener esta estructura:

```json
{
  "col_origen": "nombre_columna_origen",
  "col_destino": "nombre_columna_destino",
  "col_valor": "nombre_columna_valor",
  "factor_conversion": 1.0,
  "periodo": "2024",
  "nombre_fuente": "Nombre descriptivo",
  "filtro": { "pais": "COL" }   // opcional
}

Para archivos Excel, agrega "hoja": "Nombre de la hoja".

** Solución de problemas **
La aplicación no inicia
Asegúrate de haber instalado todas las dependencias con pip install -r requirements.txt y de tener el entorno virtual activado.

No se ven datos en el gráfico
Ve a "Extraer Datos" y haz clic en "Extraer ahora". Si las URLs de las fuentes no son accesibles, verás un mensaje de advertencia. Verifica las URLs en "Administrar Fuentes".

Error al cargar una fuente
Revisa que las reglas JSON sean válidas y que las columnas existan en el archivo fuente.

## Formato del archivo CSV para actualización de datos

El archivo CSV debe tener exactamente estas cinco columnas en el siguiente orden:

origen,destino,valor,periodo,fuente


| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| origen | Nodo de origen del flujo energético | Hidroeléctrica |
| destino | Nodo de destino del flujo energético | Electricidad SIN |
| valor | Magnitud del flujo en TJ (Terajulios) | 703800 |
| periodo | Año del dato (YYYY) | 2024 |
| fuente | Organismo que reporta el dato | XM |

Reglas:
1. El separador debe ser coma (,).
2. La codificación debe ser UTF-8.
3. No usar comillas en los nombres de nodos.
4. Mantener consistencia en los nombres de nodos (ej: siempre "Hidroeléctrica", no "Hidro" en otra fila).
5. Los valores numéricos sin separadores de miles ni símbolos.

Puedes descargar una plantilla de ejemplo desde la sección "Extraer Datos" de la aplicación.
