'''
Ebben vannak a szabalyzas szimulalt elemei: INS szimulator, aktuator meghajtas szimulator
'''

import math
import random

# INS szimulator. Az INS hibajat szimulalja. A hiba egy feher zaj integralasabol adodik, amit alulateresztovel
# szurunk, hogy ne szalljon el. A cel hogy hasonlo hibat adjon, mint a GPS-es INS
class insSim:
    # hibak
    vx = 0.0 #integratorok
    vy = 0.0
    time = 0
  
    def __init__(self, am = 1.0, fr = 0.025) -> None:
        self.amp = am
        self.freq = fr

    def process(self, dt, V):
        # merem az idot, masodpercenkent 4x jon gps adat
        self.time += dt
        r = 0.05
        # 1/4-ed sec-enkent jon ujabb minta, akkor ugrik a hiba
        if self.time > 0.25:
            self.time -= 0.25
            self.vx = V[0] + random.uniform(-r,r)
            self.vy = V[1] + random.uniform(-r,r)

        # ez meg nyersen, igy meg nagy a hiba
        return [self.vx, self.vy, V[2]]

class akutatorSim:
    AkForces = [0.0, 0.0, 0.0, 0.0] # orrsugar, farsugar, jobb motor, bal motor

    def __init__(self, dict) -> None:
        self.tau = [dict['tauT'], dict['tauT'], dict['tauM'], dict['tauM']]

    # Ak: orrsugar, farsugar, jobb motor, bal motor
    def process(self, dt, Ak):
        self.AkForces = list(map(lambda x,y, tau: x + (y-x)/tau*dt, self.AkForces, Ak, self.tau))
        return self.AkForces

