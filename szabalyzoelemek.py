''' 
Ebben a fileban lesznek a szabalyzo fobb elemei: hajo modell, PID szabalyzok, thruster eroelosztas
'''
import math
import pidcont

# hajo fizikai modell. le van egyszerusitve, nincs hatvanyozas a csillapitasban, csak a viszszintes mozgast szamolja
class modell:
    # sebesseg x, y, szogsebesseg
    V = [0.0, 0.0, 0.0]

    def __init__(self, dict) -> None:
        self.M = dict["M"]
        self.D = dict["D"]
        # Sugarkormanyok es motork adatai. Ha nincs farsugar, akkkor annak az ereje 0.
        # ha egy motor van, akkor a tavolsaguk nulla, es csak az egyiket kell nem 0-ra allitani
        self.orrL = dict["orrL"] #orrsugar tavolsaga a kozepponttol
        self.orrF = dict["orrF"] #orrsugar max ereje, [N]
        self.farL = dict["farL"] #farsugar tavolsaga a kozepponttol
        self.farF = dict["farF"] #farsugar max ereje, [N]
        self.motL = dict['motL'] #motorok tavolsaga egymastol
        self.motF = dict['motF'] #motorok toloereje, allo helyzetben

    # ez szamolja az eroket az aktuatorok erejebol, aztan a hajo fizikai modelljet.
    # ezt meg osszerakja az INS-bol kapott adatokkal. A szogsebesseget az ISN-tol veszi, a tobbit szamolja.
    # az Ak egy lista 4 elemmel, akutatorok %-ban: orrsugar, farsugar, jobb motor, bal motor
    # a V a sebesseg vektor, amit az INS-tol kap
    # kimenet a szamitott sebessegek, a szabalyzohoz
    def process(self, dt, Ak, V):
        # erok szamitasa az aktuatorok vezerlo jelei alapjan
        F = [0.0, 0.0]
        F[0] = (Ak[2]+Ak[3])*self.motF # jobb motor + bal motor
        F[1] = Ak[0]*self.orrF + Ak[1]*self.farF # ket orrsugar

        # sebessegek pontositasa az INS alapjan
        k = 0.9
        self.V = list(map(lambda v, ins: (1-k)*v + k*ins, self.V, V))

        # mozgasegyenletek
        # gyoursulasok szamitasa
        A=[0.0,0.0]
        A[0] = (F[0] + self.M[1]*self.V[1]*self.V[2] - self.D[0]*self.V[0]) / self.M[0]
        A[1] = (F[1] - self.M[0]*self.V[0]*self.V[2] - self.D[1]*self.V[1]) / self.M[1]
        # integralas. Az 1-k csak a szeperzekem miatt kell
        self.V[0] = self.V[0]+A[0]*dt*(1-k)
        self.V[1] = self.V[1]+A[1]*dt*(1-k)
        self.V[2] = V[2]

        # eredmeny a sebesseg vektor
        return self.V

class PIDcontroller:
    def __init__(self) -> None:
        self.xpid = pidcont.PIDclass(3.5,5,5)
        self.ypid = pidcont.PIDclass(5.5,8,5)
        self.zpid = pidcont.PIDclass(6,12,5)
    
    # input: V sebesseg vektor, J joystick: elore, jobbra, forg
    def process(self, dt, V, J):
        M = self.zpid.process((J[2]*0.1 - V[2]), dt)
        Job = self.ypid.process((J[1]*0.5 - V[1]), dt)
        Elo = self.xpid.process((J[0] - V[0]), dt)
        # orrsugar, farsugar, jobb motor, bal motor
        return [M+Job, -M+Job, Elo, Elo]
