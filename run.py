import sys
sys.path.append('modules')
from functions import *
from functions import read_colors_bd,update_bd,write_colors_bd,get_real_color,latency,calibrate_colors,calibar_valor_medio,test

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
    stop()
    if izquierda:
        v.rueda_l.run(-power)
        v.rueda_r.run(power)
    else:
        v.rueda_l.run(power)
        v.rueda_r.run(-power)
    print 'Giro a la izquierda' if izquierda else 'Giro a la derecha'

def girar_grados(grados=90):
    '''
    Gira el robot x grados:
    grados>0 Sentido horario
    grados<0 sentido antihorario
    
    0.61 seconds a 75 power = 90 grados
    1.22 seconds a 75 power = 180 grados
    '''
    stop()

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
    
    print 'Girando %s grados'%abs(grados) ,'hacia la izquierda.' if grados<0 else 'hacia la derecha.'
    sleep(time)

    stop()



def buscar_girando(distancia_objetivo=25):
    '''Empieza a girar hacia los costados hasta encontrar el objeto.'''
    sens=v.dist_f
    hacia_izquierda=True
    turn_time=0.2      # En segundos, tiempo que va a girar el robot hacia cada lado. Este va a ir subiendo en 0.5 segundos
    flag= True 
    double_test=True
    print 'Objetivo < %s'%distancia_objetivo

    girar(hacia_izquierda)  # Empieza a girar hacia la izquierda

    start=time()
    while flag:
        dist=sens.get_distance()
        if dist <= distancia_objetivo:
            print 'Encontre algo adelante a %s cm'%dist
            stop()
            if double_test:       # Volviendo a chequear por las dudas
                double_test=False
                sleep(0.2)

            else:           # Ya chequee 2 veces y estoy adelante del objeto
                flag=False
                print 'Lo sigo teniendo adelante a %s cm'%dist
        
        else:
            double_test=True
            conteo=time()-start # Tiempo desde que empieza a girar hacia un lado hasta cada vez que se prueba
            if conteo >= turn_time:     # Si ya paso el tiempo se empieza a girar para el otro lado y se suma el tiempo
                turn_time+=0.2
                hacia_izquierda= not hacia_izquierda
                girar(hacia_izquierda,75)  # Empieza a girar hacia un lado
                start=time()
    else:       
        return dist


def moverYgetColor():
    
    sens=v.dist_f
    color= v.color
    colores=read_colors_bd()
    acelerar(64)
    anterior=None
    print 'Acercandome al objeto para ver su color...'

    negro=colores['Negro']
    while True:
        if color.get_color()==negro:     # mientras detecte negro
            dist=sens.get_distance()
            

            if dist<=30:
                print 'Distancia %s cm. Acercandome lento...'%dist
                acelerar(64)
                anterior=dist
            elif dist<=50:
                print 'Esta lejos a %s cm. Voy rapido'%dist
                acelerar(80)
                anterior=dist

            elif dist>50 :
                stop()
                print 'He perdido el objeto, voy a buscarlo de nuevo'
                buscar_girando(anterior+10 if anterior!=None else 50)

        else:
            stop()
            break

    stop()
    sleep(0.3)
    if color.get_color()!=negro:
        c=get_real_color(color)
        print 'Encontre el color: %s'%c[0]
        return c
    else:
        print 'Vuelvo a ejecutar moverygetcolor'
        return moverYgetColor()



def mover_brazo(subir=True):
    ''' Sube y baja el brazo para trabar la pelota.
    type(subir)= bool '''
    mot=v.brazo
    power=70
    if subir:
        mot.run(-power)
        sleep(1)
        mot.idle()
    else:
        mot.run(power)
        sleep(0.6)
        mot.idle()
    sleep(0.6)
    mot.brake()
    print 'Se ha subido el brazo.' if subir else 'Se ha bajado el brazo.'
               

