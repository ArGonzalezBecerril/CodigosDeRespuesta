import pandas as pd
import psycopg2
import sys
import getopt
from datetime import datetime
from pandas.compat import FileNotFoundError
from pandas.parser import CParserError
from send2trash import send2trash as eliminar

__conn_string = "host='localhost' dbname='integridad' user='postgres' password='postgres'"
# --------------------------------------------------------------------------------------------------------------------
'''
Version: 0.1
Author:Arturo Gonzalez
email:agonzalezb@eglobal.com.mx

El script nesesita 2 Argumentos

-p[path]   -- Ruta completa del ArchivoFuente

-d[days]
           -- Representa numero de dias a restar para obtener el reporte de una fecha especifica.(Historico de datos)
               El numero de dias se debe obtener restando la fecha Actual, menos la fecha en que fueron reportado los datos del
               archivo fuente, esta fecha se encuentra dentro del archivo csv.
              (Ejemplo: Si la fecha de Reporte csv pertenecen a 2017-06-15 y la fecha de hoy es 2017-06-17 se tiene que realizar la
               resta =(2017-06-17) - (2017-06-17) = 2, el cual representa el numero de dias a restar para obtener el reporte de esa fecha

-a[alpha]  --Valor de alpha el cual determinara, que tanto peso se dara a las muetras recientes o las historicas.
               [0 <= n <= 1] donde n representa un conjunto de valores entre 0 y 1.

-w[window_size]
            --Tamanio de Ventana, se refiere al numero de muestras que se tomaran, respecto al historico de datos que se tiene, para obtener
              los datos estadisticos.
              [4 >= n <= 30] donde n representa un conjunto de valores entre 4 y 30.

Run script -- Ejemplo de ejecutar el Script[ --> python cargarRepCodMsg.py -p "/home/arturo/Descargas/rep_cod91_2017-06-14.csv" -d 1 -a .3 -w 4
'''
path_csv = ""
dias = 0
alpha=0
window_size=0

try:
    my_opts, args = getopt.getopt(sys.argv[1:], "p:d:a:w:", ["path=", "dias=","alpha=","window_size="])
    if len(my_opts) < 4:
        print "Argumentos incompletos"
        sys.exit(1)
except getopt.GetoptError:
    print "Error en los argumentos"
    sys.exit(2)

for opt, arg in my_opts:
    if opt in ("-p", "--path"):
        path_csv = str(arg).strip()
    elif opt in ("-d", "--dias"):
        dias = int(str(arg).strip())
        if dias < 1:
            print "El numero de dias debe ser mayor a 0"
            sys.exit(3)
    elif opt in ("-a", "--alpha"):
        alpha = float(str(arg).strip())
        if (alpha >= 1 and alpha <= 0):
            print "Alpha debe tener un valor mayor o igual que 0 y menor o igual que 1"
            sys.exit(7)
    elif opt in ("-w", "--window_size"):
        window_size = int(str(arg).strip())
        if (window_size <= 4 and window_size >= 30):
            print "El tamanio de Ventana deve ser mayor o igual a 4 y menor o igual a 30"
            sys.exit(8)
    else:
        print("Parametro '" + opt + "' no reconocido")

# -----------------------------------------------------------------------------------------------------------------------

'''Leer el Csv, validar datos y cargarlos a la BD'''


def read_csv(path_csv):
    try:
        report_csv = pd.read_csv(path_csv, encoding="utf-16", skiprows=3, header=None, dtype=str)
        return report_csv
    except FileNotFoundError:
        print("No se encontro el archivo de reporte codigos de mensaje 091. Validar el path")
        sys.exit(4)
    except CParserError:
        print("Error en los datos, un emisor de los 4 tiene datos incompletos.")
        sys.exit(5)


#-----------------------------------------------------------------------------------------------------------------------

'''Validar los datos del reporte. '''

def validate_data(report):
    array_report = report.as_matrix()
    list_report = array_report.tolist()
    if len(array_report) != 4:
        print('El numero de Emisores en el Reporte es incorrecto, Emisores esperados=4,Emisores encontrados:' + str(
            len(array_report)))
        sys.exit(6)
    return list_report


# -----------------------------------------------------------------------------------------------------------------------
# Validar si ya existe datos con la fecha de reporte dentro de la base de datos.
def date_exists(param_date):
    conn = psycopg2.connect(__conn_string)
    __cursorX = conn.cursor()
    __cursorX.execute("select count(*) from mensajes_091 where fecha='" + str(param_date) + "'")
    exist_date = __cursorX.fetchall()
    conn.close()
    return (False, True)[exist_date[0][0] > 1]  # ya existe un reporte con la fecha que se va agregar.


# -----------------------------------------------------------------------------------------------------------------------
# Volcar datos a postgresql

def insert_data(row_):
    conn = psycopg2.connect(__conn_string)
    __cursorX = conn.cursor()
    __cursorX.execute(
        "INSERT INTO mensajes_091 (fecha, id_emisor, nombre_emisor, txs_con_codigo_91, txs_total, plataforma)"
        " VALUES (%s, %s, %s, %s, %s, %s)",row_)
    __cursorX.execute("commit")
    conn.close()


# -----------------------------------------------------------------------------------------------------------------------
# Invocar el store procedure  pasando el numero de dias
def call_stored_procedure(alpha,window_size,historical_days):
    conn = psycopg2.connect(__conn_string)
    __cursorX = conn.cursor()
    __cursorX.execute("SELECT process_data(" + str(alpha) +"," +str(window_size) +"," +str(historical_days) +")")
    __cursorX.execute("commit")
    conn.close()
    print "Se ejecuto el stored procedure..."

#process_data(alpha numeric, window_size integer, historical_days integer)
#-----------------------------------------------------------------------------------------------------------------------
'''
   Invocar las funciones nesesarias para cargar los datos a la BD
   ------------Main----------------------------------------------
'''
data_csv = read_csv(path_csv)
report_export = validate_data(data_csv)

if len(report_export) != 4:
    print "El numero de emisores debe ser 4, para cargar a la BD"
else:
    # validar que sea una fecha con formato correcto
    #validate_dates_file(report_export)
    get_date_ = str(report_export[0][0])
    if date_exists(get_date_):
        print "Ya existen datos reportados con la fecha:" + get_date_
        sys.exit(7)
    else:
        for row in report_export:
            insert_data(row)
        print "Datos cargados correctamente"
        call_stored_procedure(alpha,window_size,dias)
        #print "El archivo se envio a la papelera de reciclaje:" + path_csv
        #eliminar(path_csv)
