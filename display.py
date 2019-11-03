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

class Display:

    def __init__(self):
        self.epd = epd2in7.EPD()
        
        logging.info("init and Clear")
        self.epd.init()
        self.epd.Clear(0xFF)
        
        self.font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        self.font96 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 96)

        self.bmp = Image.open(os.path.join(picdir, '2in7_Scale.bmp'))

    def show(self, weeks, to_go, per_week):
        self.epd.Clear(0xFF)

        image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
        image.paste(self.bmp, (0,0))

        draw = ImageDraw.Draw(image)
        draw.text((10,-12), '{:02d}'.format(weeks), font = font96, fill = 0)
        draw.text((147,-12), str(to_go), font = font96, fill = 0)
        draw.text((160,142), str(per_week), font = font18, fill = 0)
        self.epd.display(self.epd.getbuffer(image))

        self.epd.sleep()


display = Display()
display.show(0,4,4)


