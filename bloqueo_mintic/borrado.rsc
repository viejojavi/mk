:foreach item in=[/ip/firewall/address-list/find where comment="Bloqueo_Mintic_by_Oscar_Castillo"] do={/ip/firewall/address-list/remove $item}
/file/remove inicial.rsc
/file/remove borrado.rsc
:put borrado
