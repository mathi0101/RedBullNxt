

import nxt

from nxt.sensor import Ultrasonic, Color20, Light
from nxt.sensor import PORT_1,PORT_2,PORT_3,PORT_4

from nxt.motor import Motor
from nxt.motor import PORT_A, PORT_B, PORT_C

from time import sleep,time

#nxt.locator.make_config()
b=nxt.locator.find_one_brick(debug=True)
b.play_tone_and_wait(440.0, 1000) # Hace sonar el brick 1 segundo para verificar la conexion

# +-------- SENSORES Y SU UBICACION SEGUN LA VISTA DEL ROBOT --------+
dist_f=Ultrasonic(b,PORT_3)
dist_l=Ultrasonic(b,PORT_4)

color_f=Color20(b,PORT_1)

light_f=Light(b, PORT_2)

rueda_l=Motor(b, PORT_C)
rueda_r=Motor(b, PORT_A)

#motor_EXTRA=Motor(b, PORT_B)

#Ultrasonic sensor latency test

start = time()
for i in range(100):
    dist_f.get_sample()
stop = time()
print 'ultrasonic latency: %s ms' % (1000 * (stop - start) / 100.0)

input()

for i in range(5):
    v=dist_f.get_distance()
    print f'Distancia del sensor: {v}'
    sleep(1)