#!/bin/bash

echo "Conviertiendo video..."

# Argumento 1: Ruta al video de entrada
video_entrada=$1

# Argumento 3: Ruta al video de salida
video_salida=$2

# Argumento 3: Ruta al video de salida temporal
video_salida_temporal="${video_salida}_temp.mp4"

# Argumento 4: Ruta a la imagen de entrada
imagen_entrada=$3
 
# mostrar la ruta actual
echo "Ruta actual: $(pwd)"
# mostrar ls
# echo "Contenido de la carpeta actual: $(ls)"

# Comando 1
ffmpeg -i "$video_entrada" -ss 0 -t 18 -vf "scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2" "$video_salida_temporal" -loglevel warning -y 

# Comando 2
ffmpeg -i "$imagen_entrada" -i "$video_salida_temporal" -i "$imagen_entrada" -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]" -map "[outv]" "$video_salida" -loglevel warning -y

# Eliminar video temporal
rm "$video_salida_temporal"

echo "Conversión completada."