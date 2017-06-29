#!/bin/bash
#version 0.1
#Author:Arturo Gonzalez Becerril

set -e
# Any subsequent(*) commands which fail will cause the shell script to exit immediately
# If no arguments are supplied, asume files are from yesterday

if [ -z "$1" ]
   then fecha=$(date -d "1 day ago" '+%Y-%m-%d')
   else fecha=$1
fi

ruta_absoluta=$(pwd)
log="${ruta_absoluta//bin}""log/log_reporte""${fecha//-}"".log"
touch $log

echo "***Iniciando dropbox..." >> $log
echo "***Se creo el log:[log_reporte""${fecha//-}"".log]"
dropbox start
sleep 10

file="/home/arturo/Dropbox/Aplicaciones/reporte_091/rep_cod91_""${fecha}"".csv"


if [ -f "$file" ]
then
    #mover el fichero csv de la carpeta dropbox a la carpeta csv del proyecto.
    ./moverReporte.sh $fecha
    #carga y genera el reporte del fichero csv procesado.
    ./cargarYGenerarReporte.sh $fecha
    #envia por email los .png generados
    ./enviarReportePorCorreo.sh $fecha
elif [[ $fecha == *"."* ]]
then
    fechaValida=${fecha//.}
    
    
else
  echo "***No se encontro ningun reporte." >> $log
  exit 1
fi
