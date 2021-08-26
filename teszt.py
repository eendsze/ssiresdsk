import math
import random
import pygame as pg

pg.init()
clock = pg.time.Clock()
a = 0.0
fps = 60
dt = 1/fps
amp = 1.0
freq = 0.05

for x in range(10000):
    a += random.uniform(-dt*amp, dt*amp)
    a = a*(1-dt*freq)
    print(a)
    clock.tick(fps)


