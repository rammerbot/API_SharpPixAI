import os
import subprocess
import shutil

from download_files import download_media_item

def compress_video(request, callback):
    """
    Comprime videos al formato AV1 utilizando FFmpeg con SVT-AV1.
    """
    try:
        # Descargar los archivos de Google Photos
        path_dir = download_media_item(request=request, callback=callback)
        
        # Crear carpeta de salida para archivos comprimidos
        output_path = os.path.join(path_dir, 'opt')
        os.makedirs(output_path, exist_ok=True)

        # Listar archivos en el directorio de descargas
        input_files = os.listdir(path_dir)

        for filename in input_files:
            input_file = os.path.join(path_dir, filename)
            
            # Verificar si es un archivo (no un directorio)
            if not os.path.isfile(input_file):
                print(f"Ignorando directorio: {input_file}")
                continue

            # Verificar el formato del archivo
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in (".mp4", ".webm", ".mkv", ".avi", ".mov"):
                print(f"Ignorando archivo no compatible: {filename}")
                continue

            # Configuración de codecs según extensión
            codec_video = "libx265"
            preset = "medium"
            crf = "28"
            codec_audio = "aac"

            # Nombre del archivo de salida
            output_filename = f"compressed_{filename}"
            output_file = os.path.join(output_path, output_filename)

            # Ajustar codec de audio para formatos específicos
            if file_ext == ".webm":
                codec_audio = "libopus"
            elif file_ext in (".mpg", ".mpeg", ".mpeg2"):
                codec_audio = "mp2"

            # Comando de compresión
            cmd = [
                "ffmpeg",
                "-i", input_file,          # Archivo de entrada
                "-c:v", codec_video,       # Codificador de video
                "-crf", crf,              # Calidad (CRF)
                "-preset", preset,        # Velocidad de compresión
                "-c:a", codec_audio,      # Codificador de audio
                "-b:a", "128k",            # Tasa de bits del audio
                "-strict", "-2",           # Permitir configuraciones experimentales
                "-ignore_unknown",         # Ignorar errores de códec desconocidos
                output_file                # Archivo de salida
            ]

            # Ejecutar el comando
            try:
                print(f"Procesando {filename} con CRF={crf} y velocidad={preset}...")
                subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
                print(f"Compresión completada. Archivo guardado en: {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error durante la compresión de {filename}: {e.stderr.decode()}")
            except Exception as e:
                print(f"Ocurrió un error inesperado con {filename}: {e}")

        # Lista de archivos comprimidos
        lista_final = os.listdir(output_path)
        print(f'-----------------------------------{lista_final}--------------------------------')

        # Eliminar la carpeta original de descargas
        print(f"Eliminando carpeta original: {path_dir}")
        shutil.rmtree(path_dir)

        # Eliminar la carpeta de archivos comprimidos
        print(f"Eliminando carpeta de archivos comprimidos: {output_path}")
        shutil.rmtree(output_path)

        return {"message": "proceso finalizado"}

    except Exception as e:
        print(f"Error general en la función compress_video: {e}")
        raise