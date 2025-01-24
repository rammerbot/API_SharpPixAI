from PIL import Image, ImageFile
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

def optimize_image(service, dir_path, downloaded_files):
    """
    Optimiza una imagen si el formato original lo permite.
    Si la imagen optimizada es más grande que la original, se conserva la original.
    """
    # Crear lista para iterar carpeta
    file_list = os.listdir(dir_path)
    # Crear carpeta para guardar archivos
    os.makedirs(f"opt_{dir_path}", exist_ok=True)

    # Iterar archivos dentro de la carpeta para optimizar
    for input_path in file_list:
        output_path = os.path.join(f"opt_{dir_path}/", input_path)
        original_size = os.path.getsize(input_path)
        if original_size < 150000:  # 150 KB
            print(f"La imagen es menor a 150 KB. No se optimizará y se mantendrá la original.")
            os.replace(input_path, output_path)
        else:

            original_size = os.path.getsize(input_path)
            print(f"Tamaño original de la imagen: {original_size} bytes")

            # Verificar que la imagen sea válida
            try:
                with Image.open(input_path) as img:
                    img.verify()  
                    format_original = img.format
                    print(f"Imagen verificada correctamente. Formato: {format_original}")
            except (IOError, SyntaxError) as e:
                print(f"Error al abrir la imagen: {e}")
                return

            optimized = False

            try:
                with Image.open(input_path) as img:
                    if format_original in ["JPEG", "JPG", "WEBP", "PNG"]:
                        img.save(output_path, format=format_original, optimize=True)
                        optimized = True
                    else:
                        print(f"Formato '{format_original}' no soporta optimización avanzada. Se copiará sin cambios.")
                        img.save(output_path, format=format_original)
                        optimized = True
            except Exception as e:
                print(f"Error durante la optimización: {e}")
                return

            # Comparar tamaños y conservar la original si es más pequeña
            if optimized and os.path.exists(output_path):
                optimized_size = os.path.getsize(output_path)
                if optimized_size >= original_size:
                    os.replace(input_path, output_path)  # Reemplazar con la original
                    print(f"La imagen optimizada era más grande. Se mantuvo la original en {output_path}.")
                else:
                    print(f"Imagen optimizada y guardada en {output_path}.")
            else:
                print("No se pudo optimizar la imagen.")
    
        


    