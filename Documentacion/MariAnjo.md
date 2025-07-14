# SENTINELCORE – DOCUMENTACIÓN TÉCNICA COMPLETA

## INTRODUCCIÓN

SentinelCore es una plataforma modular de ciberseguridad orientada a orquestar tareas técnicas como escaneos, auditorías y mitigación a través de contenedores Docker. Se puede operar desde un dashboard web o por mensajería instantánea como WhatsApp.

Este documento recopila toda la información técnica desarrollada para el MVP: tokens, scripts, estructura del bot, integración por API, exportación de resultados y despliegue en clústeres.



# SENTINELCORE – DOCUMENTACIÓN TÉCNICA COMPLETA (ACTUALIZADA)

## INTRODUCCIÓN

SentinelCore es una plataforma SaaS de ciberseguridad que permite orquestar tareas como escaneos, auditorías y mitigación desde un entorno web centralizado. Todos los servicios están integrados en un dashboard accesible por navegador, con soporte para activación vía WhatsApp o API REST.

---

## 1. FUNCIONALIDAD A TRAVÉS DE LA INTERFAZ WEB

### Estructura del dashboard

- Acceso vía login JWT
- Vista general del estado de la infraestructura
- Menú de navegación con las siguientes secciones:
  - **Herramientas**
    - Audit SSH
    - Webscanner (Nikto)
    - Escaneo de red (Nmap)
    - System Check
  - **Informes**
    - Generar informe PDF global
  - **Estado**
    - Monitoreo de tokens activos y métricas

Cada herramienta puede activarse con un clic, y su resultado aparece en pantalla, en formato JSON, texto o PDF descargable.

---

## 2. TOKENS INTEGRADOS EN EL PANEL

Cada token está conectado a un botón en la interfaz `/herramientas`. A través del frontend Vue.js, se realiza una llamada a la API REST y se despliega el resultado directamente en el panel.

### 2.1 token_webscanner (Nikto)
- Escaneo de vulnerabilidades web
- Entrada: URL
- Resultado: JSON + PDF

```python
subprocess.run(['nikto', '-h', target])
```

### 2.2 token_audit_ssh
- Auditoría de SSH
- Resultado: lista de configuraciones inseguras

### 2.3 token_nmap
- Escaneo de red
- Entrada: IP o dominio
- Resultado: listado de puertos y servicios

### 2.4 token_systemcheck
- Auditoría del sistema
- Resultado: usuarios, cronjobs, kernel, procesos

---

## 3. INTEGRACIÓN VÍA API

Las herramientas son llamadas desde el panel web mediante:

```js
POST /api/tokens/lanzar/token_webscanner
```

Esto activa un contenedor Docker en segundo plano que ejecuta la tarea y devuelve resultados procesados.

---

## 4. WHATSAPP COMO CANAL OPCIONAL

A través del bot WhatsApp (Twilio), se pueden lanzar comandos simples como:

```
/audit_ssh
/nmap 192.168.1.1
/webscan https://sitio.com
```

Estos comandos son útiles para activación remota sin abrir la web.

---

## 5. INFORMES

Los resultados de los tokens se almacenan temporalmente y pueden consolidarse en un informe PDF:

```bash
python informes/generador_informes.py
```

La función también está disponible desde el panel con un botón: "Generar Informe Global".

---

## 6. DESPLIEGUE CON K3S + HELM

- Backend y frontend se despliegan como servicios en un clúster K3s.
- Tokens funcionan como Jobs.
- Ingress + cert-manager manejan HTTPS.
- Monitoreo opcional con Prometheus y Grafana.

---

## 7. MEMORIA TÉCNICA

La arquitectura modular, contenedorizada y web-first de SentinelCore permite a los técnicos y MSPs escalar sus servicios sin perder control ni visibilidad. Todos los tokens son activables desde la interfaz web y devuelven resultados en tiempo real, almacenados de forma auditada.

Este diseño permite añadir nuevas herramientas sin modificar el core, integrarlas visualmente y operarlas desde un único lugar.

---


## 1. TOKENS IMPLEMENTADOS

### 1.1 `token_webscanner`
**Descripción:** Escaneo de vulnerabilidades web con Nikto.

**Script `escaneo.py`:**
```python
import subprocess
import sys
import json
from utils import generar_pdf
import os

def run_nikto_scan(target):
    resultado = subprocess.run(['nikto', '-h', target],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               timeout=60)
    return {"estado": "ok", "salida": resultado.stdout, "errores": resultado.stderr}

if __name__ == "__main__":
    url = sys.argv[1]
    resultado = run_nikto_scan(url)
    os.makedirs("/salida", exist_ok=True)
    json_path = "/salida/resultado.json"
    pdf_path = "/salida/resultado.pdf"
    with open(json_path, "w") as f:
        json.dump(resultado, f, indent=2)
    generar_pdf(resultado["salida"], pdf_path)
    print(json.dumps({"estado": resultado["estado"], "json": json_path, "pdf": pdf_path}))
```

