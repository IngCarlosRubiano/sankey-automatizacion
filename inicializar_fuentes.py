"""Script para cargar las fuentes iniciales desde fuentes.json a la base de datos."""
import json
from db import crear_bd, agregar_fuente, obtener_fuentes_activas

# Crear BD si no existe
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
    print(f"Fuente agregada: {fuente['nombre']}")

# Verificar
activas = obtener_fuentes_activas()
print(f"\nFuentes activas en BD: {len(activas)}")
for f in activas:
    print(f"  - {f['nombre']} ({f['tipo']})")