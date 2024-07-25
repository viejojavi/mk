:foreach item in=[/ip/firewall/address-list/find where comment="Bloqueo_Mintic_by_Oscar_Castillo"] do={/ip/firewall/address-list/remove $item}
:foreach item in=[/ip/proxy/access/find where comment="bloqueo_mintic"] do={/ip/proxy/access/remove $item}
:foreach item in=[/system/script/find where comment="Bloqueo mintic by Oscar Castillo"] do={/system/script/remove $item}
:foreach item in=[/system/script/find where comment="Flush cache by Oscar Castillo"] do={/system/script/remove $item}
:foreach item in=[/system/scheduler/find where comment="actualizacion mintic"] do={/system/scheduler/remove $item}
:foreach item in=[/system/scheduler/find where comment="Flush dns by Oscar Castillo"] do={/system/scheduler/remove $item}
:foreach item in=[/ip/firewall/nat/find where comment="Bloqueo mintic by Oscar Castillo"] do={/ip/firewall/nat/remove $item}
:foreach item in=[/system/scheduler/find where comment="actualizacion mintic"] do={/system/scheduler/remove $item}
:foreach item in=[/system/script/find where comment="Actualizacion bloqueos"] do={/system/script/remove $item}
:foreach item in=[/system/scheduler/find where comment="update"] do={/system/scheduler/remove $item}
:local LogLineas [/system/logging/action/get memory memory-lines]; /system/logging/action/set memory memory-lines=1; :delay 1; /system/logging/action/set memory memory-lines=$LogLineas
/file/remove address_list.rsc
/file/remove acces.rsc
/file/remove inicial.rsc
/file/remove borrado.rsc
:put "para continuar con tus bloqueos comunicate con el numero +573007081170"
