import re
from urllib.parse import urlparse

# Leer el listado de URLs desde un archivo
with open('listado_urls.txt', 'r') as file:
    urls = file.readlines()

# Verificar si las URLs fueron leídas correctamente
print(f"URLs leídas: {len(urls)}")
if len(urls) > 0:
    print(f"Primera URL: {urls[0].strip()}")
    print(f"Última URL: {urls[-1].strip()}")

# Función para extraer el dominio de una URL
def obtener_dominio(url):
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        if dominio.startswith("www."):
            dominio = dominio[4:]  # Remover el prefijo 'www.'
        return dominio
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None

# Extraer dominios únicos y eliminar duplicados
dominios = set()
for url in urls:
    url = url.strip()
    if url:  # Asegurarse de que la URL no esté vacía
        dominio = obtener_dominio(url)
        if dominio:
            dominios.add(dominio)

# Generar archivo con líneas de código antes y después de cada URL
codigo_antes_con_codigos = "add list=bloqueo_mintic address="
codigo_despues_con_codigos = " comment=Bloqueo_Mintic_by_Oscar_Castillo"

with open('urls_con_codigos.txt', 'w') as file:
    for dominio in dominios:
        file.write(f"{codigo_antes_con_codigos}{dominio}{codigo_despues_con_codigos}\n")

print("Archivo con dominios únicos y códigos se ha guardado en 'urls_con_codigos.txt'.")
