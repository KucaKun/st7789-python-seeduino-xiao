import time
import board
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

clock = board.SCL() # D5 clock
data = board.SDA() # D4 data
dc = board.DigitalInOut(board.D7) # D7 data command
dc.direction = Direction.OUTPUT


try:
    def send(command):
        dc.value = False # command

        for i in range(7, -1, -1):
            # Send one bit
            data.value = (command & (1<<i)) != 0
            
            # Cycle the clock
            clock.value = True
            clock.value = False

    def sendPixel(r, g, b):
        # R 0-32
        # G 0-64
        # B 0-32
        dc.value = True # data

        counter = 0x01 << 16
        for i in range(16, 0, -1):
            if i > 10:
                color = r << 10
            elif i > 5:
                color = g << 5
            else:
                color = b
            # Send one bit
            data.value = (color & counter) == 0x01 << i
            counter = counter >> 1 
            
            # Cycle the clock
            clock.value = True
            clock.value = False

    # rim 0 3Ah db6:4 101


except Exception as ex:
    while True:
        print(str(ex))
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)


