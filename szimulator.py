#!/usr/bin/env python

import os
import math
import pygame as pg
import hajomegjelenito as hm

fps = 100
main_dir = os.path.split(os.path.abspath(__file__))[0]


#ez egy komment
def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    hajo = hm.HajoObject(screen)

    while 1:
        for event in pg.event.get():
            if event.type in (pg.QUIT, pg.CONTROLLER_BUTTON_B):
                return
            if event.type == pg.KEYDOWN:
                hajo.move()

        hajo.draw()
        hajo.move(fps)

        pg.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
