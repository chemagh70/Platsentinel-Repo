#!/bin/bash

echo "🔧 Limpieza segura iniciada..."

# 1. Limpiar caché de paquetes APT
echo "🧹 Limpiando caché de APT..."
sudo apt clean

# 2. Eliminar dependencias no necesarias
echo "🗑️ Eliminando paquetes huérfanos..."
sudo apt autoremove --purge -y

# 3. Limpiar caché de PIP
echo "📦 Limpiando caché de pip..."
pip cache purge

# 4. Mostrar carpetas pesadas para evaluación manual
echo -e "\n📊 Carpetas más grandes en raíz (TOP 10):"
sudo du -ahx / | sort -rh | head -n 10

# 5. Preguntar si desea eliminar Docker (si está instalado)
echo -e "\n❓ ¿Quieres eliminar Docker y liberar ~1.2GB? (s/n)"
read RESP
if [[ "$RESP" == "s" || "$RESP" == "S" ]]; then
  echo "🧨 Eliminando Docker y volúmenes..."
  sudo systemctl stop docker
  sudo apt purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo rm -rf /var/lib/docker
else
  echo "✅ Docker no será eliminado."
fi

echo -e "\n✅ Limpieza segura completada."
