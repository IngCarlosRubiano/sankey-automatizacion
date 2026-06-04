"""Script temporal para cargar datos de prueba en la BD."""
import pandas as pd
from db import crear_bd, insertar_flujos

crear_bd()

# Datos de prueba basados en el CSV que ya tenías
datos = [
    {'origen': 'Hidroeléctrica', 'destino': 'Electricidad SIN', 'valor': 703800, 'periodo': '2024', 'fuente': 'XM'},
    {'origen': 'Solar FV', 'destino': 'Electricidad SIN', 'valor': 42804, 'periodo': '2024', 'fuente': 'XM'},
    {'origen': 'Eólica', 'destino': 'Electricidad SIN', 'valor': 2016, 'periodo': '2024', 'fuente': 'XM'},
    {'origen': 'Térmica (gas)', 'destino': 'Electricidad SIN', 'valor': 236952, 'periodo': '2024', 'fuente': 'XM'},
    {'origen': 'Gas natural', 'destino': 'Consumo industrial', 'valor': 290000, 'periodo': '2024', 'fuente': 'UPME'},
    {'origen': 'Gas natural', 'destino': 'Consumo residencial', 'valor': 70000, 'periodo': '2024', 'fuente': 'UPME'},
    {'origen': 'Electricidad SIN', 'destino': 'Consumo residencial', 'valor': 90000, 'periodo': '2024', 'fuente': 'XM'},
    {'origen': 'Electricidad SIN', 'destino': 'Consumo industrial', 'valor': 72000, 'periodo': '2024', 'fuente': 'XM'},
    {'origen': 'Electricidad SIN', 'destino': 'Pérdidas', 'valor': 32400, 'periodo': '2024', 'fuente': 'XM'},
]

df = pd.DataFrame(datos)
insertados = insertar_flujos(df)
print(f"{insertados} registros de prueba insertados.")