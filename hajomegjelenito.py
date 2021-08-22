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
    #scr_scale = 100.0
    #hajo tenyleges merete (a modell 1m hosszu)
    #ship_scale = 0.4
    #hajo pozicioja, [m, rad]
    position = pg.math.Vector2(0.0,0.0)
    rotation = 0.0
    #hajo sebessege [m/s, rad/s]
    vx = 0
    vy = 0
    szogseb = 0.0
    #relativ pozicio a megjeleniteshez
    midscreen = pg.math.Vector2(0,0)
    #hajo pontjai, [m]. Ezt atalakitjuk vektorokka a konstrutorban, azt lehet hasznalni
#    hajoPoly = [(0, 6.82), (-1.35, 5.42), (-2.05, 0), (-2.05, -6.82),  (2.05, -6.82), (2.05, 0), (1.35, 5.42)]
    hajoPoly = [(0.5, 0), (0.4, -0.1), (0, -0.15), (-0.5, -0.15),  (-0.5, 0.15), (0, 0.15), (0.4, 0.1)]
    #elozo kirajzolt polygon a torleshez
    lastPoly = [(0,0), (0,0), (0,0)]
    lastSpeedVect = [pg.math.Vector2(0,0), pg.math.Vector2(0,0)]

    def __init__(self, scr, dict) -> None:
        self.screen = scr
        self.ship_scale = dict["length"]
        self.scr_scale = dict["zoom"]
        self.midscreen = pg.math.Vector2(scr.get_width() / 2, scr.get_height() / 2)
        self.hajoVect = list(map(lambda x: pg.math.Vector2(x), self.hajoPoly))
        if pg.font:
            self.font = pg.font.Font(None, 24)
            text = self.font.render("Ez csak egyszer lesz kiírva. Ő", 1, WHITE)
            scr.blit(text, (10, 10))

    def draw(self, color=WHITE):
        #elozo torlese
        pg.draw.polygon(self.screen, BACKGND, self.lastPoly)
        pg.draw.line(self.screen, BACKGND, self.lastSpeedVect[0], self.lastSpeedVect[1], width = 3)
        #uj pozicio szamitasa
        #forgatas es skalazas a valos meretre, poziciora mozgatas, aztan skalazas:
        shipmap = map(lambda x: (x.rotate_rad(self.rotation) * self.ship_scale + self.position) * self.scr_scale, self.hajoVect)
        speedVect = pg.math.Vector2(self.vx, self.vy).rotate_rad(self.rotation)
        self.lastSpeedVect[0] = self.position*self.scr_scale
        self.lastSpeedVect[1] = (self.position+speedVect)*self.scr_scale
        #flippelni kell lefele, es betenni a kepernyo kozepere
        self.lastPoly = list(map(lambda x: (x.x + self.midscreen.x, self.midscreen.y - x.y), shipmap))
        self.lastSpeedVect = list(map(lambda x: (x.x + self.midscreen.x, self.midscreen.y - x.y), self.lastSpeedVect))
        # uj rajzolas
        pg.draw.polygon(self.screen, color, self.lastPoly)
        pg.draw.line(self.screen, LAWNGREEN, self.lastSpeedVect[0], self.lastSpeedVect[1], width = 3)
        # texts
        text = self.font.render(f"Pos x: {self.position[0]:3.2f}, y: {self.position[1]:3.2f}. Speed: Vx: {self.vx:3.2f} [m/s], \
            Vy: {self.vy:3.2f} [m/s], W: {self.szogseb:1.3f} [rad/s]", False, WHITE, BACKGND)
        self.screen.blit(text, (10,50))

    def setspeed(self, V):
        self.vx = V[0]
        self.vy = V[1]
        self.szogseb = V[2]*3.6

    def setPosition(self, X):
        self.position.x = X[0]
        self.position.y = X[1]
        self.rotation = X[2]

