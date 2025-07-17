#!/bin/bash

# === CONFIGURACIÓN ===
BASE_DIR="/home/kali/nacho/practicas"
VENV="$BASE_DIR/venv"
BACKEND_FILE="$BASE_DIR/main_sql.py"
DASHBOARD_FILE="$BASE_DIR/aml_dashboard.py"
BACKEND_PORT=8010
DASHBOARD_PORT=8501
LOG_DIR="$BASE_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/lanzamiento_$(date +%Y%m%d).log"

exec > >(tee -a "$LOG_FILE") 2>&1

# === CABECERA ESTÉTICA ===
echo -e "\n\e[1;34m═══════════════════════════════════════════════════"
echo -e "🔐 Lanzando Menarguez-IA AML Suite Integrada"
echo -e "═══════════════════════════════════════════════════\e[0m"
echo -e "🕒 Inicio: $(date)\n"

# === VERIFICACIÓN DE RUTAS SEGURAS ===
echo -e "\e[1;36m[*] Verificando rutas críticas...\e[0m"
ARCHIVOS_CLAVE=("main_sql.py" "aml_dashboard.py" "forensic_toolkit_pro.sh")
RUTAS_VOLATILES=("/tmp" "/run" "/dev/shm")
problemas=0

for archivo in "${ARCHIVOS_CLAVE[@]}"; do
  ubicacion=$(find "$BASE_DIR" -type f -name "$archivo" 2>/dev/null | head -n 1)
  if [ -z "$ubicacion" ]; then
    echo -e "\e[1;31m[✗] No encontrado: $archivo\e[0m"
    ((problemas++))
  else
    for ruta_tmp in "${RUTAS_VOLATILES[@]}"; do
      if [[ "$ubicacion" == $ruta_tmp* ]]; then
        echo -e "\e[1;33m[⚠️] $archivo está en ruta volátil: $ubicacion\e[0m"
        ((problemas++))
      fi
    done
    echo -e "\e[1;32m[✔] $archivo ubicado en: $ubicacion\e[0m"
  fi
  echo "---------------------------------------"
done

if [ $problemas -gt 0 ]; then
  echo -e "\n\e[1;31m❌ Detenido: se detectaron archivos en ubicaciones volátiles o ausentes.\e[0m"
  exit 2
fi

# === FUNCIÓN PARA INICIAR BACKEND ===
function lanzar_backend() {
  echo -e "\n\e[1;36m[*] Lanzando backend FastAPI en puerto $BACKEND_PORT...\e[0m"
  fuser -k ${BACKEND_PORT}/tcp &>/dev/null
  cd "$BASE_DIR" || { echo "❌ ERROR: No se encuentra $BASE_DIR"; exit 1; }
  source "$VENV/bin/activate"
  uvicorn main_sql:app --port $BACKEND_PORT &
  sleep 2
}

# === FUNCIÓN PARA INICIAR DASHBOARD ===
function lanzar_dashboard() {
  echo -e "\n\e[1;36m[*] Lanzando dashboard Streamlit en puerto $DASHBOARD_PORT...\e[0m"
  fuser -k ${DASHBOARD_PORT}/tcp &>/dev/null
  cd "$BASE_DIR"
  source "$VENV/bin/activate"
  streamlit run "$DASHBOARD_FILE" --server.port $DASHBOARD_PORT &
  sleep 3
}

# === EJECUCIÓN ===
if [ ! -d "$VENV" ]; then
  echo -e "\e[1;33m[+] Creando entorno virtual...\e[0m"
  python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
echo -e "\e[1;36m[*] Instalando dependencias requeridas...\e[0m"
pip install --quiet streamlit pandas uvicorn chardet

# Crear base de datos si no existe
if [ ! -f "$BASE_DIR/aml_data.db" ]; then
  echo -e "\e[1;33m[*] Ejecutando $BACKEND_FILE para generar base de datos inicial...\e[0m"
  python3 "$BACKEND_FILE"
fi

lanzar_backend
lanzar_dashboard

# === INFORMACIÓN FINAL ===
echo -e "\n\e[1;32m✅ Todo lanzado correctamente.\e[0m"
echo -e "🌐 Local URL   : \e[1;34m\e[4mhttp://localhost:$DASHBOARD_PORT\e[0m"
echo -e "📡 Swagger API : \e[1;34m\e[4mhttp://127.0.0.1:$BACKEND_PORT/docs\e[0m"
echo -e "🧾 Log guardado en: $LOG_FILE"

wait

echo -e "\n\e[1;34m===== FIN DE EJECUCIÓN: $(date) =====\e[0m\n"
