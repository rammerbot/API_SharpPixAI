import os
import subprocess
import shutil

from download_files import download_media_item

def compress_video(request, callback):
    """
    Comprime un video al formato AV1 utilizando FFmpeg con SVT-AV1.

    Args:
        input_file (str): Ruta del archivo de entrada.
        output_file (str): Ruta del archivo comprimido.

    Returns:
        None
    """

    # Descargar los archivos de google photos
    path_dir = download_media_item(request=request, callback=callback)
    input_dir = os.listdir(path_dir)
    
    for input_file in input_dir:
        input_file = os.path.join(path_dir, input_file)
        # Verifica que FFmpeg esté disponible
        if not shutil.which("ffmpeg"):
            raise EnvironmentError("FFmpeg no está instalado o no está en PATH.")

        # Verificar el formato del archivo
        file_ext =  os.path.splitext(input_file)[1].lower()
        codec_video = "libx265"
        preset = "medium"
        crf = "28"
        codec_audio = "aac"

        # Crear rutas para carpeta de salida y ruta del archivo de salida
        output_dir = os.makedirs(input_file + 'opt', exist_ok=True)
        output_file = os.path.dirname(output_dir + 'opt')

        # Establecer codec si es webm
        if file_ext == ".webm":
            codec_audio = "libopus"
        elif file_ext == ".mpg" or file_ext == ".mpeg" or file_ext == ".mpeg2":
            codec_audio = "mp2"

        # Comando de compresión
        cmd = [
            "ffmpeg",
            "-i", input_file,          # Archivo de entrada
            "-c:v", codec_video,       # Codificador de video
            "-crf", crf,         # Calidad (CRF)
            "-preset", preset,   # Velocidad de compresión
            "-c:a", codec_audio,       # Codificador de audio
            "-b:a", "128k",            # Tasa de bits del audio
            "-strict", "-2",           # Permitir configuraciones experimentales
            "-ignore_unknown",         # Ignorar errores de códec desconocidos
            output_file                # Archivo de salida
        ]
        # Ejecuta el comando
        try:
            print(f"Procesando {input_file} con CRF={28} y velocidad={preset}...")
            result = subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
            print(f"Compresión completada. Archivo guardado en: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error durante la compresión de {input_file}: {e.stderr.decode()}")
        except Exception as e:
            print(f"Ocurrió un error inesperado con {input_file}: {e}")
