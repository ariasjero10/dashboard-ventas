# Dashboard de ventas por estado (Amazon Sale Report)

Dashboard en Dash que muestra los ingresos por estado de India en un mapa interactivo y, para el estado seleccionado, la categoría líder, el uso de promociones, la tasa de cancelación, el ticket promedio con y sin promoción y la tendencia mensual de ventas.

## Datos

- Ventas: dataset de Kaggle [Unlock Profits with E-commerce Sales Data](https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data) (archivo `Amazon Sale Report.csv`). Se descarga automáticamente con `kagglehub` al ejecutar la app.
- Mapa: GeoJSON de los estados de India ([adarshbiradar/maps-geojson](https://github.com/adarshbiradar/maps-geojson)).

## Estructura

```
tp2_dashboard/
├── app.py                  # Punto de entrada: crea la app, asigna el layout y la ejecuta
├── requirements.txt        # Librerías necesarias
├── README.md
├── data/
│   ├── carga_datos.py      # Descarga, limpieza y preparación de los datos
│   └── indicadores.py      # Cálculo y formato de los indicadores
├── layouts/
│   ├── graficos.py         # Figuras: mapa y tendencia mensual
│   └── pagina.py           # Estructura visual de la página
└── callbacks/
    └── interacciones.py    # Interactividad: clic en el mapa y actualización de indicadores
```

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python app.py
```

Luego abre http://127.0.0.1:8051/ en el navegador.

## Despliegue (Render)

Comando de inicio: `gunicorn app:server`
