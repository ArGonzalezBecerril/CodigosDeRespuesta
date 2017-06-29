import psycopg2
import matplotlib.pyplot as plt
import sys
import getopt
import os
import numpy as np
from matplotlib.dates import DayLocator, DateFormatter, HourLocator

_SQL_HISTORIC_DATA="SELECT fecha,nombre_emisor,plataforma,proporcion_msg_91,stand_desv,average_mov,average_mov_exp,mean" \
                   " FROM mensajes_091 WHERE fecha > now()::Date - "

__conn_string = "host='localhost' dbname='integridad' user='postgres' password='postgres'"

# -----------------------------------------------------------------------------------------------------------------------
# main run the program

'''
Author:Arturo Gonzalez
version:0.1
email:agonzalezb@eglobal.com.mx

 -numero dias,emisor,rutaSalida


El script nesesita 3 Argumentos(emisor,dias,output o salida)

  -e   -- Nombre del Emisor
          ->Si solo se requiere los reportes de Bancomer, se debe escribir de la siguiente manera 'Bancomer,Banamex'
          ->Si se requieren todos, se debe escribir 'Bancomer,Banamex'

  -d   -- Representa los ultimos  dias pasados para ver el reporte de Rechazos Arqc
          d - No debe ser un numero negativo

  -o   -- Ruta [Directorio] en la cual se depositaran los reportes generados.
       -->Ejemplo :python generarReporteMsg91.py -e Bancomer -d 60 -o /home/reportes/

'''
emisor = ""
dias = 0
rutasalida = ""
emisorValido = ["Bancomer", "Banamex"]
listaEmisor = []
try:
    myopts, args = getopt.getopt(sys.argv[1:], "e:d:o:", ["emisor=", "dias=", "salida="])
    if len(myopts) < 3:
        print "Argumentos incompletos"
        sys.exit(1)
except getopt.GetoptError:
    print "Error en los argumentos"
    sys.exit(2)

for opt, arg in myopts:
    if opt in ("-e", "--emisor"):
        listaEmisor = str(arg).strip().split(",")

    elif opt in ("-d", "--dias"):
        dias = int(str(arg).strip())
        if dias < 3:
            print "El numero de dias debe ser mayor a 3"
            sys.exit(3)
    elif opt in ("-o", "--salida"):
        existeRuta = os.path.isdir(str(arg).strip())
        if existeRuta and str(arg).strip()[-1][0] == '/':
            rutasalida = str(arg).strip()
        else:
            print "El directorio donde se depositaran las graficas no es correcto. O bien falta una Diagonal"
            sys.exit(4)
    else:
        print("Parametro '" + opt + "' no reconocido")


# -----------------------------------------------------------------------------------------------------------------------
# Obtener los historicos de los ultimos n dias, por defecto se asignara un valor de 30. Pero el parametro puede ser modificado.
def get_last_rows(num_records):
    conn = psycopg2.connect(__conn_string)
    __cursorX = conn.cursor()
    __cursorX.execute(_SQL_HISTORIC_DATA + str(num_records) + " ORDER BY fecha,nombre_emisor,plataforma")
    __records = __cursorX.fetchall()
    conn.close()
    return __records

# -----------------------------------------------------------------------------------------------------------------------
# Obtener el emisor
def get_by_issue(param_list, param_emi, plataforma):
    return [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in param_list
            if row[1] == param_emi and row[2] == plataforma]


# -----------------------------------------------------------------------------------------------------------------------
# retorna datos estadisticos del emisor,mediana,mad
def get_by_data(param_list, data):
    if data == "proporcion":
        return [(row[0], row[3]) for row in param_list]
    if data == "limiteInf":
        return [(row[0], row[5]-row[4]) for row in param_list]
    if data == "limiteSup":
        return [(row[0], row[5]+row[4]) for row in param_list]
    elif data == "mediaMovil":
        return [(row[0], row[5]) for row in param_list]

# -----------------------------------------------------------------------------------------------------------------------
# Obtener los datos estadisticos de un Emisor en Especifico.
def graph_emi(param_list, param_emi, output, plataforma):
    list_em = get_by_issue(param_list, param_emi, plataforma)
    url_output = output + param_emi + plataforma
    date_report = str(list_em[len(list_em) - 1][0])

    prop = get_by_data(list_em, "proporcion")
    limiteInferior = get_by_data(list_em, "limiteInf")
    limiteSuperior = get_by_data(list_em, "limiteSup")
    mediaMovil = get_by_data(list_em, "mediaMovil")

    color = "#BFE2AA"  # Verde
    proporcion = prop[-1][1]
    inf = limiteInferior[-1][1]
    sup = limiteSuperior[-1][1]

    if  proporcion < inf or proporcion > sup:
        color = "#EACF83"  # Amarillo

    list_graph = [prop,limiteSuperior ,limiteInferior, mediaMovil]
    plot_time_series_r(list_graph, "Historico de transacciones con codigo de Respuesta 91 (" + param_emi +" "+plataforma + ")", "% codigos 91",
                       url_output + date_report.replace("-", ""), color)


# -----------------------------------------------------------------------------------------------------------------------
# Plot series Matplotlib
def plot_time_series_r(series, title, ylabel, filename, color_="#F5FFFA"):
    """
    Plots time series data
    :param series: A list of time series, each of them with format [(date,value),(date,value),...(date,value)]
    :param title: A string with the plot's title
    :param ylabel: A string with the Y-axis name
    :param filename: A string with the name of the output file
    :param color_: A string than define the  background of graphic
    :return:
    """
    if len(series) == 0:
        print "Error: serie sin datos"

    # If list has only one series, nest it inside another list
    if not isinstance(series[0], list):
        series = [series]

    fig, ax = plt.subplots()
    # k-black
    #prop, desv_stand, average_mov, average_mov_exp
    formats = ["k-", "r--", "r--", "m:"]
    labels = ["Proporcion de mensajes", "Limite superior", "Limite inferior", "Media movil"]
    for i, s in enumerate(series):
        plt.plot_date(x=[x[0] for x in s], y=[x[1] for x in s], fmt=formats[i], label=labels[i])

    ax.set_xlim(series[0][0][0], series[0][-1][0])

    # The hour locator takes the hour or sequence of hours you want to
    # tick, not the base multiple
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.set_facecolor(color_)
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    fig.autofmt_xdate(rotation=90)
    fig.set_size_inches(16, 6)
    ax.legend(loc='upper left')

    plt.title(title)
    plt.ylabel(ylabel)

    plt.grid(True)
    plt.savefig(filename)
    plt.cla()
    plt.clf()
    plt.close()


# -----------------------------------------------------------------------------------------------------------------------
#*******************************Inicio de ejecucion del Programa********************************************************

list_cod_msg = get_last_rows(dias)
emisorGraficado = []
emi_name = []
plataforma =["ATM","POS"]

print "Iniciando el reporte de transacciones declinadas con codigo 091:"

for exist_emi in listaEmisor:
    if exist_emi in emisorValido:
        for plat_ in plataforma:
            graph_emi(list_cod_msg, exist_emi, rutasalida,plat_)
        emisorGraficado.append(exist_emi)
    else:
        emi_name.append(exist_emi)

print "---------------Salida del programa--------------------------------"

if not len(emisorGraficado) == 0:
    print "--Se genero la grafica de los siguientes emisores:"
    for emisorSuccess in emisorGraficado:
        print "--->" + emisorSuccess

if not len(emi_name) == 0:
    print "--Los siguientes emisores no se graficaron, porque son incorrectos:"
    for emisorInvalido in emi_name:
        print "--->" + emisorInvalido
