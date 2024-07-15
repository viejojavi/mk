import re
from urllib.parse import urlparse
import os
import shutil

# Función para limpiar el prefijo http:// y https:// de una URL y devolver solo el dominio
def limpiar_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Añadir http:// si no está presente
    parsed_url = urlparse(url)
    dominio = parsed_url.netloc
    return dominio

# Leer el listado de URLs desde un archivo
with open('listado_urls.txt', 'r') as file:
    urls = file.readlines()

# Verificar si las URLs fueron leídas correctamente
print(f"URLs leídas: {len(urls)}")
if len(urls) > 0:
    print(f"Primera URL: {urls[0].strip()}")
    print(f"Última URL: {urls[-1].strip()}")

# Generar archivo con líneas de código antes y después de cada URL
codigo_antes_con_codigos = "/ip/firewall/address-list/add list=bloqueo_mintic address="
codigo_despues_con_codigos = " comment=Bloqueo_Mintic_by_Oscar_Castillo"
codigo_con_delay = "delay 1"

# Crear el directorio si no existe
os.makedirs('bloqueo_mintic', exist_ok=True)

listado_completo_path = 'bloqueo_mintic/listado_completo.rsc'
address_list_path = 'bloqueo_mintic/address_list.rsc'
dominios_unicos = set()  # Usar un conjunto para almacenar dominios únicos

with open(listado_completo_path, 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio_limpio = limpiar_url(url)
            if dominio_limpio not in dominios_unicos:  # Verificar si el dominio ya existe en el conjunto
                dominios_unicos.add(dominio_limpio)
                file.write(f"{codigo_antes_con_codigos}{dominio_limpio}{codigo_despues_con_codigos}\n")
            
                # Agregar línea con delay cada 50 líneas
                if (i + 1) % 50 == 0:
                    file.write(codigo_con_delay + "\n")

print(f"Archivo con URLs y códigos se ha guardado en '{listado_completo_path}'.")

# Función para dividir una URL en dominio y path
def dividir_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Añadir http:// si no está presente
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        path = parsed_url.path
        print(f"dst-host={dominio} path={path} para URL: {url}")
        return dominio, path
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None, None

# Generar archivo con dominio y path de cada URL
codigo_antes_divididas = "/ip/proxy/access/add action=redirect action-data=ticcol.com/internet-sano-1 "
codigo_despues_divididas = " comment=bloqueo_mintic"

access_path = 'bloqueo_mintic/access.rsc'
with open(access_path, 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio, path = dividir_url(url)
            if dominio is not None:
                if path and path != "/":
                    file.write(f"{codigo_antes_divididas}dst-host={dominio} path={path}{codigo_despues_divididas}\n")
                else:
                    file.write(f"{codigo_antes_divididas}dst-host={dominio}{codigo_despues_divididas}\n")
            
            # Agregar línea con delay cada 50 líneas
            if (i + 1) % 50 == 0:
                file.write(codigo_con_delay + "\n")

print(f"Archivo con dominios y paths se ha guardado en '{access_path}'.")

# Guardar el archivo con el nuevo nombre
shutil.copy(listado_completo_path, 'listado_urls.rsc')
print("Archivo 'listado_completo.rsc' se ha copiado como 'listado_urls.rsc'.")
