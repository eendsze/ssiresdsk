#!/usr/bin/env python
# encoding: utf-8
import pygame
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