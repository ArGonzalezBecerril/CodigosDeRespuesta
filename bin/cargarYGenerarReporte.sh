
#!/bin/bash
#version 0.1
#Author:Arturo González Becerril.
#Script que carga el reporte de rechazos arqc a base de datos y genera un reporte grafico en base a los parametros que le pasen como valor

#Demo Ejemplo Ejecutar sh --> GenerarReporte.sh /home/arturo/reporteARQC/csv/reporte20170425.csv 1 Bancomer,Banamex 60 /home/arturo/reporteARQC/output/
#Descripcion              --> GenerarReporte.sh [rutaCsv] [numero] [emisor] [rangodias] [salida]

#----------------------Descripcion de los parametros que recibe el script-------------------------------#

#[rutaCsv]            --> Ruta origen donde se encuentra el fichero de reporte arqc
#[numero]             --> Se obtiene de la resta [fecha actual - fecha en que se genero el reporte, esta fecha se encuentra en el csv de reporte arqc]
#[Emisores]           --> Los emisores van separados por comas y puedes ser los siguentes[Bancomer,Banamex,Prosa,Bancoppel].
#[salida]             --> Directorio de salida en donde se depositaran los reportes en formato png. 
set -e
fechaReporte=$1

#Obtener la ruta actual donde nos encontramos
ruta_absoluta=$(pwd)
url_raiz="${ruta_absoluta//bin}"

log="${ruta_absoluta//bin}""log/log_reporte""${fechaReporte//-}"".log"


fechaActual=$(date -d "0 day ago" '+%Y-%m-%d')
rutaCsv=$url_raiz"csv/reporte""${fechaReporte//-}"".csv"

echo "**********Directorio del csv:[""$rutaCsv""]" >> $log

numero=$((($(date -ud $fechaActual +'%s')-$(date -ud $fechaReporte +'%s'))/60/60/24))

#--------------------------Valores por defecto del Reporte. Pueden ser modificados.----------------#
emisor="Bancomer,Banamex"
rangodias=60
salida=$url_raiz"output/"
alpha=.75
historic_days=30
window_size=7


echo "Emisores:""$emisor" >> $log
#Ejecutar el script que hace una lectura del los datos del reporte csv y los carga a base de datos
echo "Iniciando lectura del archivo..."
/usr/bin/python --version

#Validar si solo se cargaran los datos a la Base de Datos.
/usr/bin/python cargarRepCodMsg.py -p ${rutaCsv} -d ${numero} -a ${alpha} -w ${window_size}

codigosalida="${?}"

if [ $codigosalida != "0" ]; then
   echo "***No se ejecuto correctamente el script cargarRepCodMsg" >> $log
   exit 2
else
   echo "***Generando el reporte..." >> $log
   echo "***Emisor:${emisor}" >> $log
   echo "***Rango de dias:${rangodias}" >> $log
   echo "***Path de los archivos de salida:${salida}" >> $log
   /usr/bin/python generarReporteMsg91.py -e ${emisor} -d ${rangodias} -o ${salida}
   echo "***Fin del proceso" >> $log
fi

