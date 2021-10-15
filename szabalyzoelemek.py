''' 
Ebben a fileban lesznek a szabalyzo fobb elemei: hajo modell, PID szabalyzok, thruster eroelosztas
'''
import math
import pidcont

# aktuator jelformalas. Egyelore egy egyszeru limietes fuggveny
def actForm(inp, k = 0.25):
    # a k itt be van betonozva. Ez monjda meg, hogy mekkora az aktuatorok minimalis
    # vezerlo jele %-ban

    x = abs(inp)
    if(x < k/2):
        res = 0
    else:
        if(x < k):
            res = k
        else:
            res = x
    return(math.copysign(res, inp))


# hajo fizikai modell, ezt használja a szabályzó.
# le van egyszerusitve, nincs hatvanyozas a csillapitasban, csak a viszszintes mozgast szamolja
class modell:
    # sebesseg x, y, szogsebesseg
    V = [0.0, 0.0, 0.0]
    # szurt INS X, Y sebesseg jel
    Vszurt = [0.0, 0.0]
    # a modell alapjan szamitott sebesseg
    Vmod = [0.0, 0.0]
    # ez meg a Vmod felulatereszto uatni sebesseg
    Vmsz = [0.0, 0.0]
    # ez a sebesseg felulatereszto szurojenek a "kondenzatora"
    CVsz = [0.0, 0.0]

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
        # időállandó a GPS és a modell adatainak összemixeléséhez
        self.taufilt = dict['tauFilt']

    # ez szamolja az eroket az aktuatorok erejebol, aztan a hajo fizikai modelljet.
    # ezt meg osszerakja az INS-bol kapott adatokkal. A szogsebesseget az ISN-tol veszi, a tobbit szamolja.
    # az Ak egy lista 4 elemmel, akutatorok %-ban: orrsugar, farsugar, jobb motor, bal motor
    # a V a sebesseg vektor, amit az INS-tol kap
    # kimenet a szamitott sebessegek, a szabalyzohoz
    def process(self, dt, Ak, V):
        l = dt / self.taufilt
        # erok szamitasa az aktuatorok vezerlo jelei alapjan
        F = [0.0, 0.0]
        F[0] = (Ak[2]+Ak[3])*self.motF # jobb motor + bal motor
        F[1] = Ak[0]*self.orrF + Ak[1]*self.farF # ket orrsugar

        # sebessegek pontositasa az INS alapjan
        # Az INS sebesseg adatat megszurom -> Vsz
        for i in range(2):
            self.Vszurt[i] += (V[i] - self.Vszurt[i]) * l
        # a szogsebesseget atveszem valtoztatas nelkul az INS-tol
        self.V[2] = V[2]

        # mozgasegyenletek.
        # fontos a csillapitas, amit a modellbol adodo sebesseggel szamitok
        A=[0.0,0.0]
        A[0] = (F[0] + self.M[1]*self.V[1]*self.V[2] - self.D[0]*self.Vmod[0]) / self.M[0]
        A[1] = (F[1] - self.M[0]*self.V[0]*self.V[2] - self.D[1]*self.Vmod[1]) / self.M[1]
        #A[0] = self.CAsz[0] + (F[0] + self.M[1]*self.V[1]*self.V[2]) / self.M[0]
        #A[1] = self.CAsz[1] + (F[1] - self.M[0]*self.V[0]*self.V[2]) / self.M[1]

        for i in range(2):
            # integralas. A gyorsitast hozzadom Vmod-hez
            self.Vmod[i] += A[i]*dt
            # szurt mdell sebesseg szamitasa
            self.Vmsz[i] = self.Vmod[i] + self.CVsz[i]
            # soros kondi kisulese
            self.CVsz[i] -= self.Vmsz[i] * l
            # vegul a sebesseg szamitasa
            self.V[i] = self.Vszurt[i] + self.Vmsz[i]

        #print(f'Vx {self.V[0]:03.2f} Vxins {V[0]:03.2f}, Vy {self.V[1]:03.2f}, Vyins {V[1]:03.2f} Vax {self.Va[0]:03.2f}, Vay {self.Va[1]:3.2f}  \r', end='', flush=True)
        #print(f'Vx {self.V[0]:+03.3f} Vxins {V[0]:+03.2f} Vszx {self.Vszurt[0]:+03.2f} Ax {A[0]:+03.4f} Cvszx {self.CVsz[0]:+03.4f} Vmodx {self.Vmod[0]:+03.3f} Vmszx {self.Vmsz[0]:+03.3f} | ', end='')
        #print(f'Vy {self.V[1]:+03.3f} Vyins {V[1]:+03.2f} Vszy {self.Vszurt[1]:+03.2f} Ay {A[1]:+03.4f} Cvszy {self.CVsz[1]:+03.4f} Vmody {self.Vmod[1]:+03.3f} Vmszy {self.Vmsz[1]:+03.3f} \r', end='', flush=True)

        # eredmeny a sebesseg vektor
        return self.V

