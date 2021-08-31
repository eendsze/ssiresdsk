''' 
Ebben a fileban lesznek a szabalyzo fobb elemei: hajo modell, PID szabalyzok, thruster eroelosztas
'''
import math
import pidcont

# hajo fizikai modell. le van egyszerusitve, nincs hatvanyozas a csillapitasban, csak a viszszintes mozgast szamolja
class modell:
    # sebesseg x, y, szogsebesseg
    V = [0.0, 0.0, 0.0]
    # szurt INS X, Y sebesseg jel
    Vsz = [0.0, 0.0]
    # ez a gyorsulas felulatereszto szurojenek a "kondenzatora"
    CAsz = [0.0, 0.0]

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
        l = dt * 0.2 # egyelore ez a szuresi idoallando
        # erok szamitasa az aktuatorok vezerlo jelei alapjan
        F = [0.0, 0.0]
        F[0] = (Ak[2]+Ak[3])*self.motF # jobb motor + bal motor
        F[1] = Ak[0]*self.orrF + Ak[1]*self.farF # ket orrsugar

        # sebessegek pontositasa az INS alapjan
        # Az INS sebessege egy idoallandoval huzza maga utan a V-t, a hajo sebesseget
        for i in range(2):
            self.V[i] += (V[i] - self.V[i]) * l
        # a szogsebesseget atveszem valtoztatas nelkul az INS-tol
        self.V[2] = V[2]

        # mozgasegyenletek. A keletkezo gyorsulast szurom felulatereszto szurovel
        # gyoursulasok szamitasa, hozzaadjuk a "soros kondi" erteket is
        A=[0.0,0.0]
        A[0] = self.CAsz[0] + (F[0] + self.M[1]*self.V[1]*self.V[2] - self.D[0]*self.V[0]) / self.M[0]
        A[1] = self.CAsz[1] + (F[1] - self.M[0]*self.V[0]*self.V[2] - self.D[1]*self.V[1]) / self.M[1]
        #A[0] = self.CAsz[0] + (F[0] + self.M[1]*self.V[1]*self.V[2]) / self.M[0]
        #A[1] = self.CAsz[1] + (F[1] - self.M[0]*self.V[0]*self.V[2]) / self.M[1]

        for i in range(2):
            # soros kondi kisulese
            self.CAsz[i] -= A[i] * l
            # integralas. A gyorsitast hozzadom V-hez
            self.V[i] += A[i]*dt

        #print(f'Vx {self.V[0]:3.2f} Vxins {V[0]:3.2f}, Vy {self.V[1]:3.2f}, Vyins {V[1]:3.2f} Ax {A[0]:3.2f}, Ay {A[1]:3.2f}  \r', end='', flush=True)
        print(f'Vx {self.V[0]:3.3f} Vxins {V[0]:3.2f} Ax {A[0]:3.4f}  \r', end='', flush=True)

        # eredmeny a sebesseg vektor
        return self.V

class PIDcontroller:
    def __init__(self) -> None:
        self.xpid = pidcont.PIDclass(3.5,5,10)
        self.ypid = pidcont.PIDclass(5.5,8,10)
        self.zpid = pidcont.PIDclass(6,12,5)
    
    # input: V sebesseg vektor, J joystick: elore, jobbra, forg
    def process(self, dt, V, J):
        M = self.zpid.process((J[2]*0.1 - V[2]), dt)
        Job = self.ypid.process((J[1]*0.5 - V[1]), dt)
        Elo = self.xpid.process((J[0] - V[0]), dt)
        # orrsugar, farsugar, jobb motor, bal motor
        return [M+Job, -M+Job, Elo, Elo]
