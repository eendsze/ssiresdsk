#!/usr/bin/env python

import os
import math
import pygame as pg
import hajomegjelenito
import joystick
import fizikaimodell
import szimulaltelemek
import szabalyzoelemek

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

Nagyhajo445_modell = {
    #"M": [12600, 28900, 170000],
    "M": [12600, 18000, 170000],
    "D": [200, 2000, 200000],
    "Af": [1.7, 2.0, 1.6],
    'kw': 0.2, # ezzel szorozza be a sebessegbol eredo forgato erot. A kormanylapat hatasara 0, kis negativ szam lesz
    "length": 13,
    'offset': 1.0, #ennyivel van hatrabb a forgaspont a hajo kozepetol, csak a megjeleniteshez kell
    "zoom": 25,
    'orrL': 5, #orrkormany tavolsaga a hajo forgaspontjatol
    'orrF': 950,
    'farL': 5,
    'farF': 950,
    'motL': 2.2, # propellerek tavolsaga egymastol
    'motF': 2000, #ez 200%-os is lehet egyelore
    'tauT': 0.5 # thrusterek idoallandoja, kb.
}

Nagyhajo445_becsles = {
    "M": [10000, 20000, 200000],
    "D": [200, 2000, 200000],
    'orrL': 5, #orrkormany tavolsaga a hajo forgaspontjatol
    'orrF': 950,
    'farL': 5,
    'farF': 950,
    'motL': 2.2, # propellerek tavolsaga egymastol
    'motF': 2000, #ez 200%-os is lehet egyelore
    'tauT': 0.6 # thrusterek idoallandoja, kb.
}


Kornyezet1 = {
    'hullamszog': math.pi/2, # az erok ebben az iranyban hatnak
    'Fkornyezet': 300, # ez az allando tag, kb a szel hatasa, ha oldalraol kapja
    'Fhullam': 2000, # ez a hullamzas amplitudoja ha oldalrol kapja
    'Whullam': 1.0, # ez a hullamzas szogfrekvenciaja, radian/sec
    'Khatulrol': 0.25 # hatulrol ekkora aranyu lesz az ero
}

#ez egy komment
def main():
    pg.init()
    dict = Nagyhajo445_modell
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    hajo = hajomegjelenito.HajoObject(screen, dict)
    joy = joystick.myJoystic()
    valosModell = fizikaimodell.physicalShip(dict)
    valosModell.setEnvironment(Kornyezet1)
    AkForces = [0.0, 0.0, 0.0, 0.0]
    aktuators = szimulaltelemek.akutatorSim()
    INS = szimulaltelemek.insSim()
    modell = szabalyzoelemek.modell(Nagyhajo445_becsles)
    PID = szabalyzoelemek.PIDcontroller()
    Akt = [ 0, 0, 0, 0]

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.JOYBUTTONDOWN:
                joy.readOffset()
 
        J = joy.read()
        # a hajo koordinatarendszereben: elore x, balra van a +y, balra +forg
        
        # *** itt van a szimulacio ***
        # Az elozoleg meghatarozott akutator jeleket atadja az aktuator vezerlonek. Ez az aktuatorok idobeni viselkedeset modellezi
        # TODO ebbe kene tenni az ero szamitast is, most csak idoallandot szamit, az is fixen van bebetonozva
        AkForces = aktuators.process(dt, Akt)
        # Ez az adatot kapja a hajo szimulator, ami alapjan a rajzolas is megy
        # TODO ez nem jo, a valos es a szimulator modell is ugyanazt a szamitott aktuator erot kapja...
        V = valosModell.calcForces(dt, AkForces)
        # A szimulatorbol a hajo sebessege bemegy az INS-t szimulalo egysegbe
        Vins = INS.process(dt, V)
        # Az aktuatorok jele es az INS sebesseg jele megy be a modellbe, amit a szabalyzas hasznal. Itt lenne a sensor fusion
        Vmod = modell.process(dt, AkForces, Vins) 
        # A PID megkapja a modell altal josolt sebesseget es az input vektort is, ezekbol szamolja az aktuatorok jeleit
        Akt = PID.process(Vmod, J)

        # Ezek a megjelenites dolgai, a szabalyzasba nem szol bele
        hajo.setPosition(valosModell.X)
        hajo.setspeed(V)
        hajo.setThrust(AkForces)
        if joy.getReset():
            hajo.resetPos()
        hajo.draw()
        # Ez is megjelenites
        pg.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
