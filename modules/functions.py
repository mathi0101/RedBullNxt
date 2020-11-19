from time import time,sleep

from nxt.sensor import *

#b.play_sound_file(False,'blue.rso') # Brick play sound file

            
def latency(sensor):
    ''' Calcula el tiempo de latencia del sensor y python'''
    start = time()
    for i in range(100):
        sensor.get_sample()
    stop = time()
    print 'Sensor latency: %s ms' % (1000 * (stop - start) / 100.0)


def test(sens):
    while len(raw_input('Enter para testear sensor %s'%sens))==0:
        for i in range(10):
            print sens.get_sample()
            sleep(0.5)

def promedio(values):
    largo=len(values)
    suma=sum(values)
    return suma/largo

def calibar_valor_medio(sens):
    sens.set_illuminated(True)
    raw_input('Coloque el sensor en color BLANCO y presione Enter ')
    blanco=[]
    for i in range(5):
        x=sens.get_sample()
        print x
        blanco.append(x)
        sleep(0.2)

    col_blanco=promedio(blanco)
    raw_input('Coloque el sensor en color NEGRO y presione Enter ')
    negro=[]
    for i in range(5):
        x=sens.get_sample()
        print x
        negro.append(x)
        sleep(0.2)

    sens.set_illuminated(False)
    col_negro=promedio(negro)

    valor_medio=promedio([col_blanco,col_negro])
    print 'Valor medio calculado: %s'%valor_medio

    write_colors_bd({'medio':valor_medio},False)


def update_bd(dic,to_colors=True):
    '''Lee la base de datos y la actualiza con el nuevo dic'''

    old_dic=read_colors_bd(False,to_colors)
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

    write_colors_bd(mix_dic,to_colors)

def write_colors_bd(dic,to_colors=True):
    #dic={'Negro':4,'Blanco':7}
    path= 'bd/colors.txt' if to_colors else 'bd/middle_value.txt'
    with open(path,'w') as f:
        l=[]
        for k,v in dic.items():
            l.append(k+','+str(v)+'\n')
        f.writelines(l)
    
def read_colors_bd(reverse=False,to_colors=True):
    '''
    reverse=True
        {color_id : color_name}
    reverse=False
        {color_name : color_id}
    '''
    path='bd/colors.txt' if to_colors else 'bd/middle_value.txt'
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
            
        return dic if to_colors else dic['medio']



    except IOError:
        print 'Se ha creado un nuevo archivo .txt en "%s"' %path
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
            print 'Asignando valor {} al color "{}".'.format(c,user_input.capitalize())

    update_bd(dic)

def get_color_in_db(color_id):
    colors=read_colors_bd(True)
    if color_id in colors.keys():
        return colors[color_id]
    else:
        print 'Se ha detectado un nuevo color con id: %s'% color_id
        print 'Quieres agregar este color a la base de datos? '
        color_user=raw_input('Ingresa el color o pulsa Enter para omitr -> ').capitalize()
        if len(color_user)>1:
            update_bd({color_user:color_id})
            return color_user
        else:
            return 'None Color'

def get_real_color(sens):
    '''
    Realiza varias mediciones en cierto tiempo para 
    obtener la mejor lectura del color '''

    print 'Calculando color...'

    ids={}
    #{color_id: qty}
    for i in range(30):
        color_id=sens.get_color()
        if color_id not in ids:
            ids[color_id]=1
        else:
            qty=ids[color_id]
            ids[color_id]=qty+1
        sleep(0.1)

    values=ids.values()
    max_=max(values)

    for id in ids:
        if ids[id]==max_:
            return get_color_in_db(id),id



if __name__=='__main__':
    pass