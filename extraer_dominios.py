import re
from urllib.parse import urlparse
from github import Github

# Función para limpiar el prefijo http:// y https:// de una URL
def limpiar_url(url):
    url = re.sub(r'^https?://', '', url)  # Eliminar http:// o https://
    return url

# Leer el listado de URLs desde un archivo
with open('listado_urls.rsc', 'r') as file:
    urls = file.readlines()

# Verificar si las URLs fueron leídas correctamente
print(f"URLs leídas: {len(urls)}")
if len(urls) > 0:
    print(f"Primera URL: {urls[0].strip()}")
    print(f"Última URL: {urls[-1].strip()}")

# Generar archivo con líneas de código antes y después de cada URL
codigo_antes_con_codigos = "add list=bloqueo_mintic address="
codigo_despues_con_codigos = " comment=Bloqueo_Mintic_by_Oscar_Castillo"

with open('urls_con_codigos.txt', 'w') as file:
    for url in urls:
        url = url.strip()
        if url:  # Asegurarse de que la URL no esté vacía
            url_limpia = limpiar_url(url)
            file.write(f"{codigo_antes_con_codigos}{url_limpia}{codigo_despues_con_codigos}\n")

print("Archivo con URLs y códigos se ha guardado en 'urls_con_codigos.txt'.")

# Autenticación en GitHub
# Reemplaza con tu token de acceso personal de GitHub y el nombre de usuario del repositorio
token = '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'
repo_owner = 'viejojavi'
repo_name = 'mk'

g = Github(token)
repo = g.get_repo(f"{repo_owner}/{repo_name}")

# Actualizar el archivo listado_urls.rsc en el repositorio de GitHub
path_to_file = 'bloqueo_mintic/listado_urls.rsc'
branch_name = 'main'

with open('urls_con_codigos.txt', 'r') as file:
    content = file.read()

try:
    # Obtener el archivo existente en el repositorio
    file = repo.get_contents(path_to_file, ref=branch_name)
    
    # Actualizar el contenido del archivo
    repo.update_file(path_to_file, "Actualización de listado_urls.rsc desde script", content, file.sha, branch=branch_name)
    print(f"Archivo {path_to_file} actualizado correctamente en el repositorio.")
except Exception as e:
    print(f"No se pudo actualizar el archivo en el repositorio: {e}")

print("Proceso completado.")
