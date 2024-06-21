ip/proxy/set enabled=yes port=999 max-cache-size=2048
ip/firewall/nat/add chain=dstnat dst-address-list=bloqueo_mintic protocol=tcp dst-port=80 action=redirect to-ports=999 place-before=0 comment="Bloqueo mintic by Oscar Castillo"
/tool fetch url="https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/addres_list.rsc?token=GHSAT0AAAAAACS6TKMAQLTWPVBQTHJKOC2YZTVYB2A" mode=https dst-path=addres_list.rsc 
/tool fetch url="https://raw.githubusercontent.com/viejojavi/mk/main/bloqueo_mintic/inicial.rsc?token=GHSAT0AAAAAACS6TKMAWKE6MRUOVD2RJODMZTV4F2Q" mode=https dst-path=urls.rsc

