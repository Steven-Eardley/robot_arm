#!/usr/bin/python
import sys
import time
import RPi.GPIO as GPIO
import curses

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
    step_delay = 0.01                                          # 10ms in seconds

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
        self.step_delay = step_delay / 1000.00

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

    def stop(self):
        [GPIO.output(pin, bool(sig)) for (pin, sig) in zip(self.pins, OFF)]

m1 = ArmStepperMotor(ROTPINS, clockwise=False)
m2 = ArmStepperMotor(SH1PINS)
m3 = ArmStepperMotor(SH2PINS)


def main(screen):
    screen.nodelay(True)
    key = ''
    while key != 'q':
        try:
            key = screen.getkey()
        except curses.error:
            pass  # no keypress was ready
        else:
            if key == 'KEY_LEFT':
                m1.step()
            elif key == 'KEY_RIGHT':
                m1.step(forwards=False)
            elif key == 'KEY_UP':
                m2.step()
            elif key == 'KEY_DOWN':
                m2.step(forwards=False)


if __name__ == '__main__':
    curses.wrapper(main)
