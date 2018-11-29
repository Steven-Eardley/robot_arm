import pygame, time
from pygame.locals import *

def slow():
    for i in range(0, 200):
        print(i)
        time.sleep(1)

def slow2():
    for i in range(999, 200, -1):
        print(i)
        time.sleep(1)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((1, 1))
    pygame.key.set_repeat(10,10)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("left")
                    #slow()
                elif event.key == pygame.K_RIGHT:
                    print("right")
                    #slow2()
                elif event.key == pygame.K_UP:
                    print("up")
                elif event.key == pygame.K_DOWN:
                    print("down")
                elif event.key == pygame.K_COMMA:
                    print(",")
                elif event.key == pygame.K_PERIOD:
                    print(".")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit();
                    exit(0)

        clock.tick(10)
