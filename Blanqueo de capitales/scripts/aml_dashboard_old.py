import streamlit as st
import pandas as pd
import requests
import altair as alt
import base64
import subprocess
from datetime import datetime
import os
import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib
from email.header import Header
from email.utils import formataddr
from email.mime.application import MIMEApplication

st.set_page_config(layout="wide")
st.title("📊 Platformline-IA AML Dashboard")

# Botón técnico para acceder a Swagger API manualmente
if getpass.getuser() in ["nacho", "root"]:
    with st.expander("🔧 Herramientas Técnicas Avanzadas"):
        if st.button("⚠️ Ver Documentación Técnica (Swagger API)", help="Acceso reservado a usuarios técnicos para pruebas y validación de endpoints.", type="primary"):
            subprocess.Popen(["xdg-open", f"http://localhost:8010/docs"])

BACKEND = "http://localhost:8010"
df = pd.DataFrame()
sospechosas = pd.DataFrame()

# KPIs
st.subheader("📉 Indicadores Clave de Riesgo")
try:
    data_kpis = requests.get(f"{BACKEND}/kpis").json()
    kpi_cols = st.columns(4)
    kpi_cols[0].metric("Transacciones", data_kpis['total_transacciones'])
    kpi_cols[1].metric("Alertas", data_kpis['total_alertas'])
    kpi_cols[2].metric("Monto alto", data_kpis['montos_altos'])
    kpi_cols[3].metric("% Alertas", f"{data_kpis['porcentaje_sospechosas']}%")
except:
    st.error("No se pudo obtener KPIs del backend")

# KPIs avanzados
st.subheader("💖 Análisis Avanzado de Riesgo")
try:
    tabla_avz = requests.get(f"{BACKEND}/kpis_avanzados").json()
    df_alertas = pd.DataFrame(tabla_avz)
    st.dataframe(df_alertas)
except:
    st.error("No se pudo cargar KPIs avanzados")

# Gráficos
st.subheader("📈 Gráficos de Riesgo")
try:
    if not df_alertas.empty:
        df_alertas['suma_montos'] = pd.to_numeric(df_alertas['suma_montos'], errors='coerce')
        df_alertas['num_sospechosas'] = pd.to_numeric(df_alertas['num_sospechosas'], errors='coerce')

        chart = alt.Chart(df_alertas).mark_circle(size=200, color='orange').encode(
            x=alt.X('pais_origen:N', title='País de Origen'),
            y=alt.Y('suma_montos:Q', title='Suma de Montos (€)', axis=alt.Axis(format=',.0f')),
            size='num_sospechosas:Q',
            tooltip=['pais_origen', 'suma_montos', 'num_sospechosas']
        ).properties(
            width=700,
            height=400,
            title='🚨 Riesgo por País: Monto Total y Número de Alertas'
        )

        st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.error(f"Error gráfico: {e}")

# Carga CSV
st.subheader("📂 Carga Masiva de Transacciones")
archivo = st.file_uploader("Selecciona un archivo CSV con transacciones", type="csv")
if archivo is not None:
    try:
        files = {"file": (archivo.name, archivo.getvalue(), "text/csv")}
        r = requests.post(f"{BACKEND}/transacciones_csv", files=files)
        if r.status_code == 200:
            st.success(r.json()["mensaje"])
        else:
            st.error(f"Error {r.status_code}: {r.text}")
    except Exception as e:
        st.error(str(e))

# Transacciones
st.subheader("📋 Transacciones Registradas")
try:
    data_trans = requests.get(f"{BACKEND}/transacciones").json()
    if data_trans:
        df = pd.DataFrame(data_trans)
        df['monto'] = pd.to_numeric(df['monto'])
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['dia_semana'] = df['fecha'].dt.dayofweek
        df['sospechosa'] = (
            (df['monto'] > 10000) |
            ((df['monto'] > 5000) & (df['dia_semana'] >= 5)) |
            df.duplicated(subset=['cuenta_origen','cuenta_destino','monto','fecha'], keep=False)
        )

        sospechosas = df[df['sospechosa'] == True]

        def highlight_alert(row):
            return ['background-color: red; color: white' if row['sospechosa'] else '' for _ in row]

        st.dataframe(df.style.apply(highlight_alert, axis=1))
except:
    st.warning("No se pudo obtener transacciones")

# Sospechosas
st.subheader("🚨 Transacciones Sospechosas")
try:
    if not sospechosas.empty:
        st.dataframe(sospechosas)
    else:
        st.info("Sin transacciones sospechosas detectadas.")
except:
    st.warning("No se pudo calcular transacciones sospechosas")

# Herramientas
st.subheader("🛠 Herramientas")
col1, col2, col3 = st.columns([1,1,2])

