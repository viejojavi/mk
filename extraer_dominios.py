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

# Generar archivo con líneas de código antes y después de cada URL, eliminando duplicados
codigo_antes_con_codigos = "add list=bloqueo_mintic address="
codigo_despues_con_codigos = " comment=Bloqueo_Mintic_by_Oscar_Castillo"
codigo_con_delay = " delay 1"

# Utilizar un conjunto para almacenar los dominios únicos
dominios_unicos = set()

with open('urls_con_codigos.txt', 'w') as file:
    for i, url in enumerate(urls):
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            url_limpia = limpiar_url(url)
            parsed_url = urlparse(url_limpia)
            dominio = parsed_url.netloc
            if dominio.startswith("www."):
                dominio = dominio[4:]  # Remover el prefijo 'www.'
            
            # Verificar si el dominio ya ha sido procesado para evitar duplicados
            if dominio not in dominios_unicos:
                dominios_unicos.add(dominio)
                file.write(f"{codigo_antes_con_codigos}{dominio}{codigo_despues_con_codigos}\n")
        
        # Agregar línea con delay cada 50 líneas
        if (i + 1) % 50 == 0:
            file.write(f"{codigo_con_delay}\n")

print("Archivo con URLs y códigos se ha guardado en 'urls_con_codigos.txt'.")

# Función para dividir una URL en dominio y path
def dividir_url(url):
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        if dominio.startswith("www."):
            dominio = dominio[4:]  # Remover el prefijo 'www.'
        path = parsed_url.path
        return dominio, path
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None, None

# Generar archivo con dominio y path de cada URL, sin eliminar duplicados
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
print("Proceso completado. Los dominios únicos se han guardado en 'dominios_unicos.txt'.")
