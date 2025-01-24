# Documentación: Detección de Archivos Duplicados

Este programa está diseñado para detectar archivos duplicados en un directorio basándose en sus contenidos. La detección se realiza generando un "hash" único para cada archivo y comparando estos valores. A continuación, se explican las dos funciones principales del programa:

---

## **1. Generar el Hash de un Archivo**

La función `generate_file_hash` se utiliza para crear un identificador único (hash) para cada archivo.

### **Qué hace:**
- Lee el archivo en bloques pequeños para evitar cargarlo completamente en la memoria.
- Genera un hash utilizando el algoritmo SHA-256.
- Devuelve el hash en formato hexadecimal.

### **Por qué es útil:**
- Asegura que incluso si los nombres de archivo son diferentes, los archivos con el mismo contenido serán detectados como duplicados.

---

## **2. Detectar Archivos Duplicados**

La función `detect_duplicates` identifica archivos con contenido idéntico.

### **Qué hace:**
- Genera el hash de cada archivo en la lista de archivos proporcionada.
- Compara los hashes para encontrar duplicados.
- Devuelve una lista de archivos duplicados.

### **Cómo funciona:**
1. Recorre todas las rutas de los archivos.
2. Calcula el hash de cada archivo utilizando `generate_file_hash`.
3. Si el hash ya existe, el archivo se agrega a la lista de duplicados.
4. Si no, almacena el hash como referencia.

---

## **Instrucciones para Usar el Programa**

1. **Organizar los Archivos:**
   - Coloca los archivos que deseas analizar en un directorio llamado `images`.

2. **Ejecutar el Script:**
   - El script recorre el directorio `images`, analiza los archivos y detecta los duplicados.

3. **Salida del Programa:**
   - Imprime en la consola las rutas de los archivos duplicados.

---

## **Ejemplo de Uso**

1. **Estructura del Directorio:**
   ```
   images/
   ├── foto1.jpg
   ├── foto2.jpg
   ├── duplicado_foto1.jpg
   ```

2. **Resultados del Programa:**
   ```
   images/duplicado_foto1.jpg
   ```

El programa detectará `duplicado_foto1.jpg` como duplicado de `foto1.jpg`.

--- 

## **Nota Técnica**

- **Algoritmo SHA-256:**
  - Es un método seguro para identificar contenido único, independientemente del nombre o la extensión del archivo.
- **Rendimiento:**
  - El programa está diseñado para procesar grandes conjuntos de archivos sin consumir demasiada memoria gracias a la lectura en bloques.

¡Este programa es ideal para limpiar tus directorios y eliminar archivos redundantes!
