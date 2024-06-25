import re
from urllib.parse import urlparse
import os
import shutil

# Función para limpiar el prefijo http:// y https:// de una URL y devolver solo el dominio
def limpiar_url(url):
    parsed_url = urlparse(url)
    dominio = parsed_url.netloc
    if dominio.startswith("www."):
        dominio = dominio[4:]  # Remover el prefijo 'www.'
    return dominio

# Verificar si el archivo listado_urls.txt existe
input_file = 'listado_urls.txt'
if not os.path.isfile(input_file):
    raise FileNotFoundError(f"No se encontró el archivo: {input_file}")

# Leer el listado de URLs desde un archivo
with open(input_file, 'r') as file:
    urls = file.readlines()

# Verificar si las URLs fueron leídas correctamente
print(f"URLs leídas: {len(urls)}")
if len(urls) > 0:
    print(f"Primera URL: {urls[0].strip()}")
    print(f"Última URL: {urls[-1].strip()}")

# Generar archivo con líneas de código antes y después de cada URL
codigo_antes_con_codigos = "/ip firewall address-list add list=bloqueo_mintic address="
codigo_despues_con_codigos = " comment=Bloqueo_Mintic_by_Oscar_Castillo"
codigo_con_delay = "/delay 1"

output_file_address_list = 'address_list.rsc'
with open(output_file_address_list, 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio_limpio = limpiar_url(url)
            file.write(f"{codigo_antes_con_codigos}{dominio_limpio}{codigo_despues_con_codigos}\n")
        
        # Agregar línea con delay cada 50 líneas
        if (i + 1) % 50 == 0:
            file.write(f"{codigo_con_delay}\n")

print(f"Archivo con URLs y códigos se ha guardado en '{output_file_address_list}'.")

# Función para dividir una URL en dominio y path
def dividir_url(url):
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        if dominio.startswith("www."):
            dominio = dominio[4:]  # Remover el prefijo 'www.'
        path = parsed_url.path
        print(f"dst-host={dominio} path={path} para URL: {url}")
        return dominio, path
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None, None

# Generar archivo con dominio y path de cada URL
codigo_antes_divididas = "/ip proxy access add action=redirect action-data=ticcol.com/internet-sano-1 "
codigo_despues_divididas = " comment=bloqueo_mintic"

output_file_access = 'acces.rsc'
with open(output_file_access, 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio, path = dividir_url(url)
            if dominio is not None:
                if path:
                    file.write(f"{codigo_antes_divididas}dst-host={dominio} path={path}{codigo_despues_divididas}\n")
                else:
                    file.write(f"{codigo_antes_divididas}dst-host={dominio}{codigo_despues_divididas}\n")
            
            # Agregar línea con delay cada 50 líneas
            if (i + 1) % 50 == 0:
                file.write(codigo_con_delay + "\n")

print(f"Archivo con dominios y paths se ha guardado en '{output_file_access}'.")

# Guardar el archivo de respaldo
backup_file = 'address_list_backup.rsc'
shutil.copy(output_file_address_list, backup_file)

print(f"Archivo '{output_file_address_list}' se ha copiado como '{backup_file}'.")
