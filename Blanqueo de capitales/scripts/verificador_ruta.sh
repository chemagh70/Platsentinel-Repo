#!/bin/bash

# Archivos críticos que deben estar en ruta persistente
ARCHIVOS_CLAVE=(
  "aml_dashboard.py"
  "dashboard_integrado_aml.py"
  "main_sql.py"
  "forensic_toolkit_pro.sh"
  "lanzar_suite_aml.sh"
)

# Rutas consideradas volátiles
RUTAS_VOLATILES=("/tmp" "/run" "/dev/shm")

echo "🔍 Verificando ubicaciones de archivos clave..."
problemas=0

for archivo in "${ARCHIVOS_CLAVE[@]}"; do
  ubicacion=$(find / -type f -name "$archivo" 2>/dev/null | head -n 1)
  if [ -z "$ubicacion" ]; then
    echo "[✗] No encontrado: $archivo"
    ((problemas++))
  else
    for ruta_tmp in "${RUTAS_VOLATILES[@]}"; do
      if [[ "$ubicacion" == $ruta_tmp* ]]; then
        echo "[⚠️] $archivo está en ruta volátil: $ubicacion"
        ((problemas++))
      fi
    done
    echo "[✔] Encontrado en: $ubicacion"
  fi
  echo "---------------------------------------"
done

if [ $problemas -gt 0 ]; then
  echo -e "\n❌ Se encontraron archivos en ubicaciones volátiles o no disponibles."
  echo "💡 Mueve esos archivos a una ruta persistente como /home/kali/nacho"
else
  echo -e "\n✅ Todos los archivos están en rutas seguras."
fi