with col1:
    if st.button("📄 Exportar solo alertas CSV", key="exportar_csv"):
        if not sospechosas.empty:
            csv_data = sospechosas.to_csv(index=False)
            b64 = base64.b64encode(csv_data.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="alertas.csv">Descargar CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

with col2:
    if st.button("📄 Generar Informe Técnico Ejecutivo", key="generar_informe"):
        try:
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usuario_actual = getpass.getuser()
            html_content = f"""
            <html>
            <head>
            <style>
                body {{ font-family: Arial; margin: 40px; background-color: #f4f8fb; }}
                h1 {{ background-color: #003366; color: white; padding: 20px; border-radius: 10px; }}
                h2 {{ color: #003366; margin-top: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ccc; padding: 10px; text-align: center; }}
                th {{ background-color: #d9eaf7; font-weight: bold; }}
                .alerta {{ background-color: #ffdddd; }}
                p {{ font-size: 16px; margin: 5px 0; }}
            </style>
            </head>
            <body>
                <h1>Informe Técnico Ejecutivo AML</h1>
                <p><strong>Empresa:</strong> <span style="background-color:#cce5ff; padding:3px 10px; border-radius:5px;">Platformline</span></p>
                <p><strong>Fecha de ejecución:</strong> {fecha_actual}</p>
                <p><strong>Generado por:</strong> {usuario_actual}</p>
                <p><strong>Total de Transacciones:</strong> {len(df)}</p>
                <p><strong>Alertas Detectadas:</strong> {len(sospechosas)}</p>
                <h2>Transacciones Sospechosas</h2>
                {sospechosas.to_html(classes='alerta', index=False)}
                <h2>🧠 Análisis de Riesgo</h2>
                <ul>
                    <li>Monto superior a 10.000 €.</li>
                    <li>Transferencias > 5.000 € realizadas en fin de semana.</li>
                    <li>Transacciones duplicadas origen-destino con mismo importe y fecha.</li>
                </ul>
                <h2>🛡 Recomendaciones de Mitigación</h2>
                <ul>
                    <li>Verificar con el cliente el motivo de la transferencia sospechosa.</li>
                    <li>Notificar a cumplimiento normativo si hay patrón inusual.</li>
                    <li>Registrar excepción en auditoría interna.</li>
                    <li>Seguimiento de cuentas implicadas los próximos 30 días.</li>
                </ul>
            </body>
            </html>
            """

            directorio = "/home/kali/nacho/practicas/informes"
            os.makedirs(directorio, exist_ok=True)
            nombre_archivo = os.path.join(directorio, f"informe_forense_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(html_content)

            st.success("✅ Informe generado correctamente.")
            st.info(f"📂 Ruta del informe: {nombre_archivo}")

            with open(nombre_archivo, "rb") as file:
                contenido = file.read()
                st.download_button(
                    label="📄 Descargar Informe HTML",
                    data=contenido,
                    file_name=os.path.basename(nombre_archivo),
                    mime="text/html"
                )
                sha256_hash = hashlib.sha256(contenido).hexdigest()
                st.code(f"SHA256: {sha256_hash}", language="bash")

        except Exception as e:
            st.error(f"❌ Error generando informe: {e}")

with col3:
    st.subheader("🕵️ Auditoría Forense del Sistema")
    colbtn, colform = st.columns([1,2])

    with colbtn:
        if st.button("🔍 Ejecutar Auditoría Forense", key="auditoria"):
            st.write("Ejecutando Forensic Toolkit PRO...")
            ruta = "/home/kali/nacho/scripts/forensis.py"
            if os.path.exists(ruta):
                try:
                    result = subprocess.run(["python3", ruta], capture_output=True, text=True)
                    st.text_area("📃 Resultado del Análisis Forense", result.stdout if result.stdout else result.stderr, height=400)
                except Exception as e:
                    st.error(f"Error ejecutando forensis.py: {e}")
            else:
                st.warning("Script forensis.py no encontrado en ~/nacho/scripts/")

    with colform:
        st.markdown("### 📧 Enviar Informe Forense por Email")
        with st.form("formulario_envio"):
            destinatario = st.text_input("Dirección de correo del destinatario:", placeholder="ejemplo@gmail.com")
            asunto = st.text_input("Asunto del correo:", value="Informe Forense - Platformline")
            mensaje = st.text_area("Mensaje opcional:", height=100)
            enviar = st.form_submit_button("📤 Enviar Informe")

            if enviar:
                informes_path = "/home/kali/nacho/practicas/informes"
                if os.path.exists(informes_path):
                    lista_archivos = sorted(
                        [f for f in os.listdir(informes_path) if f.startswith("informe_forense_dashboard") and f.endswith(".html")],
                        reverse=True
                    )
                    if lista_archivos:
                        archivo_html = os.path.join(informes_path, lista_archivos[0])
                        try:
                            remitente = "tucuenta@gmail.com"
                            password = "tu_contraseña_de_aplicacion"

                            msg = MIMEMultipart()
                            msg['From'] = formataddr((str(Header('Plataforma AML', 'utf-8')), remitente))
                            msg['To'] = destinatario
                            msg['Subject'] = Header(asunto, 'utf-8')

                            msg.attach(MIMEText(mensaje, 'plain', 'utf-8'))
                            with open(archivo_html, "r", encoding="utf-8") as f:
                                html = f.read()
                            msg.attach(MIMEText(html, 'html', 'utf-8'))

                            with open(archivo_html, "rb") as f:
                                part = MIMEApplication(f.read(), Name=os.path.basename(archivo_html))
                                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(archivo_html)}"'
                                msg.attach(part)

                            server = smtplib.SMTP("smtp.gmail.com", 587)
                            server.starttls()
                            server.login(remitente, password)
                            server.send_message(msg)
                            server.quit()
                            st.success("✅ Correo enviado correctamente.")
                        except Exception as e:
                            st.error(f"❌ Error al enviar el correo: {e}")
                    else:
                        st.error("No se encuentra ningún archivo de informe HTML en la carpeta de informes.")
                else:
                    st.error("La carpeta de informes no existe.")
