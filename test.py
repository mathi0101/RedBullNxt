

import nxt
#import nxt.usbsock
from nxt.sensor import *
from time import sleep,time

#nxt.locator.make_config()
b=nxt.locator.find_one_brick(debug=True)
b.play_tone_and_wait(440.0, 100) # Hace sonar el brick para verificar la conexion



#Ultrasonic sensor latency test
ultrasonic = Ultrasonic(b, PORT_4)
start = time()
for i in range(100):
    ultrasonic.get_sample()
stop = time()
print 'ultrasonic latency: %s ms' % (1000 * (stop - start) / 100.0)

