# Cálculo y formato de los indicadores (parte de la sección 4 del archivo original).

import pandas as pd

from data.carga_datos import ventas, pedidos_venta, todos_los_pedidos


def rupias(valor):
    return "—" if pd.isna(valor) else f"₹ {valor:,.0f}"


def porcentaje(valor):
    return "—" if pd.isna(valor) else f"{valor:.1%}"


def calcular_indicadores(estado):
    ventas_estado = ventas[ventas["estado"] == estado]
    pedidos_estado = pedidos_venta[pedidos_venta["estado"] == estado]
    todos_estado = todos_los_pedidos[todos_los_pedidos["estado"] == estado]

    por_categoria = ventas_estado.groupby("categoria")["Amount"].sum()
    return {
        "categoria": por_categoria.idxmax() if por_categoria.sum() > 0 else "—",
        "promo": pedidos_estado["con_promo"].mean(),
        "ticket_con": pedidos_estado.loc[pedidos_estado["con_promo"], "ingreso"].mean(),
        "ticket_sin": pedidos_estado.loc[~pedidos_estado["con_promo"], "ingreso"].mean(),
        "cancelacion": todos_estado["cancelado"].mean(),
    }
