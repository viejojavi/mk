import re
from urllib.parse import urlparse
import socket

# Función para limpiar el prefijo http:// y https:// de una URL y devolver solo el dominio
def limpiar_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Añadir http:// si no está presente
    parsed_url = urlparse(url)
    dominio = parsed_url.netloc
    return dominio

# Función para dividir una URL en dominio y path
def dividir_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Añadir http:// si no está presente
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        path = parsed_url.path
        return dominio, path
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None, None

# Función para obtener la dirección IP de un dominio
def obtener_ip(dominio):
    try:
        ip = socket.gethostbyname(dominio)
        return ip
    except socket.gaierror as e:
        print(f"Error al resolver la IP del dominio {dominio}: {e}")
        return None

# Leer el listado de URLs desde un archivo
with open('listado_urls.txt', 'r') as file:
    urls = file.readlines()

# Generar archivo con líneas de código antes y después de cada URL
codigo_antes_con_codigos = "/ip/firewall/address-list/add list=bloqueo_mintic address="
codigo_despues_con_codigos = " comment=Bloqueo_Mintic_by_Oscar_Castillo"
codigo_con_delay = "delay 1"

listado_completo_path = 'listado_completo.rsc'
dominios_unicos = set()  # Usar un conjunto para almacenar dominios únicos

# Crear el archivo listado_completo.rsc con todas las URLs y también generar access.rsc
with open(listado_completo_path, 'w') as listado_file, open('access.rsc', 'w') as access_file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio_limpio = limpiar_url(url)
            listado_file.write(f"{codigo_antes_con_codigos}{dominio_limpio}{codigo_despues_con_codigos}\n")
            
            # Agregar línea con delay cada 50 líneas en listado_completo.rsc
            if (i + 1) % 50 == 0:
                listado_file.write(codigo_con_delay + "\n")
            
            # Generar línea en access.rsc con dominio y path
            dominio, path = dividir_url(url)
            if dominio is not None:
                if path and path != "/":
                    access_file.write(f"/ip/proxy/access/add action=redirect action-data=ticcol.com/internet-sano-1 dst-host={dominio} path={path} comment=bloqueo_mintic\n")
                else:
                    access_file.write(f"/ip/proxy/access/add action=redirect action-data=ticcol.com/internet-sano-1 dst-host={dominio} comment=bloqueo_mintic\n")
            
            # Agregar línea con delay cada 50 líneas en access.rsc
            if (i + 1) % 50 == 0:
                access_file.write(codigo_con_delay + "\n")
            
            # Agregar dominio limpio al conjunto de dominios únicos
            dominios_unicos.add(dominio_limpio)

print(f"Archivo con URLs y códigos se ha guardado en '{listado_completo_path}'.")

address_list_path = 'address_list.rsc'
# Escribir IPs únicas en un nuevo archivo address_list.rsc
with open(address_list_path, 'w') as file:
    for dominio in sorted(dominios_unicos):  # Ordenar para tener consistencia en el archivo
        ip = obtener_ip(dominio)
        if ip:
            file.write(f"{codigo_antes_con_codigos}{ip}{codigo_despues_con_codigos}\n")

print(f"Archivo con IPs únicas se ha guardado en '{address_list_path}'.")
print(f"Archivo access.rsc se ha generado correctamente.")
