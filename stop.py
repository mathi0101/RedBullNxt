from modules import init as v

v.initialize_brick_and_consts(False)

x=[v.rueda_l,v.rueda_r,v.brazo]

for mot in x:
    mot.brake()