class PIDcontroller:
    def __init__(self, dict) -> None:
        self.speedX = dict['speedX']
        self.speedY = dict['speedY']
        self.speedZ = dict['speedZ']
        self.orrL = dict['orrL']
        self.farL = dict['farL']
        self.motL = dict['motL']
        self.orrF = dict['orrF']
        self.farF = dict['farF']
        self.motF = dict['motF']
        self.Fmin = dict['Fmin']
        self.F2U2 = dict['F2U2']
        self.Fakt = [self.orrF, self.farF, self.motF, self.motF]

        # a szabalyzokat hatarfrekvenciara kell optimalizalni. Ez elvileg a tomegtol es az erositestol fugg. 
        # az erosites meg a motorok erejetol. Tehat a P tag a tomegtol es az akt. erejetol fugg, a szorzo tenyezo emirikus.
        tau = dict['tauM']
        p = dict['M'][0] / dict['motF'] / dict['tauSzab']
        i = p*dict['D'][0]/dict['M'][0]
        d = p*tau *0
        self.xpid = pidcont.PIDclass(p, i, d)

        tau = dict['tauT']
        p = dict['M'][1] / (dict['orrF'] + dict['farF']) / dict['tauSzab']
        i = p*dict['D'][1]/dict['M'][1]
        d = p*tau *0
        self.ypid = pidcont.PIDclass(p, i, d)

        tau = max(dict['tauT'], dict['tauM'])
        # az Mi a motorok nyomatek kepzese, fugg a nyomatek elosztastol is.Most az egyszeru eset van.
        self.Mi = dict['orrF'] * dict['orrL'] + dict['farF'] * dict['farL'] + 2*dict['motF']*dict['motL']
        p = dict['M'][2] / self.Mi / dict['tauSzab']
        i = p*dict['D'][2]/dict['M'][2]
        # ide kell a D tag, mert ez nem a modellre szabalyoz.
        d = p*tau
        self.zpid = pidcont.PIDclass(p, i, d)
    
    # input: V sebesseg vektor, J joystick: elore, jobbra, forg
    def process(self, dt, V, J):
        Elo = self.xpid.process((J[0]*self.speedX - V[0]), dt)
        Job = self.ypid.process((J[1]*self.speedY - V[1]), dt)
        M = self.zpid.process((J[2]*self.speedZ - V[2]), dt)
        # Erok szetosztasa
        # 1: erok kiosztas az aktuatorokra. Figyelembe kell venni a keletkezo nyomatekokat
        # az x irany egyszeru
        jobbMot = Elo
        balMot = Elo
        # az y irany is egyszeru, de ellenorizni kell, hogy a keletkezo nyomatekot a fomotorok tudjak-e kompenzalni?
        orrsugar = Job
        farsugar = Job
        # a keletkezo nyomatek:
        m2 = orrsugar * self.orrL * self.orrF - farsugar * self.farL * self.farF
        # ezt levonjuk motorokbol
        comp = m2 / self.motF / self.motL
        jobbMot -= comp
        balMot += comp
        # a forgato komponens hozzaadasa
        jobbMot += M
        balMot -= M
        orrsugar += M
        farsugar -= M
        # 2: limitalas aktuatoronkent. A motorok 200%-ra vannak limitalva
        jobbMot =  max(min(2.0, jobbMot), -2.0)
        balMot =  max(min(2.0, balMot), -2.0)
        orrsugar =  max(min(1.0, orrsugar), -1.0)
        farsugar =  max(min(1.0, farsugar), -1.0)
        # 3: kiszamitjuk hogy az elo, job, M tagok hany%-a ervenyesult, es ezt visszacsatoljuk a szabalyzokba.
        eloFb = (jobbMot + balMot) / 2
        jobbFb = (orrsugar + farsugar) / 2
        MFb = (orrsugar * self.orrF * self.orrL - farsugar * self.farF * self.farL + (jobbMot-balMot)/2 * self.motF * self.motL) / self.Mi
        self.xpid.postProcess(eloFb)
        self.ypid.postProcess(jobbFb)
        self.zpid.postProcess(MFb)
        # orrsugar, farsugar, jobb motor, bal motor
        return [orrsugar, farsugar, jobbMot, balMot]

    # ez a PID-bol jovo normalizalt ero komponenseket atszamitja aktuator feszultsegekke. Egyben a limitalast is elvegzi.
    def F2Volt(self, Act):
        # meg kell szorozni az aktuator tenyleges erejevel, utana limitalas erore
        Flim = map(lambda f, l, Fakt: actForm(f*Fakt,l), Act, self.Fmin, self.Fakt)
        #Ez mar valos ero, atszamitasa feszultsegge
        U = list(map(lambda f, k: math.sqrt(f*k), Flim, self.F2U2))
        return U
