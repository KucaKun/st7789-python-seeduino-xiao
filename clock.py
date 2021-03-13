#!/usr/bin/env python3
import usb.core
import usb.util
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageGrab
import struct
import pause
import datetime
import numpy

def findusb():
    dev = usb.core.find(idVendor=0x03eb, idProduct=0x2040)
    if dev is None:
        print("Not found!")
        exit(1)

    dev.set_configuration()
    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]
    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)
    return (dev,ep)

def sendimage(dev,im):
    im = im.convert("RGB")

    data=struct.pack("<HHHH",0,0,im.width,im.height)
    dev[0].ctrl_transfer(usb.util.CTRL_RECIPIENT_INTERFACE|usb.util.CTRL_TYPE_VENDOR|usb.util.CTRL_OUT,1,data_or_wLength=data)

    #data = []
    #for r,g,b in im.getdata():
    #    color=((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    #    data.extend(struct.pack(">H",color))

    #dev[1].write(data)
    data=numpy.array(im)
    R5 = (data[...,0]>>3).astype(numpy.uint16) << 11
    G6 = (data[...,1]>>2).astype(numpy.uint16) << 5
    B5 = (data[...,2]>>3).astype(numpy.uint16)
    RGB565 = R5 | G6 | B5
    dev[1].write(RGB565.astype('>i2').tobytes())

lcd=findusb()
fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 40)
MAX_SIZE = (240,180)

im=Image.new('RGB', (240,240), color=(0,0,0))


def getFrame():
    img=ImageGrab.grab()
    img.thumbnail(MAX_SIZE)
    return img

while True:
    im2=im.copy()
    d = ImageDraw.Draw(im2)
    dat=datetime.datetime.now()
    d.text((10,0),dat.strftime("%H:%M:%S"),font=fnt,fill=(255,255,255))
    im2.paste(getFrame(),(0,60))
    im2=im2.transpose(Image.ROTATE_180)
    sendimage(lcd,im2)
    dat2=dat.replace(microsecond=0) + datetime.timedelta(seconds=1)
