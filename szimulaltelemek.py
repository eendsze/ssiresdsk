'''
Ebben vannak a szabalyzas szimulalt elemei: INS szimulator, aktuator meghajtas szimulator
'''

import math
import random

# INS szimulator. Az INS hibajat szimulalja. A hiba egy feher zaj integralasabol adodik, amit alulateresztovel
# szurunk, hogy ne szalljon el. A cel hogy hasonlo hibat adjon, mint a GPS-es INS
class insSim:
    vx = 0.0 #integratorok
    vy = 0.0

    def __init__(self, am = 1.0, fr = 0.025) -> None:
        self.amp = am
        self.freq = fr

    def process(self, dt, V):
        '''  k = (1-dt*self.freq)
        r = dt*self.amp * 0.2
        self.vx += random.uniform(-r,r)
        self.vx *= k
        self.vy += random.uniform(-r,r)
        self.vy *= k
        '''
        #egyelore kiveszem a zajt, mert mas lesz
        return [V[0]+self.vx, V[1]+self.vy, V[2]]

class akutatorSim:
    AkForces = [0.0, 0.0, 0.0, 0.0]

    def __init__(self, ta = 0.5) -> None:
        self.tau = ta

    # Ak: orrsugar, farsugar, jobb motor, bal motor
    def process(self, dt, Ak):
        self.AkForces = list(map(lambda x,y: x + (y-x)/self.tau*dt, self.AkForces, Ak))
        return self.AkForces

