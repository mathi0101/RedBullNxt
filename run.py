
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

def acelerar(speed=100):
    assert speed>=-127 and speed<=127
    motors=[v.rueda_l,v.rueda_r]
    for m in motors:
        m.run(speed)


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


    mot_l=v.rueda_l
    mot_r=v.rueda_r

    dist_l=v.dist_l
    dist_f=v.dist_f

    color=v.color

    # 1ra parte: Va a buscar un objeto con el sensor de de distancia de la izq

    distancia_obj=20


    while dist_l.get_distance()>=distancia_obj:
        mot_l.
        


# +----------- RUN ----------------+

def main():

    #v.initialize_brick_and_consts()
    x=get_real_color(v.color)

    print 'El color es %s' %x


main()


