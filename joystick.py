#!/usr/bin/env python

#ebben van minden:
# myJoystic: ez a joystick kezelo, beolvassa, vagy ha nincs akkor a billentyuzetet
# remoteJoystick: ez a tavoli joystick jelet veszi, beolvassa. Es van neki egy kuldo fuggvenye is,
# amin keresztul elkuldi a printelendo adatokat egy lsitaban (minden listaelem uj sorken jelenik meg)
# ha onmagaban futtatjak, akkor meg o a kuldo, kezeli a joysticket es elkuldi, ami jon azt meg megjeleniti.

import pygame
import socket
import json
import netifaces

fps = 50
dt = 1.0/fps
WHITE = (255, 255, 255)
BACKGND = (0, 0, 0)

class remoteJoystick:
    recPort = 6544
    sendPort = 6546

    def __init__(self, dt) -> None:
        self.dt = dt
        self.bss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.bss.setblocking(False)
        gwadd = netifaces.gateways()[2][0][0]
        b = socket.inet_aton(gwadd)
        self.badd = f'{b[0]}.{b[1]}.{b[2]}.255'
        self.bss.bind(('0.0.0.0', self.recPort))
        self.J = [0.0, 0.0, 0.0]
        self.timeout = 0.0

    def read(self):
        while 1:
            try:
                data, add = self.bss.recvfrom(1000)
                self.J = json.loads(data)
                self.badd = add[0]
                self.timeout = 0.0
            except:
                self.timeout += self.dt
                break
        if(self.timeout > 1): 
            self.J = [0.0, 0.0, 0.0]
        return self.J

    def readOffset(self):
        pass

    def getReset(self) -> bool:
        return False

    def write(self, d):
        txt = json.dumps(d)
        try:
            self.bss.sendto(txt.encode(), (self.badd, self.sendPort))
        except:
            pass

class myJoystic:
    elore = 0.0
    jobbra = 0.0
    forg = 0.0
    xo = 0.0
    yo = 0.0
    zo = 0.0
    sendReset = False
    k = 0.1 #egy kis szures

    def __init__(self, dt) -> None:
        self.k = dt * 5
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            #self.name = self.joystick.get_name()
            self.joyExist = True
            #print("Joystick name: {}".format(self.name) )
        else:
            self.joyExist = False
            print("Nincsen joystick hehehe")

    def read(self):
        if self.joyExist:
            self.jobbra =  -(self.joystick.get_axis(2) + self.xo)
            self.elore = -(self.joystick.get_axis(3) + self.yo)
            self.forg = -(self.joystick.get_axis(0) + self.zo)
        else:
            tmp = 0
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                tmp += 1.0
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                tmp -= 1.0
            self.jobbra += self.k*(tmp - self.jobbra)

            tmp = 0
            if pygame.key.get_pressed()[pygame.K_s]:
                tmp -= 1.0
            if pygame.key.get_pressed()[pygame.K_w]:
                tmp += 1.0
            self.elore += self.k*(tmp - self.elore)

            tmp = 0
            if pygame.key.get_pressed()[pygame.K_a]:
                tmp += 1.0
            if pygame.key.get_pressed()[pygame.K_d]:
                tmp -= 1.0
            self.forg += self.k*(tmp - self.forg)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.sendReset = True
        return [self.elore, self.jobbra, self.forg]
                    
    def readOffset(self):
        i = 0
        xo = 0
        yo = 0
        zo = 0
        while i < 10:
            i +=1
            xo -= self.joystick.get_axis(2)
            yo -= self.joystick.get_axis(3)
            zo -= self.joystick.get_axis(0)
        self.xo = xo / 10.0
        self.yo = yo / 10.0
        self.zo = zo / 10.0

    def getReset(self) -> bool:
        if self.sendReset:
            self.sendReset = False
            return True
        return False

# onalloan is elindithato, akkor kuldi a joystick adatokat UDP-n
# es akkor mar meg is jeleniti amit kap
def main():
    pygame.init()
    font = pygame.font.Font(None, 24)
    joy = myJoystic(dt)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 300), pygame.RESIZABLE)
    joyPort = 6544 # Ez a joystick adatok portja
    recPort = 6546
    bss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    bss.setblocking(False)
    gwadd = netifaces.gateways()[2][0][0]
    b = socket.inet_aton(gwadd)
    badd = f'{b[0]}.{b[1]}.{b[2]}.255'
    bss.bind(('0.0.0.0', recPort))
    datalist = []

    print('Broadcast address:' + badd)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.JOYBUTTONDOWN:
                joy.readOffset()

        J = joy.read() 
        str = json.dumps(J)
        #print(str + '\r', end='', flush=True)
        bss.sendto(str.encode(), (badd, joyPort))

        #most meg ki kell venni az osszes kapott UDP csomagot es kiirni. Sima txt/t kell kapnunk.
        while 1:
            try:
                data, add = bss.recvfrom(1000)
                datalist = json.loads(data)
                badd = add[0]
            except:
                break

        screen.fill(BACKGND)
        pos = 10
        for x in datalist:
            text = font.render(x, True, WHITE, BACKGND)
            screen.blit(text, (10,pos))
            pos += 25

        pygame.display.update()
        clock.tick(50)

if __name__ == "__main__":
    main()

