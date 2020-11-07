
from functions import *
import nxt

from nxt.sensor import Ultrasonic, Color20, Light
from nxt.sensor import PORT_1,PORT_2,PORT_3,PORT_4

from nxt.motor import Motor
from nxt.motor import PORT_A, PORT_B, PORT_C

from time import sleep,time

#nxt.locator.make_config()
b=nxt.locator.find_one_brick(debug=True)
b.play_tone_and_wait(440.0, 1000) # Hace sonar el brick 1 segundo para verificar la conexion

b.play_sound_file(False,'blue.rso')

# +-------- SENSORES Y SU UBICACION SEGUN LA VISTA DEL ROBOT --------+
dist_f=Ultrasonic(b,PORT_3)
dist_l=Ultrasonic(b,PORT_4)

color=Color20(b,PORT_1)

light=Light(b, PORT_2)

rueda_l=Motor(b, PORT_C)
rueda_r=Motor(b, PORT_A)

#motor_EXTRA=Motor(b, PORT_B)



def soltar():
    rueda_l.idle()
    rueda_r.idle()

def frenar():
    rueda_l.brake()
    rueda_r.brake()

latency(light)