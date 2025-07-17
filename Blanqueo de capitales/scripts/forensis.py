# forensis.py corregido y estructurado con presentación en tabla clara en interfaz y HTML
import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import datetime
import getpass
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import webbrowser

HTML_FILENAME = "informe_forense_dashboard.html"

class ForensicToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Forensic Toolkit PRO - Menarguez_IA-Solutions")
        self.root.geometry("1200x600")
        self.root.eval('tk::PlaceWindow . center')

        self.panel = ttk.Treeview(root)
        self.panel.grid(row=0, column=1, rowspan=10, padx=10, pady=10, sticky="nsew")
        self.scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=self.panel.yview)
        self.panel.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.grid(row=0, column=2, rowspan=10, sticky="ns")

        botones = [
            ("🧠 Procesos Activos", self.procesos_activos),
            ("🔍 Procesos Sospechosos", self.procesos_sospechosos),
            ("🌐 Conexiones de Red", self.conexiones_red),
            ("📁 Archivos Modificados", self.archivos_modificados),
            ("🧬 Info de Red", self.info_red),
            ("📡 Sniffer IP (50)", self.mostrar_sniffer_basico),
            ("📄 Generar Informe HTML", self.exportar_html_final),
            ("🌐 Abrir Informe HTML", self.abrir_informe_html),
            ("🚀 Ejecutar Todo", self.iniciar_analisis)
        ]

        for i, (texto, comando) in enumerate(botones):
            tk.Button(root, text=texto, command=comando).grid(row=i, column=0, sticky="ew")

    def mostrar_tabla(self, salida):
        filas = salida.strip().split("\n")
        if not filas:
            return
        headers = filas[0].split()
        self.panel.delete(*self.panel.get_children())
        self.panel["columns"] = headers
        self.panel["show"] = "headings"
        for col in headers:
            self.panel.heading(col, text=col)
            self.panel.column(col, width=80, anchor="center")
        for fila in filas[1:]:
            columnas = fila.split(None, len(headers)-1)
            self.panel.insert("", "end", values=columnas)

    def ejecutar(self, comando):
        return subprocess.getoutput(comando)

    def procesos_activos(self):
        salida = self.ejecutar("ps aux")
        self.mostrar_tabla(salida)

    def procesos_sospechosos(self):
        salida = self.ejecutar("ps aux | grep -v root | grep -E 'nc|ncat|bash|sh|perl|python'")
        self.mostrar_tabla(salida)

    def conexiones_red(self):
        salida = self.ejecutar("netstat -tunlp")
        self.mostrar_tabla(salida)

    def archivos_modificados(self):
        salida = self.ejecutar("find /home -type f -mtime -1 2>/dev/null | tail -n 20")
        self.panel.delete(*self.panel.get_children())
        self.panel["columns"] = ["Archivos Modificados"]
        self.panel["show"] = "headings"
        self.panel.heading("Archivos Modificados", text="Archivos Modificados")
        for fila in salida.splitlines():
            self.panel.insert("", "end", values=[fila])

    def info_red(self):
        salida = self.ejecutar("ip -br address")
        self.panel.delete(*self.panel.get_children())
        self.panel["columns"] = ["Dispositivo", "Estado", "Direcciones"]
        self.panel["show"] = "headings"
        self.panel.column("Dispositivo", width=120, anchor="center")
        self.panel.column("Estado", width=100, anchor="center")
        self.panel.column("Direcciones", width=300, anchor="w")
        for fila in salida.splitlines():
            columnas = fila.split(maxsplit=2)
            if len(columnas) == 3:
                self.panel.insert("", "end", values=columnas)

    def mostrar_sniffer_basico(self):
        salida = self.ejecutar("tcpdump -c 50 -n -i any 2>/dev/null")
        self.panel.delete(*self.panel.get_children())
        self.panel["columns"] = ["Sniffer"]
        self.panel["show"] = "headings"
        self.panel.heading("Sniffer", text="Sniffer")
        for fila in salida.splitlines():
            self.panel.insert("", "end", values=[fila])

    def exportar_html_final(self):
        contenido = ""
        columnas = self.panel["columns"]
        if columnas:
            contenido += "<table border='1'><tr>" + ''.join(f"<th>{col}</th>" for col in columnas) + "</tr>"
            for item in self.panel.get_children():
                fila = self.panel.item(item)['values']
                contenido += "<tr>" + ''.join(f"<td>{c}</td>" for c in fila) + "</tr>"
            contenido += "</table>"
        else:
            contenido = "<p>No se encontraron datos para exportar.</p>"

        with open(HTML_FILENAME, "w", encoding="utf-8") as f:
            f.write(f"<html><body>{contenido}</body></html>")

        try:
            with open(HTML_FILENAME, "rb") as f:
                r = requests.post("http://localhost:8010/forensics_upload", files={"file": (HTML_FILENAME, f, "text/html")})
            if r.status_code == 200:
                print("📡 Informe enviado al backend correctamente.")
            else:
                print(f"⚠️ Error al enviar informe: {r.status_code}")
        except Exception as e:
            print(f"❌ Fallo al conectar con backend: {e}")

    def abrir_informe_html(self):
        try:
            webbrowser.open(f"file://{os.path.abspath(HTML_FILENAME)}")
        except Exception as e:
            print(f"❌ No se pudo abrir el informe: {e}")

    def iniciar_analisis(self):
        self.procesos_activos()
        self.procesos_sospechosos()
        self.conexiones_red()
        self.archivos_modificados()
        self.info_red()
        self.mostrar_sniffer_basico()
        self.exportar_html_final()

if __name__ == "__main__":
    root = tk.Tk()
    app = ForensicToolkit(root)
    root.mainloop()
