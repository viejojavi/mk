import re
from urllib.parse import urlparse
import os

# Función para limpiar el prefijo http:// y https:// de una URL
def limpiar_url(url):
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

# Crear la carpeta bloqueo_mintic si no existe
carpeta_bloqueo = 'bloqueo_mintic'
if not os.path.exists(carpeta_bloqueo):
    os.makedirs(carpeta_bloqueo)

# Ruta completa del archivo address_list.rsc
address_list_path = os.path.join(carpeta_bloqueo, 'address_list.rsc')

with open(address_list_path, 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio_limpio = limpiar_url(url)
            file.write(f"{codigo_antes_con_codigos}{dominio_limpio}{codigo_despues_con_codigos}\n")
        
        # Agregar línea con delay cada 50 líneas
        if (i + 1) % 50 == 0:
            file.write(f"{codigo_con_delay}\n")

print(f"Archivo con URLs y códigos se ha guardado en '{address_list_path}'.")

# Función para dividir una URL en dominio y path
def dividir_url(url):
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        path = parsed_url.path
        # Verificar si el path termina solo con '/'
        if path == '/':
            path = ''  # Si es así, dejar el path vacío
        print(f"dst-host={dominio} path={path} para URL: {url}")
        return dominio, path
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None, None

# Generar archivo con dominio y path de cada URL
codigo_antes_divididas = "/ip/proxy/access/add action=redirect action-data=ticcol.com/internet-sano-1 "
codigo_despues_divididas = " comment=bloqueo_mintic"

# Ruta completa del archivo acces.rsc
acces_path = os.path.join(carpeta_bloqueo, 'acces.rsc')

with open(acces_path, 'w') as file:
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
                file.write(f"{codigo_con_delay}\n")

print(f"Archivo con dominios y paths se ha guardado en '{acces_path}'.")

# Copiar el archivo address_list.rsc como listado_urls.rsc en la misma carpeta
listado_urls_path = os.path.join(carpeta_bloqueo, 'listado_urls.rsc')
shutil.copy(address_list_path, listado_urls_path)
print(f"Archivo '{address_list_path}' se ha copiado como '{listado_urls_path}'.")
