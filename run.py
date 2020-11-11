
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

def acelerar(speed=85):
    assert speed>=-128 and speed<=127
    motors=[v.rueda_l,v.rueda_r]
    for m in motors:
        m.run(speed)

def girar(izquierda=True):
    '''Gira el robot hacia un lado infinitamente'''

    power=70

    if izquierda:
        v.rueda_l.run(-power)
        v.rueda_r.run(power)
    else:
        v.rueda_l.run(power)
        v.rueda_r.run(-power)

def girar_grados(grados=90):
    '''
    Gira el robot x grados:
    grados>0 Sentido horario
    grados<0 sentido antihorario
    
    0.61 seconds a 75 power = 90 grados
    1.22 seconds a 75 power = 180 grados
    '''
    if grados==0:
        frenar()
        return

    motL=v.rueda_l
    motR=v.rueda_r

    power=75
    
    time= (abs(grados)*0.61) / 90  # Tiempo para girar x grados
    
    if grados>0:
        motL.run(power)
        motR.run(-power)
    else:
        motL.run(-power)
        motR.run(power)
    
    sleep(time)

    frenar()

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

    acelerar()

    distancia_obj_izq=25
    distancia_obj_adelante=30
    while dist_l.get_distance()>=distancia_obj_izq:

        if dist_f.get_distance()<=distancia_obj_adelante:   # Si detecta algo delante
            print 'Tengo algo adelante a %s cm.'%dist_f.get_distance()
            soltar()
            sleep(0.3)
            girar_grados(-95)
        else:
            acelerar()
    
    else:
        obj_dist=dist_l.get_distance()
        print 'Tengo algo a mi izquierda a %s cm.'%obj_dist
        print 'Girando hacia el objeto'
        girar_grados(-50)

        girar(True)
        while True:
            if dist_f.get_distance()<=obj_dist+5:
                frenar()       # Tengo el objeto delante
                break
        
        print 'Tengo el objeto adelante a %s cm'%dist_f.get_distance()
        sleep(0.5)
        acelerar(65)
        while dist_f.get_distance()>=10:
            print 'Tengo el objeto adelante a %s cm'%dist_f.get_distance()
            if dist_f.get_distance()>=20:
                break
        
        c='s'
        while c!='Negro':
            real_color=moverYgetColor()
            c=real_color[0]

        else:
            print 'Encontrado objeto de color %s.' %c

        
        
def moverYgetColor():


    color= v.color
    colores=read_colors_bd()
    acelerar(65)
    while color.get_color()==colores['Negro']:
        pass
    else:
        frenar()

    return get_real_color(color)




               


# +----------- RUN ----------------+

def main():


    v.initialize_brick_and_consts(False)
    frenar()
    print v.dist_f.get_distance()
    #buscarYgetColor()
    girar(False)
    raw_input()
    frenar()


main()



