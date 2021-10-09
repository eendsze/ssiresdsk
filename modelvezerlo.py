import os
import math
import pygame as pg
import joystick
import szabalyzoelemek
from modellek import *

fps = 50
dt = 1.0/fps
main_dir = os.path.split(os.path.abspath(__file__))[0]

def main():
    pg.init()
    becsultDict = Hajomodell2Becs
    clock = pg.time.Clock()
 #   screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    joy = joystick.myJoystic()
    modell = szabalyzoelemek.modell(becsultDict)
    PID = szabalyzoelemek.PIDcontroller(becsultDict)
    Akt = [ 0, 0, 0, 0] # orrsugar, farsugar, jobb motor, bal motor
    AktFormed = Akt

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.JOYBUTTONDOWN:
                joy.readOffset()
 
        J = joy.read()
        # a hajo koordinatarendszereben: elore x, balra van a +y, balra +forg
        # *** itt van a szimulacio ***

#       Vins = ide kell beolvasni az ins jelet

        # Az aktuatorok vezerlojele es az INS sebesseg jele megy be a modellbe, amit a szabalyzas hasznal. 
        # Itt van a sensor fusion, a GPS es a modell szamitas osszerakasa is.
        # A modell a nyers Akt-ot kapja, ami a szabalyzas kimenete.
        Vmod = modell.process(dt, Akt, Vins)
        # A PID megkapja a modell altal josolt sebesseget es az input vektort is, ezekbol szamolja az aktuatorok jeleit
        Akt = PID.process(dt, Vmod, J)
        AktFormed = map(lambda x: szabalyzoelemek.actForm(x), Akt)

# ezt el is kell kuldeni a motoroknak

        # Ezek a megjelenites dolgai, a szabalyzasba nem szol bele
        # Ez is megjelenites
#        pg.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    main()
