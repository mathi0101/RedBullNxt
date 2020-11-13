import sys
sys.path.append('modules')
from functions import read_colors_bd,update_bd,write_colors_bd,get_real_color

from modules import init as v

from time import sleep,time


# +--------------- FUNCIONES ---------------+


def idle():
    v.rueda_l.idle()
    v.rueda_r.idle()

def stop():
    v.rueda_l.brake()
    v.rueda_r.brake()

def acelerar(speed=85):
    assert speed>=-128 and speed<=127
    motors=[v.rueda_l,v.rueda_r]
    stop()
    for m in motors:
        m.run(speed)

def girar(izquierda=True,power=70):
    '''Gira el robot hacia un lado infinitamente'''
    assert power>0

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
        stop()
        return

    motL=v.rueda_l
    motR=v.rueda_r

    power=70
    
    time= (abs(grados)*0.7) / 90  # Tiempo para girar x grados
    
    if grados>0:
        motL.run(power)
        motR.run(-power)
    else:
        motL.run(-power)
        motR.run(power)
    
    sleep(time)

    stop()

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

    dist_l=v.dist_l
    dist_f=v.dist_f

    # 1ra parte: Va a buscar un objeto con el sensor de de distancia de la izq

    acelerar()

    distancia_obj_izq=25
    distancia_obj_adelante=25
    while dist_l.get_distance()>=distancia_obj_izq:

        if dist_f.get_distance()<=distancia_obj_adelante:   # Si detecta algo delante
            print 'Tengo algo adelante a %s cm.'%dist_f.get_distance()
            idle()
            sleep(0.3)
            girar_grados(-90)
        else:
            acelerar()
    
    obj_dist=dist_l.get_distance()
    print 'Tengo algo a mi izquierda a %s cm.'%obj_dist
    print 'Girando hacia el objeto'
    girar_grados(-50)

    obj_dist=buscar_girando(obj_dist+10)
    
    print 'Tengo el objeto adelante a %s cm'%obj_dist
    sleep(0.5)
    
    
    real_color=moverYgetColor()
    print real_color
    c=real_color[0]

    print 'Encontrado objeto de color %s.' %c

def buscar_girando(distancia=20):
    '''Empieza a girar a la izquierda hasta encontrar un objeto adelante a
    menos de "distancia" en cm.
    Cuando lo encuentra frena.'''
    sens=v.dist_f
    izquierda=True
    i=0.2
    while True:
        dist=sens.get_distance()
        if dist>=distancia: # Si no detecta nada
            girar(izquierda)
            print 'Giro a la izquierda' if izquierda else 'Giro a la derecha'
            sleep(i)
        else:  # Si lo encontro
            idle()
            sleep(0.1)
            stop()
            dist=sens.get_distance()
            if dist<=distancia:     # Vuelvo a chequear si lo encuentra
                print 'Encontre algo adelante a %s cm.' % dist
                acelerar(64)
                sleep(0.3)
                return dist
            else:
                izquierda= not izquierda
                i+=0.2
                continue
        

        
def moverYgetColor():
    
    sens=v.dist_f
    color= v.color
    colores=read_colors_bd()
    acelerar(64)
    print 'Acercandome al objeto para ver su color...'
    while True:
        if color.get_color()==colores['Negro']:     # mientras detecte negro
            dist=sens.get_distance()
            if dist<=25:
                print 'Distancia %s: acercandome..'%dist
                acelerar(64)
            elif dist==255 :
                stop()
                print 'He perdido el objeto, voy a buscarlo de nuevo'
                buscar_girando(dist)
            else:
                print 'Distancia mayor a 50 cm, retrocediendo...'
                stop()
                acelerar(-64)
                sleep(0.5)
                buscar_girando(dist)
        else:
            stop()

            return get_real_color(color)



def mover_brazo(subir=True):
    mot=v.brazo
    power=64
    if subir:
        mot.run(-power)
        sleep(1)
        mot.idle()
        sleep(0.5)
        mot.brake()
    else:
        mot.run(power)
        sleep(0.55)
        mot.idle()
        sleep(0.55)
        mot.brake()


               


# +----------- RUN ----------------+

def main():


    b=v.initialize_brick_and_consts(False)
    print('Bateria actual: %s mV'% b.get_battery_level())
    idle()
    '''
    flag=True
    while True:
        if len(raw_input())==0:
            #mover_brazo(flag)
            flag= not flag
            for i in range(10):
                print 'Distancia: %s cm'%v.dist_f.get_distance()
        else:
            break'''

    moverYgetColor()


    

    idle()
    print 'Apagando brick con %s mV de bateria.'%b.get_battery_level()













if __name__=='__main__':
    main()