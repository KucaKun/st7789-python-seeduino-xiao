import time
import board
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

clock = board.SCL() # D5 clock
data = board.SDA() # D4 data
 

try:
    ctr = 0
    while True:
        clock.value = ctr%2
        data.value = False
        ctr += 1
        time.sleep(0.01)

except Exception as ex:
    while True:
        print(str(ex))
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)


