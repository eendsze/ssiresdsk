import time, sys, random
import math

class disp:
    actVoltages = [0.0] * 4
    actCurrents = [0.0] * 4
    battVolt = 0.0
    rows = 4

    def __init__(self) -> None:
        sys.stdout.write("\n" * self.rows)
        
    def show(self):
        sys.stdout.write(u"\u001b[1000D") # Move left
        sys.stdout.write(u"\u001b[" + str(self.rows) + "A") # Move up
        #elso sor actuator fesz orrsugar, farsugar, jobb motor, bal motor
        print(f'Actuator fesz: Uorr {self.actVoltages[0]:+02.2f} Ufar {self.actVoltages[1]:+02.2f} \
Ujobb {self.actVoltages[2]:+02.2f} Ubal {self.actVoltages[3]:+02.2f}')
        #masodik sor aramok
        print(f'Actuator aram: Iorr {self.actCurrents[0]:+02.2f} Ifar {self.actCurrents[1]:+02.2f} \
Ijobb {self.actCurrents[2]:+02.2f} Ibal {self.actCurrents[3]:+02.2f}. Batt V: {self.battVolt:+02.2f}')
        #tobbi
        print("-")
        print("-")

    def setActVolt(self, v):
        self.actVoltages = v

    def setActCurr(self, v):
        self.actCurrents = v

    def setBattV(self, v):
        self.battVolt = v

