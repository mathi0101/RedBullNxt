import nxt

from nxt.sensor import Ultrasonic, Color20, Light
from nxt.sensor import PORT_1,PORT_2,PORT_3,PORT_4

from nxt.motor import Motor
from nxt.motor import PORT_A, PORT_B, PORT_C

from nxt.system import get_device_info,get_firmware_version




def initialize_brick_and_consts(make_sound=True):

    #nxt.locator.make_config()
    b=nxt.locator.find_one_brick()
    if make_sound:
        b.play_tone_and_wait(440.0, 1000) # Hace sonar el brick 1 segundo para verificar la conexion
    print 'Se ha conectado al brick exitosamente.'
    print('Bateria actual: %s mV'% b.get_battery_level())

    # +-------- SENSORES Y SU UBICACION SEGUN LA VISTA DEL ROBOT --------+
    global dist_f
    dist_f=Ultrasonic(b,PORT_3)  # Distancia frontal
    global dist_l
    dist_l=Ultrasonic(b,PORT_4)  # Distancia izquierda

    global color
    color=Color20(b,PORT_1)     # Sensor de color

    global light
    light=Light(b, PORT_2)      # Sensor de grises

    global rueda_l
    rueda_l=Motor(b, PORT_C)    # Motor izquierdo
    global rueda_r
    rueda_r=Motor(b, PORT_A)    # Motor derecho

    global brazo
    brazo=Motor(b, PORT_B)      # Brazo compuerta

    return b

