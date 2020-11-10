
from functions import *

import init as v

from time import sleep,time


# +--------------- FUNCIONES ---------------+


def soltar():
    v.rueda_l.idle()
    v.rueda_r.idle()

def frenar():
    v.rueda_l.brake()
    v.rueda_r.brake()

def buscarYgetColor():
    '''
    Esta funcion mueve el robot hacia adelante hasta que encuentra algun objeto a su izquierda o adelante.
    Adelante:
        Gira 180 grados hacia izq y continua buscando
    Izquierda:
        Detecta un objeto y va a buscarlo.

    Cuando lo encuentra se empieza a acercar hasta que el sensor de color detecta un color. En este momento
    se frena hasta que detecte bien el color y luego lo devuelve.
    Aca termina el codigo '''

    

# +----------- RUN ----------------+

def main():
    PATH=  'bd/colors.txt'

    colors=read_colors_bd(PATH,True)

    #v.initialize_brick_and_consts()



main()


