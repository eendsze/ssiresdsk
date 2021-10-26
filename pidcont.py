''' 
Altalanos PID kontroller, limitalassal. A kimenet +/- 1.0 koze limital.
A bemenet a hibajel, ezt a hivo kell hogy kiszamolja
'''


class PIDclass:
    Iterm = 0.0
    lastErr = 0.0
    integrate = True
    output = 0.0
    err = 0
    dt = 1

    def __init__(self, P, I, D) -> None:
        self.kpt = P
        self.kit = I
        self.kdt = D

    # Itt kapja meg a PID a hiba jelet, es kiszamitja a kimeno jelet
    def process(self, err, dt):
        self.err = err
        self.dt = dt
        Pterm = err * self.kpt
        Dterm = (err - self.lastErr) / dt
        self.lastErr = err
        # kimenet szamitasa, D tag nelkul, hogy az ne limitalja az integralast
        self.output = Pterm + self.kit*self.Iterm + self.kdt*Dterm
        # integralas - nem itt van, hanem a postProcessben
        # a kimenetet elore limitaljuk
        return max(min(1.0, self.output), -1.0)

    # Itt pedig megkapja a visszacsatolast, hogy tenylegesen mekkoa jel
    # tudott kimenni az aktuatorokra. Ez alapja tortenik az integralas korlatozasa
    # az input +/-1.0 kozott kell legyen, normalis esetben, illetve, ha nem volt limitalas,
    # akkor AZONOSNAK KELL LENNIE a process-ben kiadott ertekkel.
    # az integralas ide kerul, de eolobb ugy modositom az err tagot, hogy ne hozzon
    # letre nagyobb outputot, mint ami ki tudott menni. Es a self.lastErr-t is meghamisitom,
    # hogy a D tag szamitasa is jo maradjon.
    def postProcess(self, fb):
        # ki kell szamitani, hogy a megvalosult - fb - kimenethez mekkora error tag tartozott volna
        # itt a self.output-tal szamolunk, azt kell visszahozni. A kimenet limitalva volt, de az itt nem erdekes
        diff = fb - self.output
        errDelta = diff / (self.kpt + self.kdt / self.dt)
        self.err += errDelta # ez lesz az a szam, ami nem okozott volna kiulest, ezzel kell integralni
        # ide kerul az integralas
        self.Iterm += self.err * self.dt
        # es a modositott erteket taroljuk el lastErr-kent.
        self.lastErr = self.err
