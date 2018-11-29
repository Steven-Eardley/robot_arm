#!/usr/bin/python
import sys
import time
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *

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
    step_delay = 0
    halt = False

    def __init__(self, pins, clockwise=True, step_delay=10, **kwargs):
        self.pins = pins
        for p in self.pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, False)
        global STEPSEQ
        if clockwise:
            self.seq = [list(zip(self.pins, s)) for s in STEPSEQ]
        else:
            self.seq = [list(zip(self.pins, s)) for s in reversed(STEPSEQ)]
        self.step_delay = step_delay / float(1000)

    def step(self, forwards=True):
        # Apply the next step instruction to the motor controller
        [GPIO.output(pin, bool(sig)) for (pin, sig) in self.seq[self.next_step_index]]
        time.sleep(self.step_delay)
        if forwards:
            self.next_step_index += 1
        else:
            self.next_step_index -=1

        # Set the index to our next step in the sequence
        if self.next_step_index >= len(self.seq):
            self.next_step_index = 0
        elif self.next_step_index < 0:
            self.next_step_index = len(self.seq) - 1

    def spin(self, forwards=True):
        while self.halt is False:
            self.step(forwards=forwards)
        self.halt = False

    def stop(self):
        self.halt = True
        global OFF
        [GPIO.output(pin, bool(sig)) for (pin, sig) in list(zip(self.pins, OFF))]
        self.halt = False

if __name__ == '__main__':
    m1 = ArmStepperMotor(ROTPINS, clockwise=False)
    m2 = ArmStepperMotor(SH1PINS)
    m3 = ArmStepperMotor(SH2PINS, clockwise=False)

    pygame.init()
    pygame.key.set_repeat(0, 10)
    pygame.display.set_mode((1, 1))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    m1.step(forwards=False)
                elif event.key == pygame.K_RIGHT:
                    m1.step()
                elif event.key == pygame.K_UP:
                    m2.step(forwards=False)
                elif event.key == pygame.K_DOWN:
                    m2.step()
                elif event.key == pygame.K_COMMA:
                    m3.step(forwards=False)
                elif event.key == pygame.K_PERIOD:
                    m3.step()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit();
                    exit(0)

        clock.tick(10)
