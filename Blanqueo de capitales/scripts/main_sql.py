from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
from datetime import datetime
import io
import csv

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulación de base de datos en memoria
transacciones_db = []

# Modelo de datos
class Transaccion(BaseModel):
    cuenta_origen: str
    cuenta_destino: str
    monto: float
    fecha: str
    pais_origen: str
    pais_destino: str
    canal: str

# Endpoints principales
@app.get("/kpis")
def obtener_kpis():
    total = len(transacciones_db)
    alertas = sum(1 for t in transacciones_db if t["monto"] > 10000)
    altos = sum(1 for t in transacciones_db if t["monto"] > 5000)
    porcentaje = (alertas / total * 100) if total else 0.0
    return {
        "total_transacciones": total,
        "total_alertas": alertas,
        "montos_altos": altos,
        "porcentaje_sospechosas": round(porcentaje, 2)
    }

@app.get("/transacciones")
def listar_transacciones():
    return transacciones_db

@app.post("/transacciones")
def registrar_transaccion(t: Transaccion):
    transacciones_db.append(t.dict())
    return {"status": "ok"}

@app.get("/kpis_avanzados")
def obtener_kpis_avanzados():
    if not transacciones_db:
        return []

    df = pd.DataFrame(transacciones_db)
    df['monto'] = pd.to_numeric(df['monto'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['dia_semana'] = df['fecha'].dt.dayofweek

    # Reglas AML
    df['sospechosa'] = (
        (df['monto'] > 10000) |
        ((df['monto'] > 5000) & (df['dia_semana'] >= 5)) |
        df.duplicated(subset=['cuenta_origen', 'cuenta_destino', 'monto', 'fecha'], keep=False)
    )

    resumen = df.groupby(['pais_origen', 'pais_destino']).agg({
        'monto': ['count', 'sum', 'mean'],
        'sospechosa': 'sum'
    }).reset_index()

    resumen.columns = ['pais_origen', 'pais_destino', 'num_transacciones', 'suma_montos', 'promedio_montos', 'num_sospechosas']
    return resumen.to_dict(orient='records')

@app.get("/sospechosas")
def transacciones_sospechosas():
    if not transacciones_db:
        return []
    df = pd.DataFrame(transacciones_db)
    df['monto'] = pd.to_numeric(df['monto'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['dia_semana'] = df['fecha'].dt.dayofweek
    df['sospechosa'] = (
        (df['monto'] > 10000) |
        ((df['monto'] > 5000) & (df['dia_semana'] >= 5)) |
        df.duplicated(subset=['cuenta_origen', 'cuenta_destino', 'monto', 'fecha'], keep=False)
    )
    return df[df['sospechosa']].to_dict(orient='records')

@app.post("/transacciones_csv")
def registrar_csv(file: UploadFile = File(...)):
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    cargadas = 0
    for row in reader:
        try:
            row["monto"] = float(row["monto"])
            row["fecha"] = str(row["fecha"])
            transacciones_db.append(row)
            cargadas += 1
        except Exception as e:
            continue
    return {"mensaje": f"Se cargaron {cargadas} transacciones."}

@app.get("/reporte_alertas_csv")
def descargar_alertas_csv():
    if not transacciones_db:
        return ""
    df = pd.DataFrame(transacciones_db)
    df['monto'] = pd.to_numeric(df['monto'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['dia_semana'] = df['fecha'].dt.dayofweek
    df['sospechosa'] = (
        (df['monto'] > 10000) |
        ((df['monto'] > 5000) & (df['dia_semana'] >= 5)) |
        df.duplicated(subset=['cuenta_origen', 'cuenta_destino', 'monto', 'fecha'], keep=False)
    )
    sospechosas = df[df['sospechosa']]
    output = io.StringIO()
    sospechosas.to_csv(output, index=False)
    return output.getvalue()

@app.get("/informe_ejecutivo")
def generar_informe_html():
    if not transacciones_db:
        return "<h3>No hay datos para generar el informe.</h3>"
    df = pd.DataFrame(transacciones_db)
    df['monto'] = pd.to_numeric(df['monto'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['dia_semana'] = df['fecha'].dt.dayofweek
    df['sospechosa'] = (
        (df['monto'] > 10000) |
        ((df['monto'] > 5000) & (df['dia_semana'] >= 5)) |
        df.duplicated(subset=['cuenta_origen', 'cuenta_destino', 'monto', 'fecha'], keep=False)
    )
    resumen = df.groupby(['pais_origen', 'pais_destino']).agg({
        'monto': ['count', 'sum', 'mean'],
        'sospechosa': 'sum'
    }).reset_index()
    resumen.columns = ['pais_origen', 'pais_destino', 'num_transacciones', 'suma_montos', 'promedio_montos', 'num_sospechosas']
    resumen_html = resumen.to_html(index=False, classes='table table-bordered table-striped')

    html_template = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px; }}
            h1 {{ color: #343a40; }}
            .table {{ border-collapse: collapse; width: 100%; }}
            .table th, .table td {{ border: 1px solid #dee2e6; padding: 8px; }}
            .table th {{ background-color: #007bff; color: white; }}
            .table-striped tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Informe Ejecutivo AML</h1>
        <p>Este informe presenta un resumen técnico del análisis de riesgos basado en las transacciones procesadas.</p>
        {resumen_html}
    </body>
    </html>
    """
    return html_template

@app.post("/forensics_upload")
async def subir_informe_forense(file: UploadFile = File(...)):
    contenido = await file.read()
    with open("informe_forense_dashboard.html", "wb") as f:
        f.write(contenido)
    return {"mensaje": "Informe forense recibido correctamente y guardado como informe_forense_dashboard.html"}

