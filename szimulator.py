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
    #
    #hajoAdatok = Nagyhajo445_modell
    #becsulthajoAdatok = Nagyhajo445_becsles
    #
    hajoAdatok = Hajomodell2
    becsulthajoAdatok = Hajomodell2Becs
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    hajo = hajomegjelenito.HajoObject(screen, hajoAdatok)
    joy = joystick.myJoystic(dt)
    megj = megjelenit.disp()
    valosModell = fizikaimodell.physicalShip(hajoAdatok)
    #
    #valosModell.setEnvironment(Kornyezet1)
    valosModell.setEnvironment(KornyezetCsendes)
    AkForces = [0.0, 0.0, 0.0, 0.0]
    aktuators = szimulaltelemek.akutatorSim(hajoAdatok)
    INS = szimulaltelemek.insSim()
    modell = szabalyzoelemek.modell(becsulthajoAdatok)
    PID = szabalyzoelemek.PIDcontroller(becsulthajoAdatok)
    Akt = [ 0, 0, 0, 0] # orrsugar, farsugar, jobb motor, bal motor
    AktFormed = Akt
    #seged, a limitalashoz
    Fl = becsulthajoAdatok['Fmin']
    ActLim = [Fl[0]/becsulthajoAdatok['orrF'],Fl[1]/becsulthajoAdatok['farF'], Fl[2]/becsulthajoAdatok['motF'], Fl[3]/becsulthajoAdatok['motF']]
    Fakt = [becsulthajoAdatok['orrF'], becsulthajoAdatok['farF'], becsulthajoAdatok['motF'], becsulthajoAdatok['motF']]
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

#beteszek egy hibat
#        Akt[2] = Akt[2] * 3
#        Akt[3] = Akt[3] * 3

        Vmod = modell.process(dt, Akt, Vins)
        # A PID megkapja a modell altal josolt sebesseget es az input vektort is, ezekbol szamolja az aktuatorok jeleit
        Akt = PID.process(dt, Vmod, J)
#        Akt = PID.processJoyOnly(dt, Vmod, J)
        # hogy tesztelheto legyen az akt_form(), eloszor megszorzom az erovel, aztan visszaosztom, mert a szimulacio relativ 
        # erokat hasznal
        F = list(map(lambda a, Fakt: a * Fakt, Akt, Fakt))
        Fformed = PID.akt_form(F)
        AktFormed = map(lambda f, Fakt: f / Fakt, Fformed, Fakt)
        # ez a regi a rendszer itt normalizalt erokkel dolgozik, ezert kell az ActLim
        # ez a regi AktFormed = map(lambda x, l: szabalyzoelemek.actForm(x,l), Akt, ActLim)

        # Ezek a megjelenites dolgai, a szabalyzasba nem szol bele
        hajo.setPosition(valosModell.X)
        hajo.setspeed(V)
        hajo.setSpeeds(Vins, Vmod)
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
