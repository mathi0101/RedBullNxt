from time import time,sleep

#b.play_sound_file(False,'blue.rso') # Brick play sound file

def test_light():
    while raw_input('Enter para repeat: ')=='':
        light_f.set_illuminated(True)
        for i in range(5):
            v=light_f.get_lightness()
            print 'Valor de la medida: %s' % v
            sleep(1)
    light_f.set_illuminated(False)


def test_sensor(sensor):
    while raw_input('Enter para repeat: ')=='':
        for i in range(5):
            v=sensor.get_sample()
            print 'Valor de la medida: %s' % v
            sleep(1)

            
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



def update_bd(dic):
    '''Lee la base de datos y la actualiza con el nuevo dic'''
    PATH=  'bd/colors.txt'

    old_dic=read_colors_bd(PATH)
    mix_dic=old_dic.copy()

    update_mode=2
    # 0 -> Sobreescribir 
    # 1 -> Conservar antiguo valor 
    # 2 -> Preguntar


    for key in dic.keys():
        if key not in old_dic.keys():
            mix_dic[key]=dic[key]
        elif old_dic[key]!=dic[key]:
            print 'Se han encontrado 2 valores distintos para el color {}.'.format(key)
            print 'Valor antiguo: %s'%old_dic[key]
            print 'Valor nuevo: %s'%dic[key]
            if update_mode==0:
                print 'Asignando valor nuevo al color %s' %key
                mix_dic[key]=dic[key]
            elif update_mode==1:
                print 'Omitiendo nuevo valor.'
            else:
                flag= True
                while flag:
                    print 'Selecciona una opcion del menu:\n'
                    print '1- Sobreescribir valor: {} -> {}'.format(key, dic[key])
                    print '2- Conservar antiguo valor: {} -> {} \n'.format(key, old_dic[key])
                    user_input=raw_input('Opcion: ')
                    try:
                        user_input=int(user_input)
                    except ValueError:
                        print 'OPCION INVALIDA'
                        continue
                    if user_input==1:
                        print 'Asignando valor nuevo al color %s' %key
                        mix_dic[key]=dic[key]
                        flag=False
                    elif user_input==2:
                        print 'Omitiendo nuevo valor.'
                        flag=False
                    else:
                        print 'OPCION INVALIDA'
                        continue
    
    write_colors_bd(PATH,mix_dic)

def write_colors_bd(path,dic):
    #dic={'Negro':4,'Blanco':7}
    with open(path,'w') as f:
        l=[]
        for k,v in dic.items():
            l.append(k+','+str(v)+'\n')
        f.writelines(l)
    
def read_colors_bd(path,reverse=False):
    '''
    reverse=True
        {color_id : color_name}
    reverse=False
        {color_name : color_id}
    '''
    try:
        with open(path, 'r') as f:
            doc=f.readlines()
            if doc==[]:
                return {}
            dic={}
            for i,line in enumerate(doc):
                if ',' not in line:
                    raise Exception('Imposible leer linea numero: {} en {} '.format(i,path))
                items=line.replace('\n','').split(',')
                if reverse:
                    dic[int(items[1].strip())]=items[0].strip()
                else:
                    dic[items[0].strip()]=int(items[1].strip())
            
        return dic



    except IOError:
        print 'Se ha creado un nuevo archivo colors.txt en "%s"' %path
        with open(path, 'w') as f:
            f.write('')


def calibrate_colors(sensor):
    dic={}
    user_input=None
    while user_input!='':
        user_input=raw_input('Coloca el objeto adelante del sensor y dime su color: ')
        if user_input!='':
            c=sensor.get_color()
            dic[user_input.capitalize()]=c
            print 'Valor obtenido: %s' % c

    update_bd(dic)

def get_color_in_db(color_id):
    PATH=  'bd/colors.txt'
    colors=read_colors_bd(PATH,True)
    if color_id in colors.keys():
        return colors[color_id]
    else:
        print 'Se ha detectado un nuevo color con id: %s'% color_id
        print 'Se agregara este color a la base de datos.'
        color_user=raw_input('Que color es? -> ').capitalize()
        write_colors_bd(PATH,{color_user:color_id})
        return color_user

def get_real_color(sens):
    '''
    Realiza varias mediciones en cierto tiempo para 
    obtener la mejor lectura del color '''

    print 'Tomando valores...'

    valores=[]
    for i in range(5):
        v=sens.get_color()
        valores.append(int(v))
        sleep(0.2)
    
    dic={}
    for v in valores:
        qty=valores.count(v)
        dic[qty]=v

    max_v=max(dic.keys())
    colorid=dic[max_v]

    return get_color_in_db(colorid)
    


    