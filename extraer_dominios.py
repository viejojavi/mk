import re
from urllib.parse import urlparse

# Función para limpiar el prefijo http:// y https:// de una URL
def limpiar_url(url):
    url = re.sub(r'^https?://', '', url)  # Eliminar http:// o https://
    return url

# Leer el listado de URLs desde un archivo
with open('listado_urls.txt', 'r') as file:
    urls = file.readlines()

# Verificar si las URLs fueron leídas correctamente
print(f"URLs leídas: {len(urls)}")
if len(urls) > 0:
    print(f"Primera URL: {urls[0].strip()}")
    print(f"Última URL: {urls[-1].strip()}")

# Generar archivo con líneas de código antes y después de cada URL
codigo_antes_con_codigos = "add list=bloqueo_mintic address="
codigo_despues_con_codigos = " comment=Bloqueo_Mintic_by_Oscar_Castillo"
codigo_con_delay = "delay 1"

with open('urls_con_codigos.txt', 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            url_limpia = limpiar_url(url)
            file.write(f"{codigo_antes_con_codigos}{url_limpia}{codigo_despues_con_codigos}\n")
            
            # Agregar línea con delay cada 50 líneas
            if (i + 1) % 50 == 0:
                file.write(codigo_con_delay + "\n")

print("Archivo con URLs y códigos se ha guardado en 'urls_con_codigos.txt'.")

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
codigo_antes_divididas = "/ip/proxy/access/add action=redirect action-data=ticcol.com/internet-sano-1 "
codigo_despues_divididas = " comment=bloqueo_mintic"

with open('urls_divididas.txt', 'w') as file:
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

print("Archivo con dominios y paths se ha guardado en 'urls_divididas.txt'.")

# Guardar el archivo con el nuevo nombre
import shutil
shutil.copy('urls_con_codigos.txt', 'listado_urls.rsc')

print("Archivo 'urls_con_codigos.txt' se ha copiado como 'listado_urls.rsc'.")

import os
from github import Github

# Nombre del archivo que queremos actualizar en el repositorio
archivo_actualizar = 'listado_urls.rsc'
# Ruta local del archivo que queremos actualizar en el repositorio
archivo_local = 'urls_con_codigos.txt'
# Ruta de la subcarpeta donde se encuentra listado_urls.rsc en el repositorio
subcarpeta = 'bloqueo_mintic'

# Obtener el token de autenticación de GitHub desde las secrets
token = os.getenv('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')

# Crear una instancia de la clase Github usando el token
github = Github(token)

# Obtener el repositorio
repo = github.get_repo('viejojavi/mk')  # Reemplaza 'usuario/repo' con tu nombre de usuario y nombre de repositorio

# Leer el contenido del archivo local
with open(archivo_local, 'r', encoding='utf-8') as file:
    contenido = file.read()

# Actualizar el contenido del archivo en el repositorio
try:
    # Obtener el contenido del archivo en la subcarpeta del repositorio
    ruta_archivo = f"{subcarpeta}/{archivo_actualizar}"
    archivo = repo.get_contents(ruta_archivo)
    
    # Actualizar el archivo con el contenido nuevo
    repo.update_file(archivo.path, f"Actualización de {archivo_actualizar}", contenido, archivo.sha)
    print(f"Archivo {archivo_actualizar} actualizado correctamente en la subcarpeta {subcarpeta}.")
except Exception as e:
    print(f"Error al actualizar el archivo {archivo_actualizar}: {e}")
