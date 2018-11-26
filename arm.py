#!/usr/bin/python
import sys
import time
import pygame
import RPi.GPIO as GPIO

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO pins to use for each of the motors.
ROTPINS = [4,17,21,22]
SH1PINS = [10,9,11,7]
SH2PINS = [23,24,25,8]

# Half step sequence
STEPSEQ = [[1,0,0,1],
           [1,0,0,0],
           [1,1,0,0],
           [0,1,0,0],
           [0,1,1,0],
           [0,0,1,0],
           [0,0,1,1],
           [0,0,0,1]]

OFF = [0,0,0,0]

class ArmStepperMotor(object):
    pins = []
    clockwise = True
    step_delay = 0.01 #seconds
    next_step_index = 0
    seq = []
    
    def __init__(pins, delay=10, clockwise=True, **kwargs):
        self.pins = pins
        for p in self.pins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        self.stepDelay = delay / 1000.00
        if clockwise:
            seq = [zip(self.pins, s) for s in STEPSEQ]
        else:
            seq = [zip(self.pins, s) for s in reversed(STEPSEQ)]
        
    def step(forwards=True):
        # Apply the next step instruction to the motor controller
        for inst_set in seq[self.next_step_index]:
            [GPIO.output(pin, bool(sig)) for (pin, sig) in inst_set]
            time.sleep(self.stepDelay)
        if forwards:
            self.next_step_index += 1
        else:
            self.next_step_index -=1
        
        # Set the index to our next step in the sequence
        if self.next_step_index >= len(self.seq):
            self.next_step_index = 0
        elif self.next_step_index < 0:
            self.next_step_index = len(self.seq - 1)
            
    def stop()
        [GPIO.output(pin, bool(sig)) for (pin, sig) in zip(self.pins, OFF)]
            


m1 = ArmStepperMotor(pins=ROTPINS)
m2 = ArmStepperMotor(pins=SH1PINS)
m3 = ArmStepperMotor(pins=SH2PINS)


pygame.key.init()
while True:
    keys = pygame.key.get_pressed()
    print(keys)
    if keys[pygame.K_LEFT]:
        m1.step()
    if keys[pygame.K_RIGHT]:
        m1.step(forwards=False)
    if keys[pygame.K_ESCAPE]:
        m1.stop()
        exit(0)
    