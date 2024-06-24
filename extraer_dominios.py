import re
from urllib.parse import urlparse

# Función para extraer el dominio de una URL
def obtener_dominio(url):
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        if dominio.startswith("www."):
            dominio = dominio[4:]  # Remover el prefijo 'www.'
        print(f"Procesado dominio: {dominio} para URL: {url}")
        return dominio
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None

# Función para limpiar el prefijo http:// y https:// de una URL
def limpiar_url(url):
    url = re.sub(r'^https?://', '', url)  # Eliminar http:// o https://
    return url
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

# Leer el listado de URLs desde un archivo
with open('listado_urls.txt', 'r') as file:
    urls = file.readlines()

# Verificar si las URLs fueron leídas correctamente
print(f"URLs leídas: {len(urls)}")
if len(urls) > 0:
    print(f"Primera URL: {urls[0].strip()}")
    print(f"Última URL: {urls[-1].strip()}")

# Extraer dominios y eliminar duplicados
dominios = set()
for url in urls:
    url = url.strip()
    if url:  # Asegurarse de que la URL no esté vacía
        dominio = obtener_dominio(url)
        if dominio:
            dominios.add(dominio)

# Verificar los dominios extraídos
print(f"Dominios extraídos: {dominios}")
print(f"Total de dominios únicos: {len(dominios)}")

# Guardar los dominios únicos en un archivo
with open('dominios_unicos.txt', 'w') as file:
    for dominio in dominios:
        file.write(dominio + '\n')
# Generar archivo con líneas de código antes y después de cada URL
codigo_antes = "add list=bloqueo_mintic address="
codigo_despues = " comment=Bloqueo_Mintic_by_Oscar_Castillo"

with open('urls_con_codigos.txt', 'w') as file:
    for url in urls:
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            url_limpia = limpiar_url(url)
            file.write(f"{codigo_antes}{url_limpia}{codigo_despues}\n")

# Generar archivo con dominio y path de cada URL
with open('urls_divididas.txt', 'w') as file:
    for url in urls:
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            dominio, path = dividir_url(url)
            if dominio is not None:
                if path:
                    file.write(f"dst-host={dominio}, path={path}\n")
                else:
                    file.write(f"dst-host={dominio}\n")

print("Proceso completado. Los dominios únicos se han guardado en 'dominios_unicos.txt'.")
print("Archivo con URLs y códigos se ha guardado en 'urls_con_codigos.txt'.")
print("Archivo con dominios y paths se ha guardado en 'urls_divididas.txt'.")


