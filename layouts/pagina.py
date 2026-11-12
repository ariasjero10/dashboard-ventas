# Diseño de la página (sección 5 del archivo original).
# Aquí solo se define lo que se VE: títulos, filtro, mapa, cajas e indicadores.

from dash import html, dcc

from data.carga_datos import ingresos_estado, estado_inicial
from layouts.graficos import figura_mapa

ESTILO_CAJA = {
    "flex": "1 1 150px",
    "background": "white",
    "border": "1px solid #ddd",
    "borderRadius": "8px",
    "padding": "12px",
}


def caja(titulo, id_valor):
    return html.Div([
        html.Div(titulo, style={"fontSize": 13, "color": "#555"}),
        html.Div(id=id_valor, style={"fontSize": 22, "fontWeight": "bold", "marginTop": 4}),
    ], style=ESTILO_CAJA)


layout = html.Div([
    html.H1("Ventas por estado", style={"margin": "0 0 12px"}),

    html.Label("Selecciona un estado (o haz clic en el mapa):"),
    dcc.Dropdown(
        id="filtro-estado",
        options=sorted(ingresos_estado["estado"]),
        value=estado_inicial,
        clearable=False,
        style={"maxWidth": 400, "marginBottom": 16},
    ),

    html.Div([
        # Izquierda: el mapa grande
        html.Div([
            html.H3("Ingresos por estado", style={"margin": "0 0 8px"}),
            dcc.Graph(id="mapa", figure=figura_mapa(estado_inicial), style={"height": 620}),
        ], style={"flex": "3 1 420px", "minWidth": 0}),

        # Derecha: los indicadores del estado seleccionado
        html.Div([
            html.H3(id="titulo-estado", style={"margin": "0 0 8px"}),
            html.Div([
                caja("Categoría líder", "categoria"),
                caja("Uso de promoción", "promo"),
                caja("Tasa de cancelación", "cancelacion"),
                caja("Ticket con promoción", "ticket-con"),
                caja("Ticket sin promoción", "ticket-sin"),
            ], style={"display": "flex", "flexWrap": "wrap", "gap": 10, "marginBottom": 12}),
            html.H4("Tendencia mensual de ventas", style={"margin": "0 0 4px"}),
            dcc.Graph(id="tendencia", style={"height": 260}),
        ], style={"flex": "2 1 340px", "minWidth": 0}),

        # Abajo: gráfico de barras que cambia entre estados y productos
        html.Div([
            html.H3("Ranking de ingresos", style={"margin": "0 0 8px"}),
            dcc.RadioItems(
                id="selector-barras",
                options=[
                    {"label": "Top 9 estados", "value": "estados"},
                    {"label": "Productos (toda India)", "value": "productos"},
                ],
                value="estados",
                inline=True,
                style={"marginBottom": 8},
            ),
            dcc.Graph(id="barras", style={"height": 380}),
        ], style={"marginTop": 20}),
        
    ], style={"display": "flex", "flexWrap": "wrap", "gap": 20}),


], style={"fontFamily": "Arial, sans-serif", "padding": 20, "background": "#fafafa"})
