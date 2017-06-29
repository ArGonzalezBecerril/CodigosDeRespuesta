#!/bin/bash
#Version 0.1
#Author: Arturo Gonzalez Becerril
#mail:agonzalezb@eglobal.com.mx
# run script -> bash ./cargar_datosDB.sh [arg1]
# arg1         - Representa la fecha en el cual se quiere obtener el reporte estadistico a partir de
#                esta fecha se contaran 30 dias hacia atras para mostrar el historico de datos.
#              - En caso de desear obtener el reporte de ayer no se pasa ningun argumento.
#              - Para el formato de fecha se usa la siguiente estructura.
#                ./cargar_datosDB.sh YYYY-MM-DD  --> Ejemplo: ./cargar_datosDB.sh 2017-06-15  
set -e
fecha=""
if [ -z "$1" ]
   then fecha=$(date -d "1 day ago" '+%Y-%m-%d')
   else fecha=$1
fi

ruta_absoluta=$(pwd)
log="${ruta_absoluta//bin}""log/log_reporte""${fecha//-}"".log"

echo "***Log[Reporte de transacciones declinadas con codigo de respuesta 091]" >> $log
file="/home/arturo/Dropbox/Aplicaciones/reporte_091/rep_cod91_""${fecha}"".csv"

#Si no se agrega ningun argumento al lanzar el script. Realizar el reporte por defecto.
if [ -f "$file" ]
then
    echo "***Fichero encontrado. Se copiara a la ruta ${ruta_absoluta}""/csv" >> $log
    mv $file "${ruta_absoluta//bin}""csv/reporte${fecha//-}.csv" 
else
	echo "***No se encontro ningun reporte." >> $log
	exit 1
fi