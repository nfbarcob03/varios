#!/bin/bash

# Crear una estructura de directorios de prueba
mkdir -p prueba_origen/
mkdir -p prueba_destino/

# Crear archivos de prueba
touch ./prueba_origen/archivo1.txt
touch prueba_origen/archivo2.txt
touch prueba_origen/archivo3.jpg
touch prueba_origen/archivo4.jpg
touch prueba_origen/archivo5.pdf
touch prueba_origen/archivo6.md

chmod +x ./organizador.sh

# Ejecutar el organizador con directorios de prueba
./organizador.sh organizar prueba_origen/ prueba_destino

# Listar el contenido del directorio de destino
echo "Contenido del directorio de destino:"
ls -R prueba_destino

# Realizar una búsqueda por nombre de archivo
read -p "Ingresa el nombre del archivo a buscar: " nombre_archivo
echo "Resultados de la búsqueda:"
organizador.sh buscar prueba_destino/ | grep "$nombre_archivo"

# Limpiar archivos de prueba
#rm -rf prueba_origen
#rm -rf prueba_destino