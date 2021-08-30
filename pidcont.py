''' 
Altalanos PID kontroller, limitalassal. A kimenet +/- 1.0 koze limital.
A bemenet a hibajel, ezt a hivo kell hogy kiszamolja
'''


class PIDclass:
    Iterm = 0.0
    lastErr = 0.0
    integrate = True

    def __init__(self, P, I, D) -> None:
        self.pt = P
        self.it = I
        self.dt = D

    def process(self, err, dt):
        Pterm = err * self.pt
        Dterm = (err - self.lastErr) / dt
        self.lastErr = err
        # kimenet szamitasa
        output = self.pt*Pterm + self.it*self.Iterm + self.dt*Dterm
        # integralas, anti windup
        if not((output > 1.0 and err > 0) or (output < -1.0 and err < 0)):
            self.Iterm += err * dt
        # limitalas +/- 1.0-ra
        return max(min(1.0, output), -1.0)

