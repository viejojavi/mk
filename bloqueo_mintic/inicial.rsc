/system/script/add name=eliminar_nat source=":local commentToFind \"Bloqueo mintic by Oscar Castillo\"; :foreach item in=[/ip firewall nat find where comment=\$commentToFind] do={/ip firewall nat remove \$item}"
/system/scheduler/add comment="actualizacion mintic" name=mintic on-event=eliminar_nat interval=30d
/ip/proxy/set enabled=yes port=999 max-cache-size=2048
/tool fetch url="https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/addres_list.rsc?token=GHSAT0AAAAAACS6TKMAQLTWPVBQTHJKOC2YZTVYB2A" mode=https dst-path=addres_list.rsc 
/tool fetch url="https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/urls.rsc?token=GHSAT0AAAAAACS6TKMBHDYGHBYILXZLORQYZTV4TKQ" mode=https dst-path=urls.rsc
import addres_list.rsc
import urls.rsc
/file/remove addres_list.rsc
/file/remove urls.rsc
