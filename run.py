
from functions import *

'''from initialize import initialize_brick_and_consts
from initialize import b,rueda_l,rueda_r,light,color,dist_f,dis'''
import init as v

from time import sleep,time


# +--------------- FUNCIONES ---------------+


def soltar():
    v.rueda_l.idle()
    v.rueda_r.idle()

def frenar():
    v.rueda_l.brake()
    v.rueda_r.brake()



# +----------- RUN ----------------+

def main():
    PATH=  'bd/colors.txt'

    x=read_colors_bd(PATH,True)
    print x

    #v.initialize_brick_and_consts()



main()


