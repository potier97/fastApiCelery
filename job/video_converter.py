import moviepy.editor as mp
import PIL
import os

# Ruta del video original
video_path = "job/video_original.mp4"

# Rutas de las imágenes para los frames inicial y final
frame_imagen_path = "job/frame.png"

# Duración máxima del video en segundos
duracion_maxima = 18

# Carga el video
clip = mp.VideoFileClip(video_path)

# Recorta el video a 20 segundos si es más largo
if clip.duration > duracion_maxima:
    clip = clip.subclip(0, duracion_maxima)

# Cambia el aspecto del video a 16:9
clip_resized = clip.resize((640, 360))

# Carga los frames inicial y final
frame_logo = mp.ImageClip(frame_imagen_path).resize(width=640, height=360).set_duration(1)

# Combina el frame inicial, el video y el frame final
video_modificado = mp.concatenate_videoclips([
    frame_logo,
    clip_resized.set_position('center'),
    frame_logo,
], method='compose',)

# Exporta el video resultante
video_modificado.write_videofile("video_modificado.mp4", fps=24)  # Puedes ajustar el fps según tu necesidad
