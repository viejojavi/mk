import re
from urllib.parse import urlparse

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

listado_completo_path = 'listado_completo.rsc'
address_list_path = 'address_list.rsc'
dominios_unicos = set()  # Usar un conjunto para almacenar dominios únicos

with open(listado_completo_path, 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio_limpio = limpiar_url(url)
            file.write(f"{codigo_antes_con_codigos}{dominio_limpio}{codigo_despues_con_codigos}\n")

            # Agregar línea con delay cada 50 líneas
            if (i + 1) % 50 == 0:
                file.write(codigo_con_delay + "\n")

print(f"Archivo con URLs y códigos se ha guardado en '{listado_completo_path}'.")

# Filtrar dominios únicos y escribir en un nuevo archivo
with open(address_list_path, 'w') as file:
