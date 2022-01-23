from time import sleep
import board
from digitalio import DigitalInOut, Direction, DriveMode


def hang():
    while True:
        sleep(0.1)
        led.value = True
        sleep(0.1)
        led.value = False


led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
dc = DigitalInOut(board.D7)
dc.direction = Direction.OUTPUT
reset = DigitalInOut(board.D6)
reset.switch_to_output(value=True, drive_mode=DriveMode.PUSH_PULL)
power = DigitalInOut(board.D5)
power.direction = Direction.OUTPUT
power.value = True
reset.value = False
sleep(0.1)
reset.value = True
sleep(0.3)

spi = board.SPI()
sleep(0.1)
led.value = True
sleep(0.1)
led.value = False

while not spi.try_lock():
    pass
spi.configure(baudrate=100)  # Configure SPI for 24MHz
spi.unlock()
_INIT_SEQUENCE = (
    b"\x01\x80\x96",  # _SWRESET and Delay 150ms
    b"\x11\x80\xFF",  # _SLPOUT and Delay 500ms
    b"\x3A\x81\x55\x0A",  # _COLMOD and Delay 10ms
    b"\x36\x01\x08",  # _MADCTL
    b"\x21\x80\x0A",  # _INVON Hack and Delay 10ms
    b"\x13\x80\x0A",  # _NORON and Delay 10ms
    b"\x36\x01\xC0",  # _MADCTL
    b"\x29\x80\xFF",  # _DISPON and Delay 500ms
)


def sendCommand(data):
    command = bytearray(data[0])
    args = bytearray(data[1:len(data)])
    no_args = False
    if args[0] == 0x80:
        sleep(args[1] / 1000)
        no_args = True
    spi.try_lock()
    dc.value = False  # command
    sleep(0.1)
    spi.write(command)
    dc.value = True  # argument
    sleep(0.1)
    if not no_args:
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
    spi.write(bytearray([colorLowByte]))
    spi.write(bytearray([colorHighByte]))
    spi.unlock()


for cmd in _INIT_SEQUENCE:
    sendCommand(cmd)

for i in range(31):
    sendPixel(i, i, i)

hang()
