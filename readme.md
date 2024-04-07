# Proyecto FastAPI - README


Este proyecto utiliza FastAPI como framework para crear una API web. A continuación se detallan los pasos necesarios para configurar el entorno de desarrollo, instalar las dependencias, manejar las variables de entorno y ejecutar el servidor FastAPI.

### Configuración del Entorno de Desarrollo

Clona este repositorio en tu máquina local: 


```bash
git clone <URL del repositorio>
cd <nombre del directorio>
```

Crea un entorno virtual para el proyecto:

```bash
python -m venv venv
```

Activa el entorno virtual:

```bash
# En Linux/MacOS
source venv/bin/activate
```
    
```bash
# En Windows
.\venv\Scripts\activate
```

### Instalación de Dependencias

Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

Las dependencias necesarias para este proyecto son:
- fastapi
- uvicorn
- sqlalchemy
- asyncpg
- pyjwt
- redis

Las versiones pueden variar dependiendo del sistema operativo y/o la versión de Python que estés utilizando, etc.

### Manejo de Variables de Entorno

1. Crea un archivo .env en el directorio raíz del proyecto.
2. Define las variables de entorno necesarias en el archivo .env, como la cadena de conexión a la base de datos y la configuración de JWT.


Ejemplo de archivo .env:

```bash
DATABASE_URL=postgresql://usuario:contraseña@localhost:8050/nombre_bd
SECRET_KEY=supersecreta
DEBUG=True
```

Si la aplicación está desplegada en un entorno de producción, asegúrate de cambiar el valor de DEBUG a False.

 > Asegurese de que la url de la base de datos sea correcta, en este caso  en el archivo docker-compose.yml se define el puerto 8050 para la base de datos, por lo que la url de la base de datos debe ser `postgresql://usuario:contraseña@localhost:8050/nombre_bd`.

### Iniciar el Servidor FastAPI

Para iniciar el servidor FastAPI, ejecuta el siguiente comando:

```bash
uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8080
```

### Documentación de la API - Swagger

Accede a la API en http://localhost:8080 en tu navegador o con herramientas como Postman o curl.


### Ejecutar Docker

Para ejecutar el proyecto con Docker, sigue los siguientes pasos:

1. Construye la imagen de Docker:

```bash
docker build -t fastapi-app .
```

2. Ejecuta el contenedor de Docker:

```bash
docker run -e DB_URL=postgresql://fpv_user_dev:pfv_user_pwd@localhost:5080/fpv_db_dev -e SECRET_KEY=supreSecretKey123 -e DEBUG=False -p 3000:8080  fastapi-app
```
 
 > Ejecutar solo este contenedor genera un error, ya que este proyecto necesita una base de datos PostgreSQL, además de un servidor de redis para la cola de tareas y el servicio del proceso batch, por lo que se recomienda ejecutar el archivo docker-compose.yml.

 > Si todo sale bien, y ejecuto el mismo comando anterior, deberia ver este error en la consola: `ERROR:    Application startup failed. Exiting.`, indicandole que no se ha poddo contectar con la base de datos, para esto necesitamos ejecutar el archivo docker-compose.yml. ya que nos permite tener una red de contenedores y servicios que se comunican entre si.


### Docker Compose del Worker

Para ejecutar el servicio de Celery, sigue los siguientes pasos:

1. Ejecuta el siguiente comando para iniciar el servicio de redis:
```bash	
docker-compose up -d redis
```

2. Ejecuta el siguiente comando para construir la imagen de Docker del servicio de Celery:

```bash
docker build -t worker-api -f dockerfileWorker .     
```

3. Ejecuta el siguiente comando para iniciar el servicio de Celery:

```bash
docker-compose up -d workertres
```

### Ingresar a un contenedor por SH

Para ingresar a un contenedor por SH, sigue los siguientes pasos:

1. Ejecuta el siguiente comando para listar los contenedores que estan corriendo:

```bash
docker ps
```

2. Ejecuta el siguiente comando para ingresar a un contenedor por SH:
```bash
docker exec -it <id_del_contenedor> bash     
```	

