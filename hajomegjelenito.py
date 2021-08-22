import math
import pygame as pg

WHITE = (255, 255, 255)
BACKGND = (0, 0, 0)
LAWNGREEN = (0, 223, 0)
BORDO = (100, 0, 0)

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
    hajoOffset = 0.0 #ennyivel elorebb tolja a hajo korvonalat a centerhez kepest, csak a megjeleniteshez, hogy szep legyen a fordulas
    #elozo kirajzolt polygon a torleshez
    lastPoly = [(0,0), (0,0), (0,0)]
    speedVect = [pg.math.Vector2(0,0), pg.math.Vector2(0,0)]
    thrustVects = [[],[],[],[]] # a hajo koordinatarendszereben az aktuatorok vektorai
    lastThVec = [ 
        [(0,0), (0,0)],
        [(0,0), (0,0)],
        [(0,0), (0,0)],
        [(0,0), (0,0)]
    ]
    Thrust = [0, 0, 0, 0]

    def __init__(self, scr, dict) -> None:
        self.screen = scr
        self.ship_scale = dict["length"]
        self.scr_scale = dict["zoom"]
        self.hajoOffset = dict['offset']
        self.midscreen = pg.math.Vector2(scr.get_width() / 2, scr.get_height() / 2)
        # a hajo formaja, felskalazva, offsetelve, de zoomolas elott
        self.hajoVect = list(map(lambda x: pg.math.Vector2(x)*self.ship_scale+(self.hajoOffset, 0), self.hajoPoly))
        self.font = pg.font.Font(None, 24)
        #meghajtas kijelzeshez vektorok
        self.thrustVects[0] = [(dict['orrL'], 0), (0, -1.0)] #orrsugar helye, iranya
        self.thrustVects[1] = [(-dict['farL'], 0), (0, -1.0)] #farsugar helye, iranya
        self.thrustVects[2] = [(self.hajoVect[3][0], dict['motL']/-2), (-1.0, 0)] #jobb motor 
        self.thrustVects[3] = [(self.hajoVect[3][0], dict['motL']/2), (-1.0, 0)] #bal motor helye

    def draw(self, color=WHITE):
        #elozo torlese
        pg.draw.polygon(self.screen, BACKGND, self.lastPoly)
        pg.draw.line(self.screen, BACKGND, self.speedVect[0], self.speedVect[1], width = 3)
        for x in range(4):
            pg.draw.line(self.screen, BACKGND, self.lastThVec[x][0], self.lastThVec[x][1], width = 3)
            # uj vektorok szamitasa
            #vektor talppontja
            tol = (pg.math.Vector2(self.thrustVects[x][0]).rotate_rad(self.rotation) + self.position)*self.scr_scale
            ig  = tol + (pg.math.Vector2(self.thrustVects[x][1]).rotate_rad(self.rotation))*self.scr_scale * self.Thrust[x]
            #flippelni, kozepre tenni
            self.lastThVec[x][0] = (tol.x + self.midscreen.x, self.midscreen.y - tol.y)
            self.lastThVec[x][1] = (ig.x + self.midscreen.x, self.midscreen.y - ig.y)

        #uj pozicio szamitasa
        #forgatas, poziciora mozgatas, aztan skalazas(zoom):
        shipmap = map(lambda x: (x.rotate_rad(self.rotation) + self.position) * self.scr_scale, self.hajoVect)
        speedVect = pg.math.Vector2(self.vx, self.vy).rotate_rad(self.rotation)
        self.speedVect[0] = self.position*self.scr_scale
        self.speedVect[1] = (self.position+speedVect)*self.scr_scale

        # flippelni kell lefele, es betenni a kepernyo kozepere
        self.lastPoly = list(map(lambda x: (x.x + self.midscreen.x, self.midscreen.y - x.y), shipmap))
        self.speedVect = list(map(lambda x: (x.x + self.midscreen.x, self.midscreen.y - x.y), self.speedVect))
        # uj rajzolas
        pg.draw.polygon(self.screen, color, self.lastPoly)
        pg.draw.line(self.screen, LAWNGREEN, self.speedVect[0], self.speedVect[1], width = 3)
        for x in self.lastThVec:
            pg.draw.line(self.screen, BORDO, x[0], x[1], width = 3)
        # texts
        text = self.font.render(f"Pos x: {self.position[0]:3.2f}, y: {self.position[1]:3.2f}. Speed: Vx: {self.vx:3.2f} [m/s], \
Vy: {self.vy:3.2f} [m/s], W: {self.szogseb:1.3f} [rad/s]  ", True, WHITE, BACKGND)
        self.screen.blit(text, (10,10))

    def setspeed(self, V):
        self.vx = V[0]
        self.vy = V[1]
        self.szogseb = V[2]*3.6

    def setPosition(self, X):
        self.position.x = X[0]
        self.position.y = X[1]
        self.rotation = X[2]

    def setThrust(self, T):
        self.Thrust = T

