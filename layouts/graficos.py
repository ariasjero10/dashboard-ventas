# Funciones que construyen las figuras (parte de la sección 4 del archivo original).

import plotly.express as px

from data.carga_datos import mapa_india, ventas, ingresos_estado, meses_tendencia


def bordes_mapa(estado):
    # Resalta el estado seleccionado con un borde oscuro.
    colores = ["black" if e == estado else "#aaaaaa" for e in ingresos_estado["estado"]]
    grosores = [2.5 if e == estado else 0.5 for e in ingresos_estado["estado"]]
    return colores, grosores


def figura_mapa(estado):
    fig = px.choropleth(
        ingresos_estado,
        geojson=mapa_india,
        locations="estado",
        color="ingresos",
        color_continuous_scale="Blues",
        labels={"ingresos": "Ingresos (₹)", "estado": "Estado"},
    )
    colores, grosores = bordes_mapa(estado)
    fig.update_traces(marker_line_color=colores, marker_line_width=grosores)
    # Encuadre fijo sobre India, para que el mapa ocupe todo el espacio.
    fig.update_geos(visible=False, projection_type="mercator", lonaxis_range=[67, 98], lataxis_range=[6, 38])
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(orientation="h", x=0.5, xanchor="center", y=0, yanchor="top", len=0.6, thickness=12),
    )
    return fig


def figura_tendencia(estado):
    por_mes = ventas[ventas["estado"] == estado].groupby("mes")["Amount"].sum()
    por_mes = por_mes.reindex(meses_tendencia, fill_value=0).reset_index()
    fig = px.line(por_mes, x="mes", y="Amount", markers=True, labels={"mes": "Mes", "Amount": "Ingresos (₹)"})
    fig.update_xaxes(type="category")
    fig.update_yaxes(rangemode="tozero")
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white")
    return fig

def figura_barras(vista):
    # vista = "estados": los 9 estados con más ingresos.
    # vista = "productos": ingresos de cada categoría de producto en toda India.
    if vista == "estados":
        datos = ingresos_estado.nlargest(9, "ingresos")
        eje, nombre_eje = "estado", "Estado"
    else:
        datos = ventas.groupby("categoria")["Amount"].sum().reset_index(name="ingresos")
        datos = datos.sort_values("ingresos", ascending=False)
        eje, nombre_eje = "categoria", "Producto"

    fig = px.bar(
        datos, x=eje, y="ingresos", text_auto=".3s",
        labels={eje: nombre_eje, "ingresos": "Ingresos (₹)"},
    )
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white")
    return fig
