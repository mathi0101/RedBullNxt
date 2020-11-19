from modules import init as v

def stop():
    v.initialize_brick_and_consts(False)

    x=[v.rueda_l,v.rueda_r,v.brazo]

    for mot in x:
        mot.brake()


if __name__=='__main__':
    stop()
