# Documentación: Optimización de Imágenes con Python

Este código tiene como objetivo **optimizar imágenes** en diferentes formatos, como JPEG, PNG y WEBP, para reducir su tamaño sin perder calidad visual significativa. Está diseñado para garantizar que la versión optimizada nunca sea más grande que la original y que las imágenes pequeñas (menores a 150 KB) se mantengan sin cambios.

---

## ¿Qué hace este código?

1. **Optimiza imágenes según su formato:**  
   - **JPEG, JPG y WEBP:** Se utiliza un método interno de optimización con la librería PIL (Pillow).
   - **PNG:** Intenta usar la herramienta externa `pngquant` para optimización avanzada. Si no está disponible, recurre a los métodos básicos de PIL.

2. **Valida las imágenes antes de optimizarlas:**  
   - Verifica que las imágenes sean válidas y no estén dañadas.

3. **Compara tamaños:**  
   - Si la imagen optimizada es más grande que la original, conserva la original.
   - Si la imagen es menor a 150 KB, no la optimiza para evitar cambios innecesarios.

---

## Explicación de las funciones principales

### 1. `optimize_image(input_path, output_path, quality=75)`

- **¿Qué hace?**  
  Optimiza una imagen desde una ruta de entrada (`input_path`) y guarda la versión optimizada en una ruta de salida (`output_path`). El parámetro `quality` permite ajustar el nivel de compresión (por defecto 75).

- **Cómo funciona:**  
  1. Comprueba que el archivo exista y sea válido.  
  2. Determina el formato de la imagen (JPEG, PNG, etc.).  
  3. Optimiza la imagen usando métodos específicos según su formato:
     - JPEG, JPG, WEBP: Compresión estándar con PIL.
     - PNG: Usa `pngquant` si está disponible; si no, usa PIL.  
  4. Compara el tamaño de la versión optimizada con la original. Si la optimizada es más grande, conserva la original.

- **Mensajes clave:**  
  - Muestra el tamaño de la imagen original y el formato detectado.  
  - Indica si la optimización fue exitosa o si hubo problemas.  

### 2. Lógica para imágenes pequeñas

Antes de llamar a `optimize_image`, el código verifica el tamaño del archivo:
- Si la imagen es menor a 150 KB, no se optimiza.  
- Simplemente copia la imagen original a la ruta de salida.

---

## ¿Cómo usar este código?

1. **Preparar tus imágenes:**  
   Coloca las imágenes en una carpeta, como `imagen_original/`.

2. **Configurar las rutas:**  
   Ajusta las variables `ruta_entrada` y `ruta_salida` con las ubicaciones de entrada y salida deseadas. Por ejemplo:  
   ```python
   ruta_entrada = "imagen_original/test.png"
   ruta_salida = "imagen_optimizada/test_opt.png"
   ```

3. **Ejecutar el script:**  
   Corre el código en un entorno Python con la librería Pillow instalada.  
   Si trabajas con imágenes PNG y quieres optimización avanzada, instala `pngquant` en tu sistema.

---

## Ejemplo de salida

**Caso 1: Optimización exitosa**
```
Tamaño original de la imagen: 200000 bytes
Imagen verificada correctamente. Formato: PNG
pngquant está disponible.
Optimización exitosa: ...
Imagen optimizada y guardada en imagen_optimizada/test_opt.png.
```

**Caso 2: La imagen optimizada es más grande**
```
Tamaño original de la imagen: 250000 bytes
Imagen verificada correctamente. Formato: JPEG
La imagen optimizada era más grande. Se mantuvo la original en imagen_optimizada/test_opt.png.
```

**Caso 3: La imagen es menor a 150 KB**
```
La imagen es menor a 150 KB. No se optimizará y se mantendrá la original.
```

---

## Requisitos

1. **Python 3.x** con la librería **Pillow** instalada:  
   ```bash
   pip install pillow
   ```
2. Para optimizar imágenes PNG con `pngquant`:  
   - Instala `pngquant` en tu sistema operativo.  
     En Linux:  
     ```bash
     sudo apt install pngquant
     
