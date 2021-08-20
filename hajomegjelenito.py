import math
import pygame as pg

WHITE = (255, 255, 255)
BACKGND = (0, 0, 0)
LAWNGREEN = (0, 223, 0)

class HajoObject:
    #hajo meretek, [m]
    length = 13.64
    width = 4.1
    #skalazas a keperenyore m->pixel
    scr_scale = 10.0
    #hajo pozicioja, [m, rad]
    position = pg.math.Vector2(0.0,0.0)
    rotation = 0.0
    #hajo sebessege [m/s, rad/s]
    speed = pg.math.Vector2(0.0,4.2)
    szogseb = 0.2
    #relativ pozicio a megjeleniteshez
    midscreen = pg.math.Vector2(0,0)
    #hajo pontjai, [m]. Ezt atalakitjuk vektorokka a konstrutorban, azt lehet hasznalni
    hajoPoly = [(0, 6.82), (-1.35, 5.42), (-2.05, 0), (-2.05, -6.82),  (2.05, -6.82), (2.05, 0), (1.35, 5.42)]
    #elozo kirajzolt polygon a torleshez
    lastPoly = [(0,0), (0,0), (0,0)]

    def __init__(self, scr) -> None:
        self.screen = scr
        self.midscreen = pg.math.Vector2(scr.get_width() / 2, scr.get_height() / 2)
        self.hajoVect = list(map(lambda x: pg.math.Vector2(x), self.hajoPoly))

    def draw(self, color=WHITE):
        #elozo torlese
        pg.draw.polygon(self.screen, BACKGND, self.lastPoly)
        #uj pozicio szamitasa
        #forgatas, poziciora mozgatas, aztan skalazas:
        shipmap = map(lambda x: (x.rotate_rad(self.rotation) + self.position) * self.scr_scale, self.hajoVect)
        #flippelni kell lefele, es betenni a kepernyo kozepere
        self.lastPoly = list(map(lambda x: (x.x + self.midscreen.x, self.midscreen.y - x.y), shipmap))
        #uj pligon rajzolasa      
        pg.draw.polygon(self.screen, color, self.lastPoly)

    def move(self, fps):
        self.position += (self.speed / fps)
        self.rotation += (self.szogseb / fps)
