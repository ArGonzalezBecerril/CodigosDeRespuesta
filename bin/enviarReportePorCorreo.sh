#!/bin/bash
#version 0.1
#Author:Arturo Gonzalez.


#Capturando la fecha del reporte
set -e
fecha=$1
#Obtener la ruta en que nos encontramos situado

rm ../conf/adjunto.txt
touch ../conf/adjunto.txt

#Obtenr la url donde se encuentran depositados las graficas
ruta_absoluta=$(pwd)
url_raiz="${ruta_absoluta//bin}"

#log del aplicativo
log="${ruta_absoluta//bin}""log/log_reporte""${fecha//-}"".log"

rowBancomerAtm=$url_raiz"output/BancomerATM""${fecha//-}"".png"
rowBancomerPos=$url_raiz"output/BancomerPOS""${fecha//-}"".png"
rowBanamexAtm=$url_raiz"output/BanamexATM""${fecha//-}"".png"
rowBanamexPos=$url_raiz"output/BanamexPOS""${fecha//-}"".png"
rowLogo=$url_raiz"img/logoEglobal.png"

echo "***Se creo el archivo" >> $log

echo "***Agregando los reportes para enviar por email." >> $log
#Eliminar, crear e insertar los graficos que se adjuntaran en el correo.
rm ../conf/inline.txt
touch ../conf/inline.txt

bbvaPos="imgBancomerPos#"$rowBancomerPos
bbvaAtm="imgBancomerAtm#"$rowBancomerAtm
bnmxPos="imgBanamexPos#"$rowBanamexPos
bnmxAtm="imgBanamexAtm#"$rowBanamexAtm
logoEglobal="logo#"$rowLogo

echo $bbvaPos >> $url_raiz"conf/inline.txt"
echo $bbvaAtm >> $url_raiz"conf/inline.txt"
echo $bnmxPos >> $url_raiz"conf/inline.txt"
echo $bnmxAtm >> $url_raiz"conf/inline.txt"
echo $logoEglobal >> $url_raiz"conf/inline.txt"

echo "***Se agregaron los reportes." >> $log

#Agregando la Fecha del Reporte
#Crear contenido html temporal para insertar la fecha del reporte
cp ../conf/contenido.txt ../conf/contenidotmp.txt
#Agregar formato YYYY-mm-dd
sed -i -- 's/#keyDate/'$fecha'/g' ../conf/contenidotmp.txt

#Enviar el email
echo "***Enviando por email..."
scala -cp ReportGenerator.jar com.mx.eglobal.main.CreateMail "Reportes Transacciones Declinados con codigo 91" $url_raiz"conf/destinatarios.txt" $url_raiz"conf/contenidotmp.txt" $url_raiz"conf/adjunto.txt" $url_raiz"conf/inline.txt"

echo "***Eliminando archivos temporales" >> $log
rm $url_raiz"conf/contenidotmp.txt"
echo "***Fin del script." >> $log
