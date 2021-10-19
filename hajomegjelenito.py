import math
import pygame as pg

WHITE = (255, 255, 255)
BACKGND = (0, 0, 0)
LAWNGREEN = (0, 223, 0)
SARGA = (230, 230, 40)
BARNA = (200, 135, 80)
BORDO = (100, 0, 0)

class HajoObject:
    #hajo meretek, [m]
    length = 13.64
    width = 4.1
    #hajo pozicioja, [m, rad]
    position = pg.math.Vector2(0.0,0.0)
    rotation = 0.0
    #hajo sebessege [m/s, rad/s]
    speed = pg.math.Vector2(0,0)
    speed2 = pg.math.Vector2(0,0)
    speed3 = pg.math.Vector2(0,0)
    szogseb = 0.0
    #relativ pozicio a megjeleniteshez
    midscreen = pg.math.Vector2(0,0)
    #hajo pontjai, [m]. Ezt atalakitjuk vektorokka a konstrutorban, azt lehet hasznalni
#    hajoPoly = [(0, 6.82), (-1.35, 5.42), (-2.05, 0), (-2.05, -6.82),  (2.05, -6.82), (2.05, 0), (1.35, 5.42)]
    hajoPoly = [(0.5, 0), (0.4, -0.1), (0, -0.15), (-0.5, -0.15),  (-0.5, 0.15), (0, 0.15), (0.4, 0.1)]
    hajoOffset = 0.0 #ennyivel elorebb tolja a hajo korvonalat a centerhez kepest, csak a megjeleniteshez, hogy szep legyen a fordulas
    #elozo kirajzolt polygon a torleshez
    lastPoly = [(0,0), (0,0), (0,0)]
    speedVect = [pg.math.Vector2(0,0), pg.math.Vector2(0,0)]  #ez a zold sebesseg
    speedVect2 = [pg.math.Vector2(0,0), pg.math.Vector2(0,0)] #ez meg a sarga / INS
    speedVect3 = [pg.math.Vector2(0,0), pg.math.Vector2(0,0)] #ez meg a barna / GPS
    thrustVects = [[]] * 5 # a hajo koordinatarendszereben az aktuatorok vektorai
    #lastThVec = [ [(0,0), (0,0)] ] * 5
    Thrust = [0] * 4
    thrustVects = [[]]*5 # a hajo koordinatarendszereben az aktuatorok vektorai
    lastThVec = [ 
        [(0,0), (0,0)],
        [(0,0), (0,0)],
        [(0,0), (0,0)],
        [(0,0), (0,0)],
        [(0,0), (0,0)]
    ]
    U12V = 0.0
    Uact = [0.0]*4
    Iact = [0.0]*4
    count = 0 #ez csak egy szam, a modellnel a packet counter erteke, hogy lassuk a mukodest

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
        self.thrustVects[0] = [(dict['orrL'], 0), (0, -1)] #orrsugar helye, iranya
        self.thrustVects[1] = [(-dict['farL'], 0), (0, -1)] #farsugar helye, iranya
        self.thrustVects[2] = [(self.hajoVect[3][0], dict['motL']/-2), (-1, 0)] #jobb motor 
        self.thrustVects[3] = [(self.hajoVect[3][0], dict['motL']/2), (-1, 0)] #bal motor helye
        self.thrustVects[4] = [(self.hajoVect[0][0], 0), (0, 1)] #forgas vektor helye, iranya

    def doSpeedVec(self, V):
        result = [0,0]
        speedVect = V.rotate_rad(self.rotation)
        result[0] = self.position*self.scr_scale
        result[1] = (self.position+speedVect)*self.scr_scale
        # flippelni kell lefele, es betenni a kepernyo kozepere
        result = list(map(lambda x: (x.x + self.midscreen.x, self.midscreen.y - x.y), result))
        return result

    def draw(self, color=WHITE):
        #elozo torlese
        pg.draw.polygon(self.screen, BACKGND, self.lastPoly)
        pg.draw.line(self.screen, BACKGND, self.speedVect[0], self.speedVect[1], width = 3)
        pg.draw.line(self.screen, BACKGND, self.speedVect2[0], self.speedVect2[1], width = 3)
        pg.draw.line(self.screen, BACKGND, self.speedVect3[0], self.speedVect3[1], width = 3)
        for x in range(5):
            pg.draw.line(self.screen, BACKGND, self.lastThVec[x][0], self.lastThVec[x][1], width = 3)
            # uj vektorok szamitasa
            #vektor talppontja
            tol = (pg.math.Vector2(self.thrustVects[x][0]).rotate_rad(self.rotation) + self.position)*self.scr_scale
            if(x < 4):
                temp = self.Thrust[x]
            else:
                temp = self.szogseb * 5
            ig  = tol + (pg.math.Vector2(self.thrustVects[x][1]).rotate_rad(self.rotation)) * self.scr_scale*temp*self.ship_scale/5
            #flippelni, kozepre tenni
            self.lastThVec[x][0] = (tol.x + self.midscreen.x, self.midscreen.y - tol.y)
            self.lastThVec[x][1] = (ig.x + self.midscreen.x, self.midscreen.y - ig.y)

        #uj pozicio szamitasa
        #forgatas, poziciora mozgatas, aztan skalazas(zoom):
        shipmap = map(lambda x: (x.rotate_rad(self.rotation) + self.position) * self.scr_scale, self.hajoVect)

        # flippelni kell lefele, es betenni a kepernyo kozepere
        self.lastPoly = list(map(lambda x: (x.x + self.midscreen.x, self.midscreen.y - x.y), shipmap))
        # uj sebesseg vektorok eloallitasa
        self.speedVect = self.doSpeedVec(self.speed)
        self.speedVect2 = self.doSpeedVec(self.speed2)
        self.speedVect3 = self.doSpeedVec(self.speed3)
        # uj rajzolas
        pg.draw.polygon(self.screen, color, self.lastPoly)
        pg.draw.line(self.screen, LAWNGREEN, self.speedVect[0], self.speedVect[1], width = 3)
        pg.draw.line(self.screen, SARGA, self.speedVect2[0], self.speedVect2[1], width = 3)
        pg.draw.line(self.screen, BARNA, self.speedVect3[0], self.speedVect3[1], width = 3)
        for x in self.lastThVec:
            pg.draw.line(self.screen, BORDO, x[0], x[1], width = 3)
        pg.draw.line(self.screen, LAWNGREEN, self.lastThVec[4][0], self.lastThVec[4][1], width = 3)
        # texts
        # speed, ez a valos sebesseg vagy az INS sebesseg
        text = self.font.render("Speed / GPS", True, LAWNGREEN, BACKGND)
        yy = 10
        self.screen.blit(text, (10,yy))
        for i in range(2):
            text = self.font.render(f"V{i}: {self.speed[i]:3.2f} [m/s], ", True, WHITE, BACKGND)
            self.screen.blit(text, (150+i*130,yy))
        # speed2, ez a modell sebesseg
        text = self.font.render("INS sebesseg", True, SARGA, BACKGND)
        yy = 35
        self.screen.blit(text, (10,yy))
        for i in range(2):
            text = self.font.render(f"V{i}: {self.speed2[i]:3.2f} [m/s], ", True, WHITE, BACKGND)
            self.screen.blit(text, (150+i*130,yy))
        # speed3, ez a GPS sebesseg
        text = self.font.render("Modell sebesseg", True, BARNA, BACKGND)
        yy = 60
        self.screen.blit(text, (10,yy))
        for i in range(2):
            text = self.font.render(f"V{i}: {self.speed3[i]:3.2f} [m/s], ", True, WHITE, BACKGND)
            self.screen.blit(text, (150+i*130,yy))
        # Uact, aktuator feszultsegek
        text = self.font.render(f"U12: {self.U12V:2.2f} [V]", True, WHITE, BACKGND)
        self.screen.blit(text, (500,10))
        text = self.font.render(f"Packet cnt: {self.count}", True, WHITE, BACKGND)
        self.screen.blit(text, (480,35))
        yy = 85
        text = self.font.render("Orrsugar ---------- Farsugar ---------- Jobb mot. --------- Bal mot.", True, WHITE, BACKGND)
        self.screen.blit(text, (150,yy))
        text = self.font.render("Feszultsegek", True, WHITE, BACKGND)
        yy = 110
        self.screen.blit(text, (10,yy))
        for i in range(4):
            text = self.font.render(f"{self.Uact[i]:3.2f} [V], ", True, WHITE, BACKGND)
            self.screen.blit(text, (150+i*130,yy))

        text = self.font.render("Áramok", True, WHITE, BACKGND)
        yy = 135
        self.screen.blit(text, (10,yy))
        for i in range(4):
            text = self.font.render(f"{self.Iact[i]:3.2f} [A], ", True, WHITE, BACKGND)
            self.screen.blit(text, (150+i*130,yy))

    # sebesseg megadasa, sajat koordinatarendszerbe. Ez csak a kiirashoz kell
    def setspeed(self, V):
        self.speed = pg.math.Vector2(V[0], V[1])
        self.szogseb = V[2]

    # a masik ket sebesseg vektor megadasa
    def setSpeeds(self, V2, V3):
        self.speed2 = pg.math.Vector2(V2[0], V2[1])
        self.speed3 = pg.math.Vector2(V3[0], V3[1])

    # pozicio, fix kordinatarenszerben
    def setPosition(self, X):
        self.position.x = X[0]
        self.position.y = X[1]
        self.rotation = X[2]

    # aktuator erok, sajat kordinatarenszerben
    def setThrust(self, T):
        self.Thrust = T

    # ez kozeppre teszi a hajot
    def resetPos(self):
        X = self.position*self.scr_scale
        self.midscreen = (self.screen.get_width() / 2, self.screen.get_height() / 2) - pg.math.Vector2(X.x, -X.y)

