
from functions import *
import nxt

from nxt.sensor import Ultrasonic, Color20, Light
from nxt.sensor import PORT_1,PORT_2,PORT_3,PORT_4

from nxt.motor import Motor
from nxt.motor import PORT_A, PORT_B, PORT_C

from time import sleep,time

def get_brick():
    #nxt.locator.make_config()
    brick=nxt.locator.find_one_brick(debug=True)
    brick.play_tone_and_wait(440.0, 1000) # Hace sonar el brick 1 segundo para verificar la conexion
    print 'Se ha conectado al brick exitosamente.'
    return brick



# +--------------- FUNCIONES ---------------+


def soltar():
    rueda_l.idle()
    rueda_r.idle()

def frenar():
    rueda_l.brake()
    rueda_r.brake()

# +----------- RUN ----------------+

def main():

    b=get_brick()

    PATH=  'bd/colors.txt'
    
    # +-------- SENSORES Y SU UBICACION SEGUN LA VISTA DEL ROBOT --------+
    dist_f=Ultrasonic(b,PORT_3)  # Distancia frontal
    dist_l=Ultrasonic(b,PORT_4)  # Distancia izquierda

    color=Color20(b,PORT_1)     # Sensor de color

    light=Light(b, PORT_2)      # Sensor de grises

    rueda_l=Motor(b, PORT_C)    # Motor izquierdo
    rueda_r=Motor(b, PORT_A)    # Motor derecho
    #motor_EXTRA=Motor(b, PORT_B)
    # +-------- SENSORES Y SU UBICACION SEGUN LA VISTA DEL ROBOT --------+


    read_colors_bd(PATH)








main()


