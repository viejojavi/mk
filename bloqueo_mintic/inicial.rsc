:put "Iniciamos instalacion de Reglas para Bloqueo Mintic"
/system/script/add name=eliminar_nat source=":local commentToFind \"Bloqueo mintic by Oscar Castillo\"; :foreach item in=[/ip firewall nat find where comment=\$commentToFind] do={/ip firewall nat remove \$item}"
:put "Script Agregado"
/system/scheduler/add comment="actualizacion mintic" name=mintic on-event=eliminar_nat interval=30d
:put "Tarea Agregada"
/ip/proxy/set enabled=yes port=999 max-cache-size=2048
:put "Proxy habilitado"
/tool/fetch url=https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/addres_list.rsc; import file-name=addres_list.rsc
:put "Lista Agregada y nat funcional"
/tool/fetch url=https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/urls.rsc; import file-name=urls.rsc
:put "Access agregados"
delay delay-time=5m
/file/remove addres_list.rsc
:put "lista eliminada"
/file/remove urls.rsc
:put "Acces eliminados"
