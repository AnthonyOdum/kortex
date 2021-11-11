#!/usr/bin/env python3

import random
from time import sleep

def pulse():
    num = random.randrange(0,100)

    if(num < 50):
        print('{} is less than half'.format(num))
    elif(num > 50):
        print('{} is more than half'.format(num))

def main():
    print('Starting pulse in: ')
    for i in reversed(range(3)):
        sleep(1)
        print('{} seconds'.format(i+1))
    pulse()

if __name__ == "__main__":
    main()