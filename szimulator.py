#!/usr/bin/env python

import os
#import math
import pygame as pg
import hajomegjelenito
import joystick
import fizikaimodell
import szimulaltelemek
import szabalyzoelemek
import megjelenit
from modellek import *

fps = 50
dt = 1.0/fps
main_dir = os.path.split(os.path.abspath(__file__))[0]


def main():
    pg.init()
    #dict = Nagyhajo445_modell
    #becsultDict = Nagyhajo445_becsles
    dict = Hajomodell2
    becsultDict = Hajomodell2Becs
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    hajo = hajomegjelenito.HajoObject(screen, dict)
    joy = joystick.myJoystic(dt)
    megj = megjelenit.disp()
    valosModell = fizikaimodell.physicalShip(dict)
    #valosModell.setEnvironment(Kornyezet1)
    valosModell.setEnvironment(KornyezetCsendes)
    AkForces = [0.0, 0.0, 0.0, 0.0]
    aktuators = szimulaltelemek.akutatorSim(dict)
    INS = szimulaltelemek.insSim()
    modell = szabalyzoelemek.modell(becsultDict)
    PID = szabalyzoelemek.PIDcontroller(becsultDict)
    Akt = [ 0, 0, 0, 0] # orrsugar, farsugar, jobb motor, bal motor
    AktFormed = Akt
    #seged, a limitalashoz
    Fl = becsultDict['Fmin']
    ActLim = [Fl[0]/becsultDict['orrF'],Fl[1]/becsultDict['farF'], Fl[2]/becsultDict['motF'], Fl[3]/becsultDict['motF']]

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.JOYBUTTONDOWN:
                joy.readOffset()
 
        J = joy.read()
        # a hajo koordinatarendszereben: elore x, balra van a +y, balra +forg
        # *** itt van a szimulacio ***
        # Az elozoleg meghatarozott akutator jeleket atadja az aktuator vezerlonek. 
        # Ez az aktuatorok idobeni viselkedeset modellezi
        # Itt ezt hasznalja a valso modell is, a valosagban a mert aramjeleket fogja hasznalni.
        AkForces = aktuators.process(dt, AktFormed)
        # Ez az adatot kapja a hajo szimulator, ami alapjan a rajzolas is megy
        V = valosModell.calcForces(dt, AkForces)
        # A szimulatorbol a hajo sebessege bemegy az INS-t szimulalo egysegbe
        Vins = INS.process(dt, V)
        # Az aktuatorok vezerlojele es az INS sebesseg jele megy be a modellbe, amit a szabalyzas hasznal. 
        # Itt van a sensor fusion, a GPS es a modell szamitas osszerakasa is.
        # A modell a nyers Akt-ot kapja, ami a szabalyzas kimenete.
        Vmod = modell.process(dt, Akt, Vins)
        # A PID megkapja a modell altal josolt sebesseget es az input vektort is, ezekbol szamolja az aktuatorok jeleit
        Akt = PID.process(dt, Vmod, J)
        #a rendszer itt normalizalt erokkel dolgozik, ezert kell az ActLim
        AktFormed = map(lambda x, l: szabalyzoelemek.actForm(x,l), Akt, ActLim)

        # Ezek a megjelenites dolgai, a szabalyzasba nem szol bele
        hajo.setPosition(valosModell.X)
        hajo.setspeed(V)
        hajo.setThrust(AkForces)
        #hajo.setThrust(Akt)
        if joy.getReset():
            hajo.resetPos()
        hajo.draw()

        megj.setActVolt(AkForces)
        megj.show()

        # Ez is megjelenites
        pg.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
