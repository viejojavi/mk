:put "Iniciamos instalacion de Reglas para Bloqueo Mintic"
:foreach item in=[/system/script/find where comment="Bloqueo mintic by Oscar Castillo"] do={/system/script/remove $item}
/system/script/add name=eliminar_nat source=":local commentToFind \"Bloqueo mintic by Oscar Castillo\"; :foreach item in=[/ip firewall nat find where comment=\$commentToFind] do={/ip firewall nat remove \$item}" comment="Bloqueo mintic by Oscar Castillo"
:foreach item in=[/system/script/find where comment="Flush dns by Oscar Castillo"] do={/system/script/remove $item}
/system/script/add source={/ip/dns/cache/flush} comment="Flush cache by Oscar Castillo" name=flush_dns
:foreach item in=[/system/scheduler/find where comment="actualizacion mintic"] do={/system/scheduler/remove $item}
/system/scheduler/add name="flush dns" comment="Flush dns by Oscar Castillo" on-event=flush_dns interval=00:05:00
#:put "Script Agregado"
:foreach item in=[/ip/firewall/nat/find where comment="Bloqueo mintic by Oscar Castillo"] do={/ip/firewall/nat/remove $item}
/ip/firewall/connection/tracking/set enabled=yes
/ip/firewall/nat/add chain=dstnat dst-address-list=bloqueo_mintic protocol=tcp dst-port=80,81,8080,9388 action=redirect to-ports=999 comment="Bloqueo mintic by Oscar Castillo"
#:put "Nat Habilitado"
:foreach item in=[/system/scheduler/find where comment="actualizacion mintic"] do={/system/scheduler/remove $item}
/system/scheduler/add comment="actualizacion mintic" name=mintic on-event=eliminar_nat interval=30d
#:put "Tarea Agregada"
/ip/proxy/set enabled=yes port=999 max-cache-size=9128
/ip/dns/set cache-size=9128KiB
#:put "Proxy habilitado"
:foreach item in=[/ip/firewall/address-list/find where comment="Bloqueo_Mintic_by_Oscar_Castillo"] do={/ip/firewall/address-list/remove $item}
/tool/fetch url="https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/address_list.rsc"; import file-name=address_list.rsc
#:put "Lista Agregada"
:foreach item in=[/ip/proxy/access/find where comment="bloqueo_mintic"] do={/ip/proxy/access/remove $item}
/tool/fetch url="https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/acces.rsc"; import file-name=acces.rsc
#:put "Access agregados"
delay delay-time=5s
/file/remove address_list.rsc
#:put "lista eliminada"
/file/remove acces.rsc
#:put "Acces eliminados"
/file/remove inicial.rsc
/system/script/add comment="Actualizacion bloqueos" name=actualizacion source={/tool/fetch url=https://mk.ticcol.com/inicial.rsc; import file-name=inicial.rsc}
/system/scheduler/add comment=update interval=08:00:00 name=update on-event=actualizacion
:local LogLineas [/system/logging/action/get memory memory-lines]; /system/logging/action/set memory memory-lines=1; :delay 1; /system/logging/action/set memory memory-lines=$LogLineas
:put "Tarea Finalizada"
