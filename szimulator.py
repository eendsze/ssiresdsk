#!/usr/bin/env python

import os
import math
import pygame as pg
import hajomegjelenito as hm
import joystick

fps = 100
main_dir = os.path.split(os.path.abspath(__file__))[0]


#ez egy komment
def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    hajo = hm.HajoObject(screen)
    joy = joystick.myJoystic()

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.JOYBUTTONDOWN:
                joy.readOffset()
 
        hajo.draw()
        joy.read()
        hajo.setspeed(joy.x*10.0, joy.y*10.0, joy.z)
        hajo.move(fps)

        pg.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
