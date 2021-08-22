"""
Ez a hajó fizikai modellje.
Inputok: a hajóra ható erők és nyomtékok összessége
Kimeneti változók: a hajó sebessége, gyorsulása, saját koordinátarendszerben
    +a hajó pozíciója és szöge fix koordinátarendszerben
Saját paraméterek:
-a hajó paraméterei, a 
https://www.researchgate.net/publication/4346638_Identification_of_a_control_oriented_nonlinear_dynamic_USV_model
cikk szerint,

m11 *˙vx − m22*vy*ω + d1*sgn(vx)*|vx|**α1 = fx,
m22 *˙vy + m11*vx*ω + d2*sgn(vy)*|vy|**α2 = fy,
m33 *˙ω + md*vx*vy + d3*sgn(ω)*|ω|**α3 = T,
// md = m22 - m11

"""

import math

#seged fv, unsigned hatvanyozas
def mypow(x, y):
    return math.copysign(abs(x)**y, x)

class physicalShip:
    # A[0]:ax, gyorsulas x, A[1]:ay, A[2] szoggyorsulas
    A = [0.0, 0.0, 0.0]
    # sebesseg x, y, szogsebesseg
    V = [0.0, 0.0, 0.0]
    # pozicio, fix koordinatarendszerben
    X = [0.0, 0.0, 0.0]

    def __init__(self, dict) -> None:
        self.M = dict["M"]
        self.D = dict["D"]
        self.Af = dict["Af"]
        # Sugarkormanyok es motork adatai. Ha nincs farsugar, akkkor annak az ereje 0.
        # ha egy motor van, akkor a tavolsaguk nulla, es csak az egyiket kell nem 0-ra allitani
        self.orrL = dict["orrL"] #orrsugar tavolsaga a kozepponttol
        self.orrF = dict["orrF"] #orrsugar max ereje, [N]
        self.farL = dict["farL"] #farsugar tavolsaga a kozepponttol
        self.farF = dict["farF"] #farsugar max ereje, [N]
        self.motL = dict['motL'] #motorok tavolsaga egymastol
        self.motF = dict['motF'] #motorok toloereje, allo helyzetben


    #bemenet a dt, es az ero vektor
    def calculate(self, dt, F = [0.0, 0.0, 0.0]):
        # integralas
        # kozbenso sebesseg az integralashoz, ezzel szamol
        Vk = list(map(lambda v, a: v + a/2 * dt, self.V, self.A))
        # ez lesz a kovetkezo sebesseg, itt van az integralas
        self.V = list(map(lambda v, a: v + a * dt, self.V, self.A))

        # pozicio szamitasa, fix koordinatarendszerben
        # eloszor az uj szog kell
        self.X[2] += (self.V[2] + self.A[2]/2*dt)*dt
        # aztan ezzel eforgatva az uj pozicio
        self.X[0] += (math.cos(self.X[2])*Vk[0] - math.sin(self.X[2])*Vk[1]) *dt
        self.X[1] += (math.sin(self.X[2])*Vk[0] + math.cos(self.X[2])*Vk[1]) *dt

        # gyoursulasok updatelese a kovetkezo idopontra
        # x irany
        self.A[0] = (F[0] + self.M[1]*Vk[1]*Vk[2] - self.D[0]*mypow(self.V[0], self.Af[0])) / self.M[0]
        # y irany
        self.A[1] = (F[1] - self.M[0]*Vk[0]*Vk[2] - self.D[1]*mypow(self.V[1], self.Af[1])) / self.M[1]
        # z irany, szoggyorsulas
        self.A[2] = (F[2] - (self.M[1]-self.M[0])*Vk[0]*Vk[1] - self.D[2]*mypow(self.V[2], self.Af[2])) / self.M[2]

    def calcForces(self, dt, Ak):
        #az Ak egy lista 3 vagy negy elemmel, akutatorok %-ban: orrsugar, farsugar, jobb motor, bal motor
        F = [0.0, 0.0, 0.0]
        F[0] = (Ak[2]+Ak[3])*self.motF # jobb motor + bal motor
        F[1] = Ak[0]*self.orrF + Ak[1]*self.farF # ket orrsugar
        F[2] = Ak[0]*self.orrF*self.orrL - Ak[1]*self.farF*self.farL + (Ak[2]-Ak[3])*self.motF*self.motL/2 # nyomatekok
        self.calculate(dt, F)

