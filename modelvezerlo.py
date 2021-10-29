import os, time, socket
#import pygame as pg
import joystick
import szabalyzoelemek
import serial, json
from modellek import *

fps = 100
dt = 1.0/fps
main_dir = os.path.split(os.path.abspath(__file__))[0]

def main():
    try:
        ser = serial.Serial("/dev/ttyACM0", 115200)
        #ser = serial.Serial("com22", 115200)
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

    # INS adat fogado socket
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.settimeout(0.02) 
    ss.bind(('127.0.0.1', 6543))

    #pg.init()
    becsultDict = Hajomodell2Becs
    #clock = pg.time.Clock()
    joy = joystick.remoteJoystick(dt)
    modell = szabalyzoelemek.modell(becsultDict)
    PID = szabalyzoelemek.PIDcontroller(becsultDict)
    Akt = [ 0, 0, 0, 0] # orrsugar, farsugar, jobb motor, bal motor
    #Vins [self.vx, self.vy, V[2]]
    Vins = [0.0] * 3
    Vgps = [0.0] * 3
    #pwmDict = {}
    #ellenallas kalibracio kuldese. orrsugar, farsugar, jobb motor, bal motor
    #10 = 1 mOhm
    res = becsultDict['motRes']
    command = f"res {int(res[0]*10000)} {int(res[1]*10000)} {int(res[2]*10000)} {int(res[3]*10000)} end \n"
    print('Res: ' + command)
    #command = f"res 0 0 0 0 end \n"
    ser.write(command.encode())
    time.sleep(0.1)
    ser.write(command.encode())
    time.sleep(0.1)
    ser.write(command.encode())

    count = 0

    while 1:
        J = joy.read()
        # a hajo koordinatarendszereben: elore x, balra van a +y, balra +forg
        # *** itt van a szimulacio ***

        # Vins = ide kell beolvasni az ins jelet
        try:
            data, _ = ss.recvfrom(1000)
            jres = json.loads(data)
            if ('ang' in jres):
                #ez a gyors, INS alapu sebesseg
                Vins = jres['Vvec']
                Vins = [Vins[1], -Vins[0], Vins[2]]
                #ez megy csak a szoget veszi az INS-bol
                Vgps[2] = Vins[2]
            if('gps' in jres):
                Vgps  = jres['Vgps_vec']
                Vgps = [Vgps[1], -Vgps[0], Vgps[2]]
            count += 1
        except Exception as e:
            Vins = [0.0, 0.0, 0.0]
            Vgps = Vins
            print(e)

        # Ez valasztja ki hogy mirol menjen a vezerles
        vt = Vins

        # Az aktuatorok vezerlojele es az INS sebesseg jele megy be a modellbe, amit a szabalyzas hasznal. 
        # Itt van a sensor fusion, a GPS es a modell szamitas osszerakasa is.
        # A modell a nyers Akt-ot kapja, ami a szabalyzas kimenete.
        Vmod = modell.process(dt, Akt, vt)
        # A PID megkapja a modell altal josolt sebesseget es az input vektort is, ezekbol szamolja az aktuatorok jeleit
        Akt = PID.process(dt, Vmod, J)
#        Akt = PID.processJoyOnly(dt, Vmod, J)

        x = 1 # arany, nem N
        #Akt = [1, 1, 0, 0]
        # Az Akt itt meg -1 .. +1 kozotti relativ ertek!
        Uout = PID.F2Volt(Akt)

        if(J[3] == 0):
            Uout = [0]*4

        # ezt el is kell kuldeni a motoroknak
        command = f"start {int(Uout[0]*1000)} {int(Uout[1]*1000)}  {int(Uout[2]*1000)}  {int(Uout[3]*1000)}  end \n"

        #x = 500
        #command = f"start {x} {x} {x} {x} end \n"
        #command = f"start  0 0 {x} {x} end \n"
        ser.write(command.encode())
        # be isolvasom az aramot, ha van mit. Ennek a vegen van az U12V
        try:
            res = ser.readline()
            motCurr = json.loads(res)
        except:
            pass

        #joy.write(['Aramok: ' + json.dumps(motCurr), 'U ki: ' + json.dumps(Uout), 'INS seb: ' + json.dumps(Vins), 'Joy inp: ' + json.dumps(J), f'count: {count}'])
        joy.write({'motCurr': motCurr, 'Uout': Uout, 'Vins': Vins, 'Vmod': Vmod, 'Vgps': Vgps, 'Akt': Akt})

        #clock.tick(fps)

if __name__ == "__main__":
    main()
