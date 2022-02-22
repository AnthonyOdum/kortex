#!/usr/bin/env python3

import random
from time import sleep

def pulse():
    num = random.randrange(0,100)

    if(num < 50):
        print('{} is less than half'.format(num))
    elif(num > 50):
        print('{} is more than half'.format(num))

def robotics_test():
    print('Starting pulse in: ')
    for i in reversed(range(3)):
        print('{} seconds'.format(i+1))
        sleep(1)
    pulse()

if __name__ == "__robotics_test__":
    robotics_test()