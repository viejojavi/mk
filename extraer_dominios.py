import re
import idna
from urllib.parse import urlparse

# Función para limpiar el prefijo http:// y https:// de una URL y devolver solo el dominio
def limpiar_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Añadir http:// si no está presente
    parsed_url = urlparse(url)
    dominio = parsed_url.netloc
    return dominio

# Función para convertir dominios Unicode a ASCII
def convertir_a_ascii(dominio):
    try:
        ascii_dominio = idna.encode(dominio).decode('ascii')
        return ascii_dominio
    except idna.IDNAError:
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

listado_completo_path = 'listado_completo.rsc'
address_list_path = 'address_list.rsc'
dominios_unicos = set()  # Usar un conjunto para almacenar dominios únicos

# Crear el archivo listado_completo.rsc con todas las URLs
with open(listado_completo_path, 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio_limpio = limpiar_url(url)
            ascii_dominio = convertir_a_ascii(dominio_limpio)
            file.write(f"{codigo_antes_con_codigos}{ascii_dominio}{codigo_despues_con_codigos}\n")
            
            # Agregar línea con delay cada 50 líneas
            if (i + 1) % 50 == 0:
                file.write(codigo_con_delay + "\n")

print(f"Archivo con URLs y códigos se ha guardado en '{listado_completo_path}'.")

# Filtrar dominios únicos y escribir en un nuevo archivo address_list.rsc
with open(address_list_path, 'w') as file:
    with open(listado_completo_path, 'r') as infile:
        for line in infile:
            parts = line.split(' ')
            if len(parts) > 5:
                domain = parts[5].strip()  # Extraer el dominio del comando y eliminar espacios en blanco
                if domain not in dominios_unicos:
                    dominios_unicos.add(domain)
                    file.write(line)

print(f"Archivo con dominios únicos se ha guardado en '{address_list_path}'.")

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

access_path = 'access.rsc'
with open(access_path, 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio, path = dividir_url(url)
            ascii_dominio = convertir_a_ascii(dominio)
            if ascii_dominio is not None:
                if path and path != "/":
                    file.write(f"{codigo_antes_divididas}dst-host={ascii_dominio} path={path}{codigo_despues_divididas}\n")
                else:
                    file.write(f"{codigo_antes_divididas}dst-host={ascii_dominio}{codigo_despues_divididas}\n")
            
            # Agregar línea con delay cada 50 líneas
            if (i + 1) % 50 == 0:
                file.write(codigo_con_delay + "\n")

print(f"Archivo con dominios y paths se ha guardado en '{access_path}'.")
