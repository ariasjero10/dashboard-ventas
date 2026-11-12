# Carga, limpieza y preparación de los datos (secciones 1, 2 y 3 del archivo original).
# El dataset se descarga desde Kaggle con kagglehub; aquí no se guarda ningún CSV.

import kagglehub
import pandas as pd
import requests

# ---------- 1. Cargar los datos ----------
ruta = kagglehub.dataset_download("thedevastator/unlock-profits-with-e-commerce-sales-data")
df = pd.read_csv(f"{ruta}/Amazon Sale Report.csv", low_memory=False)

url_mapa = "https://raw.githubusercontent.com/adarshbiradar/maps-geojson/master/india.json"

mapa_india = requests.get(url_mapa, timeout=30).json()

# ---------- 2. Limpiar los nombres de los estados ----------
# El archivo trae variantes como RJ, RAJSHTHAN o Orissa.
DADRA = "Dadra And Nagar Haveli And Daman And Diu"
CORRECCIONES = {
    "Rj": "Rajasthan",
    "Rajshthan": "Rajasthan",
    "Rajsthan": "Rajasthan",
    "Pb": "Punjab", "Punjab/Mohali/Zirakpur": "Punjab",
    "Ar": "Arunachal Pradesh",
    "Nl": "Nagaland",
    "Orissa": "Odisha",
    "Pondicherry": "Puducherry",
    "New Delhi": "Delhi",
    "Nct Of Delhi": "Delhi",
    "Andaman And Nicobar Islands": "Andaman And Nicobar",
    "Dadra And Nagar": DADRA,
    "Dadra And Nagar Haveli": DADRA,
    "Daman And Diu": DADRA,
}


def limpiar_estado(nombre):
    # "&" -> "And" para que "Jammu & Kashmir" coincida con "Jammu and Kashmir" del mapa.
    nombre = str(nombre).strip().title().replace("&", "And")
    return CORRECCIONES.get(nombre, nombre)


# El mapa usa la misma limpieza, para que los nombres coincidan con los datos.
for estado_mapa in mapa_india["features"]:
    estado_mapa["id"] = limpiar_estado(estado_mapa["properties"]["st_nm"])
estados_del_mapa = {estado_mapa["id"] for estado_mapa in mapa_india["features"]}

# ---------- 3. Preparar las columnas ----------
df = df.drop(columns="index").drop_duplicates()
df["estado"] = df["ship-state"].map(limpiar_estado)

excluidos = sorted(set(df["estado"]) - estados_del_mapa)
print("Valores fuera del mapa, excluidos:", excluidos)
df = df[df["estado"].isin(estados_del_mapa)].copy()

df["fecha"] = pd.to_datetime(df["Date"], format="%m-%d-%y")
df["mes"] = df["fecha"].dt.strftime("%Y-%m")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
df["categoria"] = df["Category"].str.strip().str.title()
df["con_promo"] = df["promotion-ids"].notna()
df["cancelada"] = df["Status"] == "Cancelled"

# Estas líneas no cuentan como venta: el dinero no entró o se devolvió.
SIN_VENTA = [
    "Cancelled", "Shipped - Returned to Seller", "Shipped - Returning to Seller",
    "Shipped - Rejected by Buyer", "Shipped - Lost in Transit", "Shipped - Damaged",
]
ventas = df[~df["Status"].isin(SIN_VENTA)]

# Un pedido puede tener varias líneas, así que las tasas y el ticket se calculan por pedido.
pedidos_venta = ventas.groupby("Order ID").agg(
    estado=("estado", "first"), ingreso=("Amount", "sum"), con_promo=("con_promo", "any")
).reset_index()
pedidos_venta = pedidos_venta[pedidos_venta["ingreso"] > 0]

todos_los_pedidos = df.groupby("Order ID").agg(
    estado=("estado", "first"), cancelado=("cancelada", "all")
).reset_index()

ingresos_estado = ventas.groupby("estado")["Amount"].sum().reset_index(name="ingresos")
estado_inicial = ingresos_estado.sort_values("ingresos").iloc[-1]["estado"]

# Marzo solo tiene un día de datos (31-mar): se deja fuera para no distorsionar la tendencia.
meses_tendencia = sorted(m for m in ventas["mes"].unique() if m != "2022-03")
