import os
#import math
import pygame as pg
import joystick
import szabalyzoelemek
import megjelenit
import serial, json
from modellek import *

fps = 100
dt = 1.0/fps
main_dir = os.path.split(os.path.abspath(__file__))[0]

def main():
    try:
        #ser = serial.Serial("/dev/ttyACM0", 115200)
        ser = serial.Serial("com22", 115200)
    except Exception as e:
        print(str(e))
        exit()
    ser.timeout = 0

    if ser.isOpen():
        ser.close()

    try:
        ser.open()
    except Exception as e:
        print(str(e))
        exit()
    ser.flushInput()

    pg.init()
    becsultDict = Hajomodell2Becs
    clock = pg.time.Clock()
 #   screen = pg.display.set_mode((1000, 1000), pg.RESIZABLE)
    joy = joystick.myJoystic()
    megj = megjelenit.disp()
    modell = szabalyzoelemek.modell(becsultDict)
    PID = szabalyzoelemek.PIDcontroller(becsultDict)
    Akt = [ 0, 0, 0, 0] # orrsugar, farsugar, jobb motor, bal motor
    #Vins [self.vx, self.vy, V[2]]
    Vins = [0.0] * 3
    # AKTUATOR 100%-HOZ TARTOZO FESZULTSEGEK orrsugar, farsugar, jobb motor, bal motor
    Voltages = [6.0, 6.0, 3.0, 3.0]
    AktFormed = Akt

    #ellenallas kalibracio kuldese
    #10 = 1 mOhm
    command = f"res 8000 8000 3500 3000 end \n"
    ser.write(command.encode())


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
        AktFormed = list(map(lambda x, v: szabalyzoelemek.actForm(x) * v, Akt, Voltages))

        # ezt el is kell kuldeni a motoroknak
        #command = f"start {int(AktFormed[0]*1000)} {int(AktFormed[1]*1000)}  {int(AktFormed[2]*1000)}  {int(AktFormed[3]*1000)}  end \n"
        x = 800
        command = f"start {x} {x} {x} {x} end \n"
        ser.write(command.encode())
        # be isolvasom az aramot, ha van mit
        try:
            res = ser.readline()
            pwmDict = json.loads(res)
            curr =[pwmDict['I1'], pwmDict['I2'], pwmDict['I3'], pwmDict['I4']]
            megj.setActCurr(curr)
            megj.setBattV(pwmDict['Ubat'])
        except:
            pass

        # Ezek a megjelenites dolgai, a szabalyzasba nem szol bele
        megj.setActVolt(AktFormed)
        megj.show()
        # Ez is megjelenites
#        pg.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    main()
