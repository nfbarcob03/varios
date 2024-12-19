#!/bin/bash

# Archivo de registro
archivo_log="actividad_organizador.log"

# Mensaje informativo
mensaje_info() {
  echo "[INFO] $1"
}

# Mensaje de error
mensaje_error() {
  echo "[ERROR] $1" >&2
}




# Verificar la cantidad de parÃ¡metros
if [ "$#" -ne 3 ]; then
  echo "Uso: $0 <accion> <directorio_origen> <?directorio_destino> <?nombre_archivo>"
  echo "Uso: accion: buscar solo necesita directorio origen y nombre archivo"
  echo "Uso: accion: organizar necesita directorio origen y destino"
  exit 1
fi


accion="$1"
directorio_origen="$2"


if [ "$accion" == "buscar" ]; then
	  nombre_archivo="$3"
	  echo "Accion buscar"
	  mensaje_info "Buscando archivos por nombre: $nombre_archivo"
	  find "$directorio_origen" -type f -name "*$nombre_archivo*" -exec ls -l {} \;
  exit 1
fi


# Directorio de origen y destino
directorio_destino="$3"



# Verificar si el directorio de destino existe, si no, crearlo
if [ ! -d "$directorio_destino" ]; then
  mkdir -p "$directorio_destino"
  mensaje_info "Directorio de destino creado: $directorio_destino"
fi

# Clasificar archivos por extensiÃ³n
mensaje_info "Clasificando archivos..."
find "$directorio_origen" -type f | while read -r archivo; do
  extension=$(echo "$archivo" | awk -F. '{print tolower($NF)}')
  destino="$directorio_destino/$extension"
  
  if [ ! -d "$destino" ]; then
    mkdir -p "$destino"
  fi

  # Manejo de duplicados
  contador=0
  while [ -e  "$destino/$(basename $archivo)" ]; do
    contador=$((contador+1))
    archivo=$(echo "$archivo" | sed "s/\(.*\)\.\(.*\)/\1_$contador.\2/")
  done

  mv "$archivo" "$destino"
  mensaje_info "Movido: $archivo a $destino"
  echo "$(date) - Movido: $archivo a $destino" >> "$archivo_log"
done


# BÃºsqueda por nombre de archivo

mensaje_info "Â¡Proceso completado!"
