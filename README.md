# ⚡ Sankey: Visualización & Automatización del Sistema Energético Colombiano

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
</p>

Aplicación web interactiva y pipeline de datos desarrollado en Python para extraer, almacenar, procesar y visualizar la matriz de flujo energético de Colombia mediante diagramas de Sankey trazables. 

El sistema está diseñado para la ingesta periódica de información desde fuentes oficiales verificables (UPME, XM, ANH), permitiendo consultar históricos y parametrizar los flujos sin necesidad de modificar el código fuente.

## 🚀 Propósito y Arquitectura

Este proyecto resuelve el reto de consolidar datos energéticos heterogéneos mediante un flujo automatizado de tres capas:

1. **ETL / Ingesta de Datos:** Extracción desde archivos estructurados (CSV/Excel) y URLs oficiales configurables.
2. **Persistencia & Almacenamiento:** Base de datos relacional SQLite para el control de versiones históricas y la trazabilidad de la información.
3. **Capa de Presentación:** Interfaz web ligera en Streamlit integrada con motores gráficos interactivos para análisis exploratorio.

## ✨ Características Principales

- **Ingesta configurable:** Ingesta automática desde fuentes gubernamentales (UPME, XM, ANH) o archivos locales parametrizables.
- **Históricos en SQLite:** Motor de almacenamiento ligero para persistir y consultar períodos energéticos específicos.
- **Visualización interactiva:** Generación de diagramas Sankey dinámicos mediante Plotly, con filtros avanzados (exclusión de pérdidas, exportaciones y nodos específicos).
- **Gestión de fuentes vía UI:** Panel de administración integrado para agregar, modificar o deshabilitar orígenes de datos en tiempo real.
- **Licencia abierta:** Proyecto bajo licencia MIT.

## ⚙️ Instalación y Configuración Local

### Requisitos Previos
- Python 3.10 o superior
- Git

### Pasos de Despliegue

1. Clona el repositorio:
   ```bash
   git clone https://github.com/IngCarlosRubiano/sankey-automatizacion.git
   cd sankey-automatizacion
Crea y activa el entorno virtual:

bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
Instala las dependencias del proyecto:

bash
pip install -r requirements.txt
Inicializa la base de datos e ingesta de datos iniciales:

bash
# Carga la estructura e inicializa las fuentes oficiales
python inicializar_fuentes.py

# (Opcional) Carga dataset de prueba para la vista previa inicial
python cargar_datos_prueba.py
Ejecuta la aplicación web:

bash
streamlit run app.py
## 👤 Autor
# Carlos Rubiano

<p>
<a href="https://github.com/IngCarlosRubiano/IngCarlosRubiano" target="_blank">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
</a>
<a href="https://www.linkedin.com/in/carlos-rubiano-engineer/" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>
</p>


⭐ Si este proyecto te fue útil, no olvides dejar una estrella.