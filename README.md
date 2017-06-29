# Proyecto 'Reporte de Transacciones con Códigos de respuesta 91'
![N|Solid](https://image.ibb.co/nDPMTQ/logo_Simple_Eglobal.png)

El reporte de Transacciones con códigos de respuesta 91, es un conjunto de scripts escritos en python y bash, para genearar un reporte grafico del porcentaje de Transacciones con codigo 91, tomando como base el dia actual menos 30 dias hacia atrás.Este reporte se genera diariamente.

### La estructura del proyecto es el siguiente:
 ![N|Solid](https://image.ibb.co/eTpkNk/reporte_Codigos_Respuesta.png)

 **output** : Contiene las graficas generadas de cada emisor.
 **log** : Cada que se ejecuta el script run.sh se genera un log en el cual se describen los scripts que se estan ejecutando y su estatus en caso de que existio algun error de procesamiento.
**img** :Se encuentran los logotipos nesesarios que usa la plantilla html, para presentar el reporte.
**csv** : Al ejecutar el script run.sh busca en el directorio csv el reporte de la fecha actual en formato rep_cod91_AAAA-MM-DD.csv, por lo tanto en este directorio se encuentras los reportes de la fechas que necesitemos cargar a la base de datos.
**conf** : En este directorio encontramos archivos de configuración, la cual nos indica los ficheros que adjuntamos en el email(adjunto.txt), una plantilla en html para la presentación del email(contenido.txt), el conjunto de destinatarios al cual enviaremos el reporte generado(destinatarios.txt), y las rutas de los reportes en formato png graficados que se van a adjuntar en el correo(inline.txt).
**bin** : Conjunto de scripts nesesarios para cargar los datos del reporte a la base de datos y generar el reporte para enviar por email.

# Pasos para descargar el proyecto y ejecutar el script principal (Run.sh)
>Es nesesario tener instalado git para ello nos podemos apoyar de la siguiente página https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

#### Requerimientos y configuración de ambiente

- Python 2.7 o superior
- Java jdk 7 o superior.
##### Python requiere de los siguientes módulos, para ello abrimos una terminal e instalamos los siguientes plugins.
En caso de tener instalados los siguientes módulos, ignorar este paso y comenzar la instalación
```sh
user@user$ sudo apt-get install python-pip #herramienta para instalar los modulos
user@user$ pip install pandas #Leer el csv
user@user$ pip install numpy #Contiene metodos nesesarios para graficar datos.
user@user$ pip install matplotlib #Modulo nesesario para graficar los datos.
user@user$ pip install psycopg2 #plugin para conexion a base de datos postgresql.
```
### Instalación
Abrir una consola y ejecutar los siguientes comandos:
```sh
user@user$ git clone git@github.com:ArturoGonzalezBecerril/CodigosDeRespuesta.git #Clonar el repositorio.
user@user$ cd reporteCodigoRespuesta91/
user@user$ ls -lrht
-rw-r--r-- 1 arturo arturo    0 jun 28 16:06 README.md
drwxr-xr-x 2 arturo arturo 4.0K jun 28 16:57 img
drwxr-xr-x 2 arturo arturo 4.0K jun 28 16:57 csv
drwxr-xr-x 2 arturo arturo 4.0K jun 28 16:57 conf
drwxr-xr-x 2 arturo arturo 4.0K jun 28 16:57 bin
drwxr-xr-x 2 arturo arturo 4.0K jun 28 16:57 output
drwxr-xr-x 2 arturo arturo 4.0K jun 28 16:57 log
user@user$ cd bin/
user@user$ ./Run.sh#Es nesesario que el reporte del dia anterior ya se encuentre en /csv
***Se creo el log:[log_reporte20170622.log]
Dropbox is already running!
Iniciando lectura del archivo...
Python 2.7.13
Datos cargados correctamente
Se ejecuto el stored procedure...
Iniciando el reporte de transacciones declinadas con codigo 091:
---------------Salida del programa--------------------------------
--Se genero la grafica de los siguientes emisores:
--->Bancomer
--->Banamex
***Enviando por email...
Reportes Transacciones Declinados con codigo 91
/home/arturo/proyectos/reporteCodigoRespuesta91/Version_0.1/conf/destinatarios.txt
/home/arturo/proyectos/reporteCodigoRespuesta91/Version_0.1/conf/contenidotmp.txt
/home/arturo/proyectos/reporteCodigoRespuesta91/Version_0.1/conf/adjunto.txt
/home/arturo/proyectos/reporteCodigoRespuesta91/Version_0.1/conf/inline.txt
Fin del script
```
Al final de la ejecución del script debemos obtener una salida como se muestra anteriormente.

 **Formas de ejecutar el Script ```[Run.sh]```**
-
```sh
user@user$ ./Run.sh
#Si no se pasa ningún argumento debemos de tener en cuenta lo siguiente
#-El reporte en formato rep_cod91_AAAA-MM-DD.csv ya debe de encontrarse depositado en /csv, ya que el script buscara el reporte del día anterior en ese directorio.
user@user$ ./Run.sh 2017-06-25.
#Genera solo el reporte de de la fecha escrita.
--Importante. Note que el parametro lleva un .[punto] al final, esto es un indicador para generar solo el reporte.
```
* La primera versión de como correr el script se realizó pensado, en correrlo mediante un cron, de manera automática. Ya que los reportes se generan todos los días
* La segunda opción esta pensada, en algunos escenarios donde solo  se nesesita visualizar un historico durante una fecha en especifico.

# Configuraciones adicionales
### Enviar los reportes de manera automática con Cron
- Crear una cuenta de gmail. Y crear la cuenta de dropbox accediendo con la cuenta de gmail previamente creada.
- Descargar dropbox desktop e instalarlo. En mi caso descargo el .deb(Elegir tipo de instalación personalizada"
- Cuando se esta instalando nos pide una ruta donde depositar nuestra carpeta dropbox, para ello escribimos lo siguiente ”/home/usuario/Dropbox/Aplicaciones/reporte_091”, donde usuario es el de la máquina
- Para finalizar accedemos a la siguiente pagina: https://sendtodropbox.com/ esta pagina no sirve para vincular a un correo nuestra cuenta de dropbox, de esta manera, cada que reenviemos un archivo a el correo asociado se descargara automáticamente a nuestra carpeta sincronizada de dropbox.
- En nuestro correo debemos crear una regla, para que cada que llegue un reporte lo reenviemos automáticamente  al correo asociado a nuestra cuenta de dropbox.
- Por ultimo crear un pequeño script que mueva el reporte de nuestra carpeta de dropbox a la carpeta csv, de esta manera, el reporte se estaria cargando sin nesesidad de tener que copiar manualmente el reporte.

Licencia
----
2017-Junio-28 Eglobal

