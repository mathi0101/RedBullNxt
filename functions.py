from time import time

def turn():
    while raw_input('Enter to repeat: ')=='':
        s=-70
        rueda_l.run(-s)
        #rueda_r.run(s)

    else:
        stop()

def test_light():
    while raw_input('Enter para repeat: ')=='':
        light_f.set_illuminated(True)
        for i in range(5):
            v=light_f.get_lightness()
            print 'Valor de la medida: %s' % v
            sleep(1)
    light_f.set_illuminated(False)

def test_distance(sensor):
    while raw_input('Enter para repeat: ')=='':
        for i in range(5):
            v=sensor.get_sample()
            print 'Valor de la medida: %s' % v
            sleep(1)

def run():
    while raw_input('Enter to repeat: ')=='':
        flag=True
        for i in range(2):
            
            s=127
        
            if flag:
                print 'adelante'
                rueda_l.run(s)
                rueda_r.run(s)
            else:
                print 'atras'
                rueda_l.run(-s)
                rueda_r.run(-s)
            flag= not flag
            sleep(1)
            soltar()
            sleep(0.5)
            
def latency(sensor):
    ''' Calcula el tiempo de latencia del sensor y python'''
    start = time()
    for i in range(100):
        sensor.get_sample()
    stop = time()
    print 'Sensor latency: %s ms' % (1000 * (stop - start) / 100.0)