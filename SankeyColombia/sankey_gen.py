import plotly.graph_objects as go
import pandas as pd

def generar_sankey(df, titulo="Diagrama Sankey - Sistema Energético Colombiano"):
    """
    Genera un diagrama Sankey a partir de un DataFrame con columnas:
    origen, destino, valor.
    
    Args:
        df: DataFrame con columnas [origen, destino, valor]
        titulo: str, título del gráfico
    
    Returns:
        fig: objeto Figure de Plotly
    """
    if df.empty:
        return None
    
    # Crear lista única de nodos ordenados alfabéticamente
    nodos = sorted(list(set(df['origen'].tolist() + df['destino'].tolist())))
    
    # Mapear cada nodo a un índice numérico
    nodo_a_indice = {nodo: i for i, nodo in enumerate(nodos)}
    
    # Convertir nombres de nodos a índices
    indices_origen = df['origen'].map(nodo_a_indice).tolist()
    indices_destino = df['destino'].map(nodo_a_indice).tolist()
    valores = df['valor'].tolist()
    
    # Crear figura Sankey
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodos,
            color="lightblue"
        ),
        link=dict(
            source=indices_origen,
            target=indices_destino,
            value=valores,
            color="rgba(0,100,200,0.2)"
        )
    )])
    
    fig.update_layout(
        title_text=titulo,
        font_size=10,
        height=600
    )
    
    return fig


def generar_sankey_con_filtros(df, incluir_exportaciones=True, incluir_importaciones=True,
                               incluir_perdidas=True, fuentes_excluir=None):
    """
    Genera un Sankey aplicando filtros adicionales.
    
    Args:
        df: DataFrame con los flujos
        incluir_exportaciones: bool
        incluir_importaciones: bool
        incluir_perdidas: bool
        fuentes_excluir: list, fuentes de energía a excluir (ej. ['Carbón', 'Petróleo crudo'])
    
    Returns:
        fig: objeto Figure de Plotly
    """
    df_filtrado = df.copy()
    
    # Filtrar exportaciones
    if not incluir_exportaciones:
        df_filtrado = df_filtrado[~df_filtrado['destino'].str.contains('Exportación', case=False)]
    
    # Filtrar importaciones
    if not incluir_importaciones:
        df_filtrado = df_filtrado[~df_filtrado['origen'].str.contains('Importación', case=False)]
    
    # Filtrar pérdidas
    if not incluir_perdidas:
        df_filtrado = df_filtrado[~df_filtrado['destino'].str.contains('Pérdida', case=False)]
    
    # Excluir fuentes específicas
    if fuentes_excluir:
        for fuente in fuentes_excluir:
            df_filtrado = df_filtrado[df_filtrado['origen'] != fuente]
    
    return generar_sankey(df_filtrado)