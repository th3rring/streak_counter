#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
else:
    print(libdir)

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in7 Demo")
    
    epd = epd2in7.EPD()
    
    '''2Gray(Black and white) display'''
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    font96 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 96)
    
    
    logging.info("Display bitmap and numbers")
    Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, '2in7_Scale.bmp'))
    Himage2.paste(bmp, (0,0))
    draw = ImageDraw.Draw(Himage2)
    draw.text((18,75), '00', font = font96, fill = 0)
    epd.display(epd.getbuffer(Himage2))
    time.sleep(20)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()
