from time import sleep
import board, sys
import st7789 as st
from digitalio import DigitalInOut, Direction

sleep(1)

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value=False

spi = board.SPI()

dc = DigitalInOut(board.D7) # D7 data command
dc.direction = Direction.OUTPUT
sleep(1)


try:
    def sendCommand(data):
        command = bytearray([data[0]])
        args = bytearray(data[1:len(data)])
        print("Command:", data)

        spi.try_lock()
        dc.value = False # command 
        sleep(0.1)
        spi.write(command)
        dc.value = True # argument
        sleep(0.1)
        spi.write(args)
        spi.unlock()
        

    def sendPixel(r, g, b):
        # R 0-32
        # G 0-64
        # B 0-32
        spi.try_lock()
        dc.value = True
        color = (r << 10) + (g << 5) + b
        colorHighByte = color >> 8
        colorLowByte = color & 0x0f
        spi.write(bytearray([colorLowByte, colorHighByte]))
        spi.unlock()
    
    def initializeScreen():
        initCommands = [
            [st.SLPOUT,],
            [st.DELAY, 500],

            [st.SWRESET,],
            [st.DELAY, 150],
            [st.SWRESET,],
            [st.DELAY, 150],

            [st.SLPOUT,],
            [st.DELAY, 500],

            [st.COLMOD, 0x55],
            [st.DELAY, 10],

            [st.MADCTL, 0x00],
            [st.DELAY, 10],
            [st.CASET, 0x00, 0x00, 0xF0>>8, 0xF0], # 0, 0, 240, 240
            [st.DELAY, 10],
            [st.RASET, 0x00, 0x00, 0xF0>>8, 0xF0], # 0, 0, 240, 240
            [st.DELAY, 10],

            [st.INVON,],
            [st.DELAY, 10],

            [st.NORON,],
            [st.DELAY, 10],

            [st.DISPON,],
            [st.DELAY, 500],
        ]
        for command in initCommands:
            if command[0] == st.DELAY:
                delayTime = command[1]*0.001
                print("Sleep:", delayTime)
                sleep(delayTime)
            else:
                sendCommand(command)
    
    led.value = True
    initializeScreen()
    led.value = False

    sendCommand([st.RAMWR])
    sleep(0.1)
    while True:
        led.value = False
        #sendPixel(30, 30, 30)
        sleep(1)
        initializeScreen()
        led.value = True
except Exception as ex:
    sys.print_exception(ex)
    while True:
        led.value = True
        sleep(0.1)
        led.value = False
        sleep(0.1)


