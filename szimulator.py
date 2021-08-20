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


#ez egy komment
def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    hajo = hajomegjelenito.HajoObject(screen)
    joy = joystick.myJoystic()
    valosModell = fizikaimodell.physicalShip()

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.JOYBUTTONDOWN:
                joy.readOffset()
 
        joy.read()
        valosModell.calculate(dt, [joy.y*10, joy.x*10, joy.z])
        hajo.setPosition(valosModell.X)
        hajo.draw()
        #hajo.setspeed(joy.x*10.0, joy.y*10.0, joy.z)
        #hajo.move(fps)

        pg.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
