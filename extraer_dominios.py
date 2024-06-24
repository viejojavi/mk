import re
from urllib.parse import urlparse

# Función para extraer el dominio de una URL
def obtener_dominio(url):
    try:
        dominio = urlparse(url).netloc
        if dominio.startswith("www."):
            dominio = dominio[4:]  # Remover el prefijo 'www.'
        return dominio
    except Exception as e:
        print(f"Error al procesar la URL: {url} - {e}")
        return None

# Leer el listado de URLs desde un archivo
with open('listado_urls.txt', 'r') as file:
    urls = file.readlines()

# Extraer dominios y eliminar duplicados
dominios = set()
for url in urls:
    dominio = obtener_dominio(url.strip())
    if dominio:
        dominios.add(dominio)

# Guardar los dominios únicos en un archivo
with open('dominios_unicos.txt', 'w') as file:
    for dominio in dominios:
        file.write(dominio + '\n')

print("Proceso completado. Los dominios únicos se han guardado en 'dominios_unicos.txt'.")
