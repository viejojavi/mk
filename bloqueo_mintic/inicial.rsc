:put "Iniciamos instalacion de Reglas para Bloqueo Mintic"
:foreach item in=[/system/script/find where comment="Bloqueo mintic by Oscar Castillo"] do={/system/script/remove $item}
/system/script/add name=eliminar_nat source=":local commentToFind \"Bloqueo mintic by Oscar Castillo\"; :foreach item in=[/ip firewall nat find where comment=\$commentToFind] do={/ip firewall nat remove \$item}" comment="Bloqueo mintic by Oscar Castillo"
:put "Script Agregado"
:foreach item in=[/ip/firewall/nat/find where comment="Bloqueo mintic by Oscar Castillo"] do={/ip/firewall/nat/remove $item}
/ip/firewall/nat/add chain=dstnat dst-address-list=bloqueo_mintic protocol=tcp dst-port=80 action=redirect to-ports=999 comment="Bloqueo mintic by Oscar Castillo"
:put "Nat Habilitado"
:foreach item in=[/system/scheduler/find where comment="actualizacion mintic"] do={/system/scheduler/remove $item}
/system/scheduler/add comment="actualizacion mintic" name=mintic on-event=eliminar_nat interval=30d
:put "Tarea Agregada"
/ip/proxy/set enabled=yes port=999 max-cache-size=2048
:put "Proxy habilitado"
:foreach item in=[/ip/firewall/address-list/find where comment="Bloqueo_Mintic_by_Oscar_Castillo"] do={/ip/firewall/address-list/remove $item}
/tool/fetch url="https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/address_list.rsc"; import file-name=addres_list.rsc
:put "Lista Agregada"
:foreach item in=[/ip/proxy/access/find where comment="bloqueo_mintic"] do={/ip/proxy/access/remove $item}
/tool/fetch url="https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/urls.rsc"; import file-name=urls.rsc
:put "Access agregados"
delay delay-time=5s
/file/remove addres_list.rsc
:put "lista eliminada"
/file/remove urls.rsc
:put "Acces eliminados"
/file/remove inicial.rsc
:put "Tarea Finalizada"
