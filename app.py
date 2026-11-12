# MVP: dashboard de ventas por estado (Amazon Sale Report)
# Instalar: pip install -r requirements.txt
# Ejecutar (desde la carpeta tp2_dashboard): python app.py

import os

import dash

from layouts.pagina import layout
import callbacks.interacciones  # noqa: F401  (al importarlo se registran los callbacks)

app = dash.Dash(__name__, title="Ventas por estado")
server = app.server  # Servidor Flask que usa Gunicorn en el despliegue (Render).

app.layout = layout

if __name__ == "__main__":
    # En local abre http://127.0.0.1:8051/. En la nube el servicio define el puerto con la variable PORT.
    # debug=False quita el panel de errores/callbacks de Dash (la burbuja de la esquina inferior derecha).
    app.run(debug=False, port=int(os.environ.get("PORT", 8051)))
