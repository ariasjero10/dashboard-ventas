# Interactividad (sección 6 del archivo original).
# Único cambio: "@app.callback" pasa a "@callback", porque en este archivo no existe la variable app.
# Dash registra estos callbacks automáticamente cuando app.py importa este archivo.

from dash import callback, Input, Output, Patch

from data.indicadores import calcular_indicadores, porcentaje, rupias
from layouts.graficos import bordes_mapa, figura_barras, figura_tendencia


@callback(
    Output("filtro-estado", "value"),
    Input("mapa", "clickData"),
    prevent_initial_call=True,
)
def clic_en_mapa(clic):
    return clic["points"][0]["location"]


@callback(
    Output("mapa", "figure"),
    Output("titulo-estado", "children"),
    Output("categoria", "children"),
    Output("promo", "children"),
    Output("cancelacion", "children"),
    Output("ticket-con", "children"),
    Output("ticket-sin", "children"),
    Output("tendencia", "figure"),
    Input("filtro-estado", "value"),
)
def actualizar(estado):
    datos = calcular_indicadores(estado)

    # Solo cambia los bordes: así no se vuelve a enviar el mapa completo en cada selección.
    colores, grosores = bordes_mapa(estado)
    mapa = Patch()
    mapa["data"][0]["marker"]["line"]["color"] = colores
    mapa["data"][0]["marker"]["line"]["width"] = grosores

    return (
        mapa,
        estado,
        datos["categoria"],
        porcentaje(datos["promo"]),
        porcentaje(datos["cancelacion"]),
        rupias(datos["ticket_con"]),
        rupias(datos["ticket_sin"]),
        figura_tendencia(estado),
    )

@callback(
    Output("barras", "figure"),
    Input("selector-barras", "value"),
)
def actualizar_barras(vista):
    return figura_barras(vista)
