"""Script para inicializar la BD con fuentes y datos por defecto."""
import json
from db import crear_bd, agregar_fuente, obtener_fuentes_activas, ejecutar_extraccion_completa, obtener_periodos

crear_bd()

# Cargar fuentes desde JSON
with open('fuentes.json', 'r', encoding='utf-8') as f:
    fuentes = json.load(f)

for fuente in fuentes:
    reglas_str = json.dumps(fuente['reglas_extraccion'])
    agregar_fuente(
        nombre=fuente['nombre'],
        url=fuente['url'],
        tipo=fuente['tipo'],
        reglas_extraccion=reglas_str,
        activo=fuente['activo']
    )

# Si no hay datos, ejecutar extracción inicial
periodos = obtener_periodos()
if not periodos:
    print("No hay datos. Ejecutando extracción inicial...")
    ejecutar_extraccion_completa()
    # Si sigue sin datos (por URLs no accesibles), cargar datos de respaldo
    periodos = obtener_periodos()
    if not periodos:
        print("Cargando datos de respaldo...")
        import pandas as pd
        from db import insertar_flujos
        df = pd.read_csv('datos/flujos_respaldo.csv')
        insertar_flujos(df)
        print("Datos de respaldo cargados.")