### Ejecutar Docker Compose

  > Importante: Asegúrate de tener las siguientes carpetas en el directorio raíz del proyecto: `pgadmin-data`, `redis_data`, `pgadmin_data`. Estas carpetas son necesarias para almacenar los datos `Volumenes` de PostgreSQL, Redis y PgAdmin, respectivamente que son manejados por docker para persistir la información.


Para ejecutar el proyecto con Docker Compose, sigue los siguientes pasos:

1. Construye las imágenes de Docker:

```bash
docker-compose build
```

2. Ejecuta los contenedores de Docker en segundo plano:

```bash
docker-compose up  -d
```

3. Detener los contenedores de Docker:

```bash
docker-compose down
```

4. Eliminal los contenedores de Docker:

```bash
docker-compose down -v
```

  > Nota: Si necesita limpiar el proyecto con los datos que se generan en los volúmenes, elimine las carpetas mencionadas anteriormente y ejecute el comando `docker-compose down -v` para eliminar los contenedores y los volúmenes asociados.

  > Si solo necesita levantar un servicio, y está seguro de que los otros servicios no están corriendo, puede ejecutar el siguiente comando: `docker-compose up <nombre del servicio>`

## Celery

Para ejecutar el servicio de Celery, sigue los siguientes pasos:

1. Ejecuta el siguiente comando para iniciar el servicio de redis:

```bash
docker-compose up -d redis
```

2. Ejecuta el siguiente comando para iniciar el servicio de Celery:

```bash
celery -A job.celery_app worker -1 info -P gevent
```

 > El  registro de logs se establece a `info`, pero puede cambiarlo a `debug` para obtener más información. Ademas para poder imprimir los logs generados por `loger` o `print` es necesario agregar el parametro `-P gevent` para que los logs se impriman en la consola. Tenga en cuenta que es necesario instalar la libreria `gevent` para poder utilizar este parametro: `pip install gevent`.

 3. Ejecuta el siguiente comando para iniciar el servicio de Celery que ejecuta los procesos batch:

```bash
celery -A job.celery_app beat --loglevel INFO
```
 
 > En el archivo `job.beat_conf` se definen las tareas que se ejecutan en el servicio de Celery, para este proceso se define un proceso batch que se ejecuta cada 5 minutos, yhace un proceso de conversión de conversión de archivos ubicados en el proyecto, modifique el valor de la variable `schedule` en el archivo `job.beat_conf`.


# ffmpeg

ffmpeg es una herramienta de línea de comandos que se utiliza para convertir archivos de audio y video de un formato a otro. En este proyecto se utiliza para convertir archivos de audio de formato mp3 a wav.

 - Convertir una imagen a video, ejecte el siguiente comando:

```bash
ffmpeg -loop 1 -i imagen.png -vf "scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2" -t 1 imagen_video.mp4
``` 

> En este comando se convierte una imagen a un video, el parametro `-loop 1` indica que la imagen se repite una vez, el parametro `-i imagen.png` indica la imagen que se va a convertir, el parametro `-vf "scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2"` indica el tamaño del video, el parametro `-t 1` indica la duración del video, y el parametro `imagen_video.mp4` indica el nombre del video que se va a generar.

 - Recortar y redimensionar un video, ejecte el siguiente comando:

```bash
ffmpeg -i input_video.mp4 -ss 0 -t 18 -vf "scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2" output_video.mp4
```	

> En este comando se recorta y redimensiona un video, el parametro `-i input_video.mp4` indica el video que se va a convertir, el parametro `-ss 0` indica el tiempo de inicio del video, el parametro `-t 18` indica la duración del video, el parametro `-vf "scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2"` indica el tamaño del video, y el parametro `output_video.mp4` indica el nombre del video que se va a generar.

  - Concatenar varios videos, ejecte el siguiente comando:

```bash
ffmpeg -i imagen_video.mp4 -i output_video.mp4 -i imagen_video.mp4  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]" -map "[outv]" output.mp4 
```

> En este comando se concatenan varios videos, el parametro `-i imagen_video.mp4 -i output_video.mp4 -i imagen_video.mp4` indica los videos que se van a concatenar, el parametro `-filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]"` indica la concatenación de los videos, y el parametro `-map "[outv]" output.mp4` indica el nombre del video que se va a generar.