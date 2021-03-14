from time import sleep
import board, sys
import st7789 as st
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

clock = DigitalInOut(board.D5) # D5 clock
clock.direction = Direction.OUTPUT

data = DigitalInOut(board.D4) # D4 data
data.direction = Direction.OUTPUT

dc = DigitalInOut(board.D7) # D7 data command
dc.direction = Direction.OUTPUT
sleep(3)
try:
    def sendCommand(argsTuple):
        first = True
        for arg in argsTuple:
            if first:
                dc.value = False # command 
                first = False
            else:
                dc.value = True # argument

            for i in range(7, -1, -1):
                # Send one bit
                data.value = (arg & (1<<i)) != 0
                
                # Cycle the clock
                clock.value = True
                clock.value = False

    def sendPixel(r, g, b):
        # R 0-32
        # G 0-64
        # B 0-32
        dc.value = True
        for i in range(15, -1, -1):
            if i > 10:
                color = r << 10
            elif i > 5:
                color = g << 5
            else:
                color = b

            # Send one bit
            data.value = (color & (1<<i)) != 0
            # Cycle the clock
            clock.value = True
            clock.value = False
    
    def initializeScreen():
        initCommands = [
            (st.SWRESET,),
            (st.DELAY, 150),

            (st.SLPOUT,),
            (st.DELAY, 500),

            (st.COLMOD, 0x55),
            (st.DELAY, 10),

            (st.MADCTL, 0x00),
            (st.DELAY, 10),
            (st.CASET, 0x00, 0x00, 0xF0>>8, 0xF0), # 0, 0, 240, 240
            (st.DELAY, 10),
            (st.RASET, 0x00, 0x00, 0xF0>>8, 0xF0), # 0, 0, 240, 240
            (st.DELAY, 10),

            (st.INVON,),
            (st.DELAY, 10),

            (st.NORON,),
            (st.DELAY, 10),

            (st.DISPON,),
            (st.DELAY, 500),
        ]
        for command in initCommands:
            if command[0] == st.DELAY:
                print("sleep")
                sleep(command[1]*0.001)
            else:
                print(command)
                sendCommand(command)
    
    initializeScreen()
    sendCommand((st.RAMWR,))
    sleep(0.001)
    while True:
        sendPixel(30, 30, 30)
        sleep(0.0001)
except Exception as ex:
    sys.print_exception(ex)
    while True:
        led.value = True
        sleep(0.1)
        led.value = False
        sleep(0.1)


