from time import time,sleep

#b.play_sound_file(False,'blue.rso') # Brick play sound file

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

def test_sensor(sensor):
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



def test_color():
    while raw_input('Enter para repeat: ')=='':
        col=color.get_color()
        col_light=color.set_light_color(0)
        #refl_col=color.get_reflected_light(20)
        print 'Color: %s' % col
        print 'Color luz: %s' % col_light
        #print 'Color luz reflejada: %s' % refl_col



def get_dict_colors():
    colores={}
    user_input=None
    i=0
    while user_input!='stop':
        color.set_light_color(i)
        user_input=raw_input('Color: ')
        if user_input!='':
            colores[i]=user_input
        elif user_input.lower()=='stop':
            pass

        i+=1

    return colores

def update_text(dic):
    PATH=  'bd/colors.txt'
    old_dic=read_colors_bd(PATH)
    mix_dic={}
    

def write_colors_bd(path,dic):
    #dic={'Negro':4,'Blanco':7}
    dic={}
    with open(path,'w') as f:
        l=[]
        for k,v in dic.items():
            l.append(k+','+str(v)+'\n')
        f.writelines(l)
    
def read_colors_bd(path):

    try:
        with open(path, 'r') as f:
            doc=f.readlines()
            if doc==[]:
                return None
            dic={}
            for i,line in enumerate(doc):
                if ',' not in line:
                    raise Exception('Imposible leer linea numero: {} en {} '.format(i,path))
                items=line.replace('\n','').split(',')
                dic[items[0].strip()]=int(items[1].strip())
            
        return dic



    except IOError:
        print 'Se ha creado un nuevo archivo colors.txt en "%s"' %path
        with open(path, 'w') as f:
            f.write('')

def calibrate_colors():
    dic={}
    user_input=None
    while user_input!='':
        user_input=raw_input('Coloca el objeto adelante del sensor y dime su color: ')
        if user_input!='':
            c=color.get_color()
            dic[user_input.capitalize()]=c
            print 'Valor obtenido: %s' % c

        

    return dic

