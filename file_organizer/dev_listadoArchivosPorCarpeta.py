from authentication import authenticate


def list_files_by_folder(service, folder_ids):
    """
    Lista los archivos en carpetas específicas de Google Drive.
    
    :param service: Servicio autenticado de Google Drive.
    :param folder_ids: Diccionario con nombres de carpetas como claves y sus IDs como valores.
    :return: Diccionario con los archivos listados por carpeta.
    """
    all_files = {}
    for folder_name, folder_id in folder_ids.items():
        print(f"Listando archivos en la carpeta '{folder_name}':")
        query = f"'{folder_id}' in parents"
        results = service.files().list(
            q=query, pageSize=1000, fields="files(id, name)"
        ).execute()
        items = results.get('files', [])
        
        if not items:
            print(f"No se encontraron archivos en la carpeta '{folder_name}'.")
        else:
            for item in items:
                print(f"{item['name']} ({item['id']})")
        
        all_files[folder_name] = items  # Guardar los archivos por carpeta
    return all_files


# IDs de las carpetas
folder_ids = {
    "audio": "1dJmaRgeEy9THWYiEM8q-Q76HXFym02a7",
    "texto": "1qYuuyU0IuhmgG65MHYbUVJGgHSyrqLhL",
    "video": "1wx3Aw3PYchC1_vk6f2nmz9YDgwdAoOpN",
    "imagen": "1fSiZg1ATlx7IU3MVsasbKjg4mEOJcAaX"
}

# Importar la función de autenticación desde otro archivo


# Autenticar y obtener el servicio
service = authenticate()

# Listar los archivos por carpetas
all_files = list_files_by_folder(service, folder_ids)

# Imprimir resultados finales
print("\nArchivos listados por carpeta:")
for folder, files in all_files.items():
    print(f"\nCarpeta: {folder}")
    for file in files:
        print(f" - {file['name']} ({file['id']})")
