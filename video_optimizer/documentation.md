# Compresión de Videos con FFmpeg

Este script permite comprimir videos utilizando el códec AV1 a través de FFmpeg, con soporte para diferentes formatos de entrada y salida. El objetivo es reducir el tamaño de los videos manteniendo una calidad aceptable.

## Requisitos Previos

1. **FFmpeg**:
   - Asegúrate de que FFmpeg esté instalado y disponible en el PATH de tu sistema.
   - Puedes verificar si está instalado ejecutando `ffmpeg -version` en tu terminal.

2. **Estructura de Carpetas**:
   - Coloca los videos originales en la carpeta especificada en `input_path`.
   - La carpeta de salida definida en `output_path` debe existir antes de ejecutar el script.

# Uso del script

input_path = "C:videos_originales"   # Ruta del video original
output_path = "videos_comprimidos"  # Ruta del video comprimido

# Iterar sobre los archivos de entrada y comprimirlos
for i in os.listdir(input_path):
    compress_video(os.path.join(input_path, i), os.path.join(output_path, i))
```

## Explicación del Código

1. **Funciones Principales**:
   - `compress_video`: Realiza la compresión del video especificado.

2. **Selección de Códec de Audio**:
   - Dependiendo de la extensión del archivo, se ajusta el códec de audio.
     - `.webm`: Usa `libopus`.
     - `.mpg`, `.mpeg`, `.mpeg2`: Usa `mp2`.

3. **Comando de FFmpeg**:
   - Configuración básica:
     - `-c:v`: Codificador de video (`libx265`).
     - `-crf`: Control de calidad (28 por defecto).
     - `-preset`: Velocidad de compresión (`medium`).
     - `-c:a`: Codificador de audio.
     - `-b:a`: Tasa de bits del audio (128 kbps).

4. **Iteración sobre Archivos**:
   - Se recorren los archivos en `input_path` y se procesan uno por uno.

## Notas Importantes

- **Tamaño y Calidad**:
  - `crf` controla la calidad del video. Valores más bajos ofrecen mejor calidad pero archivos más grandes.

- **Errores Comunes**:
  - Si FFmpeg no está disponible, el script detendrá su ejecución.

## Ejemplo de Ejecución

Supongamos que tenemos los siguientes archivos en `C:videos_originales`:

- `video1.mp4`
- `video2.webm`

Después de ejecutar el script, los archivos comprimidos se guardarán en la carpeta `videos_comprimidos`.
