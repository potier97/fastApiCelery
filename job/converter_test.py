from sqlalchemy import create_engine, text, update
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()


def conectar_bd():
    # motor = os.getenv("DB_URL", "postgresql://fpv_user_dev:pfv_user_pwd@localhost:5080/fpv_db_dev")
    # motor = "postgresql://fpv_user_dev:pfv_user_pwd@localhost:5432/fpv_db_dev"
    motor = os.getenv("DB_URL", "postgresql://fpv_user_dev:pfv_user_pwd@postgres:5432/fpv_db_dev")
    print("motor: ", motor)
    # motor = os.getenv("MOTOR_CONEXION", "postgresql://fpv_user_dev:pfv_user_pwd@postgres:5432/fpv_db_dev")
    # motor = "postgresql://fpv_user_dev:pfv_user_pwd@postgres:5432/fpv_db_dev"
    try:
        engine = create_engine(motor)
        print("Conexión exitosa a la base de datos PostgreSQL.")
        return engine
    except Exception as e:
        print("Error al conectarse a la base de datos PostgreSQL:", e)
        return None



def ejecutar_script_sh(id):
    engine = conectar_bd()
    if engine is not None:
        # Realizar consultas, operaciones, etc. aquí
        connection = engine.connect()
        stmt = text("SELECT * FROM tasks WHERE id = :id AND status='uploaded'").bindparams(id=id)
        result = connection.execute(stmt)
        row = result.first()

        if row is not None: 
            original_file_name = row[1]
            video_url = row[4] 
            processed_url = row[5]
            print("video_url: " + video_url)
            print("original_file_name: " + original_file_name)
            print("processed_url: " + processed_url)

            # Ejemplo de uso
            public_folder = os.getenv("PUBLIC_DIR", "http://localhost:8080")
            # video_url = "../public/uploaded/5a0f3089-bcc0-4d13-a922-3142feddf13d_editar-tag-sin-titulo.mp4"
            video_url_relative  = video_url.replace(public_folder, "").replace("\\", "/")
            processed_url_relative  = processed_url.replace(public_folder, "").replace("\\", "/")

            # Construir la ruta local de los archivos
            video_url_local = "." + os.path.join(os.path.dirname(os.path.realpath(__file__)), video_url_relative)
            processed_url_local = "." + os.path.join(os.path.dirname(os.path.realpath(__file__)), processed_url_relative)

            print("video_url local: " + video_url_local)
            print("processed_url local: " + processed_url_local)


            ruta_script_sh = os.path.join(os.path.dirname(os.path.realpath(__file__)), "process.sh")
            video_logo = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imagen_video.mp4")
            comando = ["sh", ruta_script_sh, video_url_local, processed_url_local, video_logo]
            subprocess.run(comando, check=True)

            update_stmt = text("UPDATE tasks SET status='processed' WHERE id = :id").bindparams(id=id)
            connection.execute(update_stmt)
            connection.commit()


        connection.close()
        engine.dispose()
    


# ejecutar_script_sh(video_entrada, video_salida)
# ejecutar_script_sh(2)
