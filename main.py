from time import sleep
import board
import sys
import st7789 as st
from digitalio import DigitalInOut, Direction, DriveMode

sleep(1)
power = DigitalInOut(board.D5)
power.direction = Direction.OUTPUT
power.value = True
sleep(1)
reset = DigitalInOut(board.D6)
reset.switch_to_output(value=True)

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

spi = board.SPI()
while not spi.try_lock():
    pass
spi.configure(baudrate=100000)
spi.unlock()

dc = DigitalInOut(board.D7)
dc.direction = Direction.OUTPUT
sleep(1)


def sendCommand(argsTuple):
    first = True
    while not spi.try_lock():
        pass
    for arg in argsTuple:
        if first:
            dc.value = False  # command
            first = False
        else:
            dc.value = True  # argument

        spi.write(bytearray([arg]))
    spi.unlock()


def sendPixel(r, g, b):
    # R 0-32
    # G 0-64
    # B 0-32
    while not spi.try_lock():
        pass
    dc.value = True
    color = (r << 10) + (g << 5) + b
    colorHighByte = color >> 8
    colorLowByte = color & 0x0f
    spi.write(bytearray([colorHighByte]))
    spi.write(bytearray([colorLowByte]))
    spi.unlock()
    sleep(0.01)


def initializeScreen():
    initCommands = [
        (st.SWRESET,),
        (st.DELAY, 150),

        (st.SLPOUT,),
        (st.DELAY, 500),

        (st.COLMOD, 0x55),
        (st.DELAY, 10),

        (st.MADCTL, 0x00),
        (st.CASET, 0x00, 0x00, 0xF0 >> 8, 0xF0),  # 0, 0, 240, 240
        (st.DELAY, 10),
        (st.RASET, 0x00, 0x00, 0xF0 >> 8, 0xF0),  # 0, 0, 240, 240
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
            print("sleep", command[1]*0.001)
            sleep(command[1]*0.001)
        else:
            print(command)
            sendCommand(command)


led.value = True
initializeScreen()
led.value = False

sendCommand((st.RAMWR,))
sleep(0.01)
while True:
    sendPixel(30, 30, 30)
