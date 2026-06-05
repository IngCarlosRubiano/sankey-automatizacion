"""Carga datos de respaldo en la BD."""
import pandas as pd
from db import crear_bd, insertar_flujos

crear_bd()
df = pd.read_csv('datos/flujos_respaldo.csv')
insertados = insertar_flujos(df)
print(f"{insertados} registros de respaldo cargados.")