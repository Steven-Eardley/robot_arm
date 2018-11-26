#!/usr/bin/python
import sys
import time
import RPi.GPIO as GPIO
import pygame

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins to use for each of the motors.
ROTPINS = (4,17,21,22)
SH1PINS = (10,9,11,7)
SH2PINS = (23,24,25,8)

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
    pins = None
    clockwise = True
    next_step_index = 0
    seq = None

    def __init__(self, pins, clockwise=True, **kwargs):
        self.pins = pins
        for p in self.pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, False)
        global STEPSEQ
        if clockwise:
            self.seq = [list(zip(self.pins, s)) for s in STEPSEQ]
        else:
            self.seq = [list(zip(self.pins, s)) for s in reversed(STEPSEQ)]

    def step(self, forwards=True):
        # Apply the next step instruction to the motor controller
        [GPIO.output(pin, bool(sig)) for (pin, sig) in self.seq[self.next_step_index]]
        if forwards:
            self.next_step_index += 1
        else:
            self.next_step_index -=1

        # Set the index to our next step in the sequence
        if self.next_step_index >= len(self.seq):
            self.next_step_index = 0
        elif self.next_step_index < 0:
            self.next_step_index = len(self.seq) - 1

    def stop(self):
        [GPIO.output(pin, bool(sig)) for (pin, sig) in zip(self.pins, OFF)]

m1 = ArmStepperMotor(ROTPINS, clockwise=False)
m2 = ArmStepperMotor(SH1PINS)
m3 = ArmStepperMotor(SH2PINS)

m1_on = False
pygame.init()
clock = pygame.time.Clock()
while True:
    m1.step(forwards=False)
    clock.tick(100)
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        print("left")
        m1.step()
    if keys[pygame.K_RIGHT]:
        print("right")
        m1.step(forwards=False)
    if keys[pygame.K_ESCAPE]:
        m1.stop()
        exit(0)
    for event in pygame.event.get():
        if m1_on:
            m1.step()
        else:
            m1.stop()
        if event.type == pygame.QUIT:
            m1.stop()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                m1_on = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                m1_on = False
    """
