/system/script/add name=eliminar_nat source=":local commentToFind \"Bloqueo mintic by Oscar Castillo\"; :foreach item in=[/ip firewall nat find where comment=\$commentToFind] do={/ip firewall nat remove \$item}"
/system/scheduler/add comment="actualizacion mintic" name=mintic on-event=eliminar_nat interval=30d
/ip/proxy/set enabled=yes port=999 max-cache-size=2048
import addres_list.rsc
import urls.rsc
delay delay-time=5m
/file/remove addres_list.rsc
/file/remove urls.rsc
