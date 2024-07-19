import re
from urllib.parse import urlparse
import idna

# Función para limpiar el prefijo http:// y https:// de una URL y devolver solo el dominio sin puerto
def limpiar_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Añadir http:// si no está presente
    parsed_url = urlparse(url)
    dominio = parsed_url.hostname  # Esto elimina el puerto
    try:
        dominio_ascii = idna.encode(dominio).decode('ascii')
    except idna.IDNAError:
        dominio_ascii = dominio
    return dominio_ascii

# Función para dividir una URL en dominio y path
def dividir_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Añadir http:// si no está presente
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.hostname  # Esto elimina el puerto
        path = parsed_url.path
        try:
            dominio_ascii = idna.encode(dominio).decode('ascii')
        except idna.IDNAError:
            dominio_ascii = dominio
        return dominio_ascii, path, parsed_url.port
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None, None, None

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
codigo_con_delay = "/ip/dns/cache/flush\ndelay 1"

listado_completo_path = 'listado_completo.rsc'
address_list_path = 'address_list.rsc'
puertos_eliminados_path = 'puertos_eliminados.txt'
dominios_unicos = set()  # Usar un conjunto para almacenar dominios únicos
puertos_unicos = set()   # Usar un conjunto para almacenar puertos únicos

# Crear el archivo listado_completo.rsc con todas las URLs y también generar access.rsc
with open(listado_completo_path, 'w') as listado_file, open('access.rsc', 'w') as access_file, open(puertos_eliminados_path, 'w') as puertos_file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio_limpio = limpiar_url(url)
            listado_file.write(f"{codigo_antes_con_codigos}{dominio_limpio}{codigo_despues_con_codigos}\n")

            # Agregar línea con delay cada 50 líneas en listado_completo.rsc
            if (i + 1) % 50 == 0:
                listado_file.write(codigo_con_delay + "\n")

            # Generar línea en access.rsc con dominio y path
            dominio, path, port = dividir_url(url)
            if dominio is not None:
                if path and path != "/":
                    access_file.write(f"/ip/proxy/access/add action=redirect action-data=ticcol.com/internet-sano-1 dst-host={dominio} path=\"{path}\" comment=bloqueo_mintic\n")
                else:
                    access_file.write(f"/ip/proxy/access/add action=redirect action-data=ticcol.com/internet-sano-1 dst-host={dominio} comment=bloqueo_mintic\n")

                # Registrar puerto eliminado si existía
                if port:
                    puertos_unicos.add(port)

            # Agregar línea con delay cada 50 líneas en access.rsc
            if (i + 1) % 50 == 0:
                access_file.write(codigo_con_delay + ";\n")

            # Agregar dominio limpio al conjunto de dominios únicos
            dominios_unicos.add(dominio_limpio)

# Escribir puertos únicos en el archivo puertos_eliminados.txt
with open(puertos_eliminados_path, 'w') as puertos_file:
    for port in sorted(puertos_unicos):
        puertos_file.write(f"{port}\n")

print(f"Archivo con URLs y códigos se ha guardado en '{listado_completo_path}'.")
print(f"Archivo con dominios y paths se ha guardado en 'access.rsc'.")
print(f"Archivo con puertos eliminados se ha guardado en '{puertos_eliminados_path}'.")

# Escribir dominios únicos en un nuevo archivo address_list.rsc
with open(address_list_path, 'w') as file:
    for i, dominio in enumerate(sorted(dominios_unicos)):  # Ordenar para tener consistencia en el archivo
        file.write(f"{codigo_antes_con_codigos}{dominio}{codigo_despues_con_codigos}\n")
        if (i + 1) % 50 == 0:
            file.write(codigo_con_delay + "\n")

print(f"Archivo con dominios únicos se ha guardado en '{address_list_path}'.")
