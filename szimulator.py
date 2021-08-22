#!/usr/bin/env python

import os
import math
import pygame as pg
import hajomegjelenito
import joystick
import fizikaimodell

fps = 60
dt = 1.0/fps
main_dir = os.path.split(os.path.abspath(__file__))[0]

#kis hajo
# m11, m22, m33
#M = [2.0, 4.4, 0.04]
# csillapitas
#D = [2.7, 13.4, 0.156]
#Af = [1.7, 1.8, 1.6]
Hajomodell1 = {
    "M": [2.0, 4.4, 0.04],
    "D": [2.7, 13.4, 0.156],
    "Af": [1.7, 1.8, 1.6],
    "length": 0.4,
    "zoom": 100
}

Nagyhajo445 = {
    #"M": [12600, 28900, 170000],
    "M": [12600, 18000, 170000],
    "D": [200, 2000, 200000],
    "Af": [1.7, 2.0, 1.6],
    "length": 13,
    "zoom": 50
}


#ez egy komment
def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    hajo = hajomegjelenito.HajoObject(screen, Nagyhajo445)
    joy = joystick.myJoystic()
    valosModell = fizikaimodell.physicalShip(Nagyhajo445)

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.JOYBUTTONDOWN:
                joy.readOffset()
 
        joy.read()
        # a hajo koordinatarendszereben: elore x, balra van a +y, balra +forg
        valosModell.calculate(dt, [joy.elore*4000, joy.jobbra*-2000, joy.forg*30000])
        hajo.setPosition(valosModell.X)
        hajo.setspeed(valosModell.V)
        hajo.draw()
        #hajo.setspeed(joy.x*10.0, joy.y*10.0, joy.z)
        #hajo.move(fps)

        pg.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
