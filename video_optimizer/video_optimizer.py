import os
import subprocess
import shutil


from googleapiclient.http import MediaFileUpload


def compress_video(service, dir_path, dowloaded_files, folder_id=None):
    """
    Comprime un video al formato AV1 utilizando FFmpeg con SVT-AV1.

    Args:
        service (conn): conexion autenticada del drive.
        dir_path (str): Ruta de la carpeta.
        download_files(dict): es un diccionario con el idownload_files (dict): Diccionario con los archivos a descargar con el id y el nombre de los archivos descargados
        folder_id (str): id de la carpeta en el drive, opcional
    Returns:
        None
    """

    # Crear carpetas
    os.makedirs(dir_path, exist_ok=True)
    os.makedirs(f"opt_{dir_path}", exist_ok=True)

    for file_name in os.listdir(dir_path):
        
        # Rutas de los archivos
        input_file = os.path.join(dir_path, file_name)
        output_file = os.path.join(f"opt_{dir_path}/", file_name)
        
 
        # Verifica que FFmpeg esté disponible
        if not shutil.which("ffmpeg"):
            raise EnvironmentError("FFmpeg no está instalado o no está en PATH.")
        
        # Verificar el formato del archivo
        file_ext = os.path.splitext(input_file)[1].lower()
        codec_video = "libx265"
        preset = "medium"
        crf = "28"
        codec_audio = "aac"

        # Establecer codec si es webm
        if file_ext == ".webm":
            codec_audio = "libopus"
        elif file_ext in [".mpg", ".mpeg", ".mpeg2"]:
            codec_audio = "mp2"

        # Comando de compresión
        cmd = [
            "ffmpeg",
            "-i", input_file,          # Archivo de entrada
            "-c:v", codec_video,       # Codificador de video
            "-crf", crf,               # Calidad (CRF)
            "-preset", preset,         # Velocidad de compresión
            "-c:a", codec_audio,       # Codificador de audio
            "-b:a", "128k",            # Tasa de bits del audio
            "-strict", "-2",           # Permitir configuraciones experimentales
            "-ignore_unknown",         # Ignorar errores de códec desconocidos
            output_file                # Archivo de salida
        ]

        # Ejecuta el comando
        try:
            print(f"Procesando {input_file} con CRF={crf} y velocidad={preset}...")
            result = subprocess.run(cmd, check=True)
            print(f"Compresión completada. Archivo guardado en: {output_file}")
            print(result)
            
            #  Guardar archivos en carpeta del drive   
            file_metadata = {'name': os.path.basename(f"{output_file}")}
            if folder_id:
                file_metadata['parents'] = [folder_id]   
   
             # Eliminar archivos originales del Drive
            for file_id_ in dowloaded_files:
                try:
                    service.files().delete(fileId=file_id_).execute()
                    print(f"Archivo con ID {file_id_} eliminado exitosamente.")
                except Exception as e:
                    print(f"No se pudo eliminar el archivo con ID {file_id_}: {e}")
            
            # Carga Archivos al drive
            media = MediaFileUpload(output_file, mimetype='video/mp4', resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()          

        

            print(f"Archivo subido. ID: {file.get('id')}")
        except subprocess.CalledProcessError as e:
            print(f"Error durante la compresión de {input_file}: {e.stderr.decode()}")
        except Exception as e:
            print(f"Ocurrió un error inesperado con {input_file}: {e}")
     # Eliminar del drive archivos anteriores
    shutil.rmtree(dir_path, ignore_errors=True)
    if os.path.exists(f"opt_{dir_path}"):  # Verificamos si fue inicializado
        shutil.rmtree(f"opt_{dir_path}", ignore_errors=True)
        opt_dir_path = f"opt_{dir_path}" if f"opt_{dir_path}" else "N/A"
        print(f"Carpetas locales eliminadas: {dir_path} y {opt_dir_path}")
 
            