def arrastrar_afuera():
    '''
    Arrastra la pelota hasta que detecte blanco en el sensor de grises
    Luego la suelta y vuelve hacia atras'''

    luz=v.light
    valor_medio=read_colors_bd(False,False)

    acelerar(80)
    while luz.get_lightness()>=valor_medio:
        pass
    
    else:
        stop()
        mover_brazo(True)
        acelerar(-80)
        sleep(0.3)
        girar_grados(-170)
        acelerar()

def turn_off_brick(brick):
    idle()
    mover_brazo()
    print 'Desconectando brick con %s mV de bateria.'%brick.get_battery_level()
    

# ------------ FUNCIONES PRINCIPALES -------------

def categoria_avanzada():
    '''
    Inicializa las variables necesarias para buscar pelotas azules y naranjas.
    Luego empieza a moverse dentro de un circulo negro buscando pelotas y cubos.
    Cuando encuentra alguna
    '''

    dist_l=v.dist_l
    dist_f=v.dist_f
    luz=v.light

    luz.set_illuminated(True)  # Enciende la luz de abajo y espera un poco
    sleep(0.5)

    print 'TRANSFORMANDO ROBOT EN ABEJA POLINIZADORA'
    

    # Colores con los que tiene que interactuar el robot
    COLORES_PELOTAS=['Azul','Naranja']
    COLORES_CUBOS=['Rojo','Verde']
    COLORES_OBJETIVO=COLORES_PELOTAS + COLORES_CUBOS

    colores_bd=read_colors_bd(True)  # {color_id : color_name}
    colores_bd_names=read_colors_bd() # {color_name : color_id}
    valor_medio=read_colors_bd(False,False)     # int

    # Distancias objetivo
    distancia_obj_izq=35
    distancia_obj_adelante=25

    # CONTADOR DE PELOTAS AGARRADAS
    PELOTAS_AFUERA=0
    PELOTAS_EN_PANAL=0


    flag= True

    acelerar(80)
    while flag:

        gray_value=luz.get_lightness()
        if gray_value<=290:
            stop()
            break
        if gray_value >= valor_medio:
            # Si estamos arriba de BLANCO ->    >=
            # Si estamos arriba de NEGRO ->     <=
            #acelerar(80)

            if dist_l.get_distance()<= distancia_obj_izq:
                stop()
                x=dist_l.get_distance()
                print 'Encontre algo a mi izquierda a %s cm'%x
                girar_grados(-50)
                distancia_obj_adelante=buscar_girando(x+10)+5

            if dist_f.get_distance()<= distancia_obj_adelante:
                color_tuple=moverYgetColor()
                name_color='Azul'      #color_tuple[0]

                print 'Objeto de color %s'%name_color

                if name_color in COLORES_OBJETIVO:
                    stop()
                    if name_color in COLORES_CUBOS:
                        if name_color=='Rojo':
                            pass
                        if name_color=='Verde':
                            pass
                    elif name_color in COLORES_PELOTAS:
                        # Agarrar 
                        mover_brazo(False)
                        if name_color=='Azul':
                            # llevar hacia afuera
                            arrastrar_afuera()
                            PELOTAS_AFUERA+=1
                        if name_color=='Naranja':
                            pass

                else:   
                    # Si es un color que queremos esquivar
                    print 'Esquivando objeto.'
                    acelerar(-84)
                    sleep(0.3)
                    girar_grados(-90)
                    acelerar(80)



        else:
            stop()
            sleep(0.2)
            acelerar(-84)
            sleep(0.3)
            girar_grados(-90)
            acelerar(80)

    





    
# +----------- RUN ----------------+

def main():


    b=v.initialize_brick_and_consts(False)
    stop()
    mover_brazo(True)
    #calibar_valor_medio(v.light)
    #categoria_avanzada()

    test(v.dist_f)
    
    




    turn_off_brick(b)







if __name__=='__main__':
    main()