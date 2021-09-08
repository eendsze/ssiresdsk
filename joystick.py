#!/usr/bin/env python

import pygame


class myJoystic:
    elore = 0.0
    jobbra = 0.0
    forg = 0.0
    xo = 0.0
    yo = 0.0
    zo = 0.0
    sendReset = False

    def __init__(self) -> None:
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
            self.jobbra = 0.0
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.jobbra += 1.0
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.jobbra -= 1.0
            self.elore = 0.0
            if pygame.key.get_pressed()[pygame.K_s]:
                self.elore -= 1.0
            if pygame.key.get_pressed()[pygame.K_w]:
                self.elore += 1.0
            self.forg = 0.0
            if pygame.key.get_pressed()[pygame.K_a]:
                self.forg += 1.0
            if pygame.key.get_pressed()[pygame.K_d]:
                self.forg -= 1.0
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




"""
pygame.init()
clock = pygame.time.Clock()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    name = joystick.get_name()
    print("Joystick name: {}".format(name) )
else:
    print("Nincsen joystick hehehe")
    exit()


axes = joystick.get_numaxes()
while True:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    
    for i in range( axes ):
    # pygame.joystick.Joystick.get_axis
        axis = joystick.get_axis( i )
        print("Axis {} value: {:>6.3f}".format(i, axis) )
    clock.tick(3)

    """