---


### 1.2 `token_audit_ssh`
**Descripción:** Auditoría de configuraciones inseguras de SSH.

**Script `escaneo.py`:**
```python
import json
from pathlib import Path

def analizar_sshd_config():
    ruta = Path("/etc/ssh/sshd_config")
    hallazgos = []
    with open(ruta) as f:
        for linea in f:
            if "PermitRootLogin yes" in linea:
                hallazgos.append("❌ PermitRootLogin habilitado")
            if "PasswordAuthentication yes" in linea:
                hallazgos.append("⚠️ PasswordAuthentication habilitado")
    return {"estado": "ok", "hallazgos": hallazgos}

if __name__ == "__main__":
    print(json.dumps(analizar_sshd_config()))
```

---


### 1.3 `token_nmap`
**Descripción:** Escaneo de red y servicios.

**Script `escaneo.py`:**
```python
import subprocess
import sys
import json

def escanear(target):
    resultado = subprocess.run(["nmap", "-sV", target],
                               capture_output=True, text=True, timeout=60)
    return {"estado": "ok", "salida": resultado.stdout}

if __name__ == "__main__":
    print(json.dumps(escanear(sys.argv[1])))
```

---


### 1.4 `token_systemcheck`
**Descripción:** Auditoría del sistema operativo.

**Script `escaneo.py`:**
```python
import os
import json

def recolectar_info():
    return {
        "usuarios": os.popen("cut -d: -f1 /etc/passwd").read().splitlines(),
        "cron": os.popen("ls /etc/cron.*").read().splitlines(),
        "kernel": os.popen("uname -a").read().strip(),
        "procesos_raros": os.popen("ps aux | grep -v root").read().splitlines()
    }

if __name__ == "__main__":
    print(json.dumps(recolectar_info(), indent=2))
```

---


## 2. ESTRUCTURA DEL BOT WHATSAPP

**Archivo principal:** `bot-whatsapp/main.py`

```python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import subprocess

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    mensaje = request.form.get("Body", "").strip()
    respuesta = MessagingResponse()

    if mensaje.startswith("/nmap"):
        _, host = mensaje.split()
        salida = lanzar_token("token.nmap", host)
        respuesta.message(f"Nmap:
{salida[:1500]}")
    elif mensaje.startswith("/audit_ssh"):
        salida = lanzar_token("token_audit_ssh")
        respuesta.message(f"Audit SSH:
{salida[:1500]}")
    return str(respuesta)

def lanzar_token(token, param=None):
    cmd = ["docker", "run", "--rm", token]
    if param:
        cmd.append(param)
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    return resultado.stdout
```

---


## 3. INTEGRACIÓN POR API

**FastAPI – `tokens.py`:**
```python
@router.post("/tokens/lanzar/{nombre_token}")
def lanzar_token(nombre_token: str, url: Optional[str] = None):
    cmd = ["docker", "run", "--rm", nombre_token]
    if url:
        cmd.append(url)
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    return {"salida": resultado.stdout}
```

---


## 4. DASHBOARD WEB

- Construido en Vue 3 + Tailwind CSS
- Panel con pestañas: Tokens, Informes, Live Status
- Ejecuta tokens vía botones
- Muestra resultados JSON/PDF
- WebSockets para métricas en vivo

---


## 5. INFORMES AUTOMÁTICOS

**Script global:** `generador_informes.py`

```python
from fpdf import FPDF
import json, os

def generar_reporte_global(ruta_resultados="/tmp/salida", salida="/tmp/informe.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    for archivo in os.listdir(ruta_resultados):
        if archivo.endswith(".json"):
            with open(os.path.join(ruta_resultados, archivo)) as f:
                data = json.load(f)
                pdf.multi_cell(0, 6, json.dumps(data, indent=2))
    pdf.output(salida)
```

---


## 6. DESPLIEGUE CON HELM + K3S

1. Crear clúster:
```bash
curl -sfL https://get.k3s.io | sh -
```

2. Instalar API y UI con Helm:
```bash
helm install core-api ./charts/api
helm install core-ui ./charts/dashboard
```

3. Configurar Ingress + SSL
4. Desplegar tokens como Jobs o CronJobs

---


## MEMORIA TÉCNICA

Cada módulo fue desarrollado con enfoque de seguridad, portabilidad y extensibilidad. Los tokens son contenedores efímeros y auditables, activables desde múltiples canales. El sistema automatiza escaneos, genera informes y permite gestión centralizada con bajo coste operativo.

El objetivo de SentinelCore es democratizar la ciberseguridad avanzada para equipos técnicos de pequeña y mediana escala.