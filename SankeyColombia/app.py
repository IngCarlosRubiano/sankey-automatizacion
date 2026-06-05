import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Agregar el directorio actual al path para importaciones locales
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from db import (crear_bd, obtener_flujos, obtener_periodos, 
                obtener_fuentes_activas, ejecutar_extraccion_completa,
                agregar_fuente, editar_fuente, eliminar_fuente)
from sankey_gen import generar_sankey, generar_sankey_con_filtros

# ------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sankey - Sistema Energético Colombiano",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Automatización de Diagramas Sankey")
st.subheader("Sistema Energético Colombiano")
st.markdown("---")

# Inicializar BD si no existe
crear_bd()

# Si no hay datos, cargar respaldo automáticamente
import pandas as pd
import os
from db import obtener_periodos, insertar_flujos

periodos = obtener_periodos()
if not periodos:
    respaldo_path = os.path.join(os.path.dirname(__file__), 'datos', 'flujos_respaldo.csv')
    if os.path.exists(respaldo_path):
        df_respaldo = pd.read_csv(respaldo_path, encoding='utf-8')
        insertar_flujos(df_respaldo)
        print("Datos de respaldo cargados automáticamente.")

# ------------------------------------------------------------
# BARRA LATERAL - NAVEGACIÓN
# ------------------------------------------------------------
st.sidebar.title("Menú Principal")
opcion = st.sidebar.radio(
    "Selecciona una sección:",
    ["📥 Extraer Datos", "📊 Generar Gráfico", "⚙️ Administrar Fuentes"]
)

# ------------------------------------------------------------
# SECCIÓN 1: EXTRACCIÓN DE DATOS
# ------------------------------------------------------------
if opcion == "📥 Extraer Datos":
    st.header("📥 Extracción de Datos desde Fuentes Oficiales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Extracción Manual")
        if st.button("🚀 Extraer Datos Ahora", type="primary", use_container_width=True):
            with st.spinner("Extrayendo datos de fuentes oficiales..."):
                total = ejecutar_extraccion_completa()
            if total > 0:
                st.success(f"✅ Extracción completada. {total} registros nuevos guardados.")
            else:
                st.warning("⚠️ No se obtuvieron datos. Verifica las URLs de las fuentes.")
    
    with col2:
        st.subheader("Extracción Programada")
        st.info("🕐 La extracción automática se ejecutará diariamente a las 08:00 AM.")
        if st.button("⏰ Iniciar Programador", use_container_width=True):
            st.session_state.scheduler_started = True
            st.success("Programador iniciado. Los datos se actualizarán automáticamente.")
    
    st.markdown("---")
    st.subheader("📋 Registro de Fuentes Configuradas")
    fuentes = obtener_fuentes_activas()
    if fuentes:
        df_fuentes = pd.DataFrame(fuentes)
        st.dataframe(df_fuentes[['nombre', 'url', 'tipo']], use_container_width=True)
    else:
        st.warning("No hay fuentes configuradas. Ve a 'Administrar Fuentes' para agregar.")

    st.markdown("---")
    st.subheader("📤 Actualizar datos desde archivo CSV")
    st.caption("Sube un archivo CSV con columnas: origen, destino, valor, periodo, fuente")
    archivo_subido = st.file_uploader("Selecciona un archivo CSV", type="csv")
    if archivo_subido is not None:
        df_nuevo = pd.read_csv(archivo_subido, encoding='utf-8')
        insertados = insertar_flujos(df_nuevo)
        st.success(f"✅ {insertados} registros añadidos a la base de datos.")
        st.caption("Ve a 'Generar Gráfico' para visualizar el nuevo período.")
# ------------------------------------------------------------
# SECCIÓN 2: GENERAR GRÁFICO
# ------------------------------------------------------------
elif opcion == "📊 Generar Gráfico":
    st.header("📊 Generar Diagrama Sankey")
    
    # Obtener períodos disponibles
    periodos = obtener_periodos()
    if not periodos:
        st.warning("⚠️ No hay datos en la base de datos. Primero extrae datos desde 'Extraer Datos'.")
    else:
        # Filtros en columnas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            periodo_seleccionado = st.selectbox("📅 Período:", periodos)
        
        with col2:
            incluir_export = st.checkbox("Mostrar exportaciones", value=True)
            incluir_import = st.checkbox("Mostrar importaciones", value=True)
            incluir_perdidas = st.checkbox("Mostrar pérdidas", value=True)
        
        with col3:
            st.subheader("Excluir fuentes:")
            excluir_hidro = st.checkbox("Hidroeléctrica", value=False)
            excluir_termica = st.checkbox("Térmica", value=False)
            excluir_solar = st.checkbox("Solar", value=False)
            excluir_eolica = st.checkbox("Eólica", value=False)
            excluir_gas = st.checkbox("Gas natural", value=False)
            excluir_carbon = st.checkbox("Carbón", value=False)
        
        # Construir lista de fuentes a excluir
        fuentes_excluir = []
        if excluir_hidro: fuentes_excluir.append('Hidroeléctrica')
        if excluir_termica: fuentes_excluir.append('Térmica (gas)')
        if excluir_solar: fuentes_excluir.append('Solar FV')
        if excluir_eolica: fuentes_excluir.append('Eólica')
        if excluir_gas: fuentes_excluir.append('Gas natural')
        if excluir_carbon: fuentes_excluir.append('Carbón')
        
        # Botón para generar
        if st.button("🎨 Generar Diagrama Sankey", type="primary", use_container_width=True):
            with st.spinner("Generando diagrama..."):
                # Obtener datos del período seleccionado
                df = obtener_flujos(periodo=periodo_seleccionado)
                
                if df.empty:
                    st.error("No se encontraron datos para el período seleccionado.")
                else:
                    # Generar Sankey con filtros
                    fig = generar_sankey_con_filtros(
                        df,
                        incluir_exportaciones=incluir_export,
                        incluir_importaciones=incluir_import,
                        incluir_perdidas=incluir_perdidas,
                        fuentes_excluir=fuentes_excluir if fuentes_excluir else None
                    )
                    
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Mostrar datos en tabla expandible
                        with st.expander("📋 Ver datos del gráfico"):
                            st.dataframe(df, use_container_width=True)
                        
                        # Botón de descarga
                        st.download_button(
                            label="📥 Descargar datos (CSV)",
                            data=df.to_csv(index=False).encode('utf-8'),
                            file_name=f'flujos_energia_{periodo_seleccionado}.csv',
                            mime='text/csv'
                        )
                    else:
                        st.error("No se pudo generar el diagrama con los filtros seleccionados.")

# ------------------------------------------------------------
# SECCIÓN 3: ADMINISTRAR FUENTES
# ------------------------------------------------------------
elif opcion == "⚙️ Administrar Fuentes":
    st.header("⚙️ Administración de Fuentes de Datos")
    
    tab1, tab2 = st.tabs(["📋 Ver Fuentes", "➕ Agregar Fuente"])
    
    # Pestaña 1: Ver fuentes existentes
    with tab1:
        st.subheader("Fuentes Configuradas")
        fuentes = obtener_fuentes_activas()
        if fuentes:
            for fuente in fuentes:
                with st.expander(f"📌 {fuente['nombre']} ({fuente['tipo'].upper()})"):
                    st.text(f"URL: {fuente['url']}")
                    st.text(f"Estado: {'Activo' if fuente['activo'] else 'Inactivo'}")
                    st.text(f"Reglas: {fuente['reglas_extraccion']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🗑️ Eliminar {fuente['nombre']}", key=f"del_{fuente['id']}"):
                            eliminar_fuente(fuente['id'])
                            st.success("Fuente eliminada.")
                            st.rerun()
        else:
            st.info("No hay fuentes configuradas.")
    
    # Pestaña 2: Agregar nueva fuente
    with tab2:
        st.subheader("Agregar Nueva Fuente")
        with st.form("form_nueva_fuente"):
            nombre = st.text_input("Nombre de la fuente", placeholder="Ej: XM Generación")
            url = st.text_input("URL de la fuente", placeholder="https://...")
            tipo = st.selectbox("Tipo de archivo", ["csv", "excel"])
            
            st.markdown("**Reglas de extracción (JSON):**")
            st.caption("Define columnas: col_origen, col_destino, col_valor, factor_conversion, periodo")
            reglas_default = '{"col_origen":"","col_destino":"","col_valor":"","factor_conversion":1.0,"periodo":"2024","nombre_fuente":""}'
            reglas = st.text_area("Reglas JSON", value=reglas_default, height=150)
            
            submitted = st.form_submit_button("💾 Guardar Fuente", type="primary")
            if submitted:
                if nombre and url and reglas:
                    import json
                    try:
                        json.loads(reglas)  # Validar JSON
                        agregar_fuente(nombre, url, tipo, reglas, activo=1)
                        st.success(f"✅ Fuente '{nombre}' agregada correctamente.")
                    except json.JSONDecodeError:
                        st.error("❌ Las reglas no son un JSON válido.")
                else:
                    st.error("❌ Completa todos los campos.")

# ------------------------------------------------------------
# PIE DE PÁGINA
# ------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.caption(f"Versión 1.0 | {datetime.now().strftime('%Y-%m-%d')}")
st.sidebar.caption("Fuentes: UPME, XM, ANH")