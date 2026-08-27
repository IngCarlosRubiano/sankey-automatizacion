# ⚡ Sankey - Sistema Energético Colombiano

Automatización de diagramas Sankey del sistema energético colombiano con fuentes oficiales verificables (UPME, XM, ANH).

## 📖 Descripción

Esta aplicación permite extraer, almacenar y visualizar los flujos energéticos de Colombia mediante diagramas Sankey interactivos. Está diseñada para ser actualizable periódicamente, trazable a fuentes oficiales y configurable por el usuario sin necesidad de programar.

### Características principales

- **Extracción automática** desde fuentes oficiales (UPME, XM, ANH) o desde cualquier CSV/Excel configurable.
- **Almacenamiento histórico** en base de datos SQLite, que permite consultar cualquier período.
- **Diagrama Sankey interactivo** generado con Plotly, con filtros visuales (excluir exportaciones, pérdidas, fuentes específicas).
- **Interfaz web amigable** construida con Streamlit.
- **Administración de fuentes** desde la misma interfaz (agregar, editar, eliminar URLs).
- **100% código abierto** (MIT License).

## 🚀 Instalación rápida

### Requisitos

- Python 3.10 o superior
- Git (opcional, para clonar)

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/IngCarlosRubiano/sankey-automatizacion.git
cd sankey-automatizacion

# Crear y activar entorno virtual (Windows)
python -m venv venv
venv\Scripts\activate

# Git Bash
source venv/Scripts/activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar la base de datos con fuentes predefinidas
python inicializar_fuentes.py

# (Opcional) Cargar datos de prueba para ver el gráfico
python cargar_datos_prueba.py

# Ejecutar la aplicación
streamlit run app.py