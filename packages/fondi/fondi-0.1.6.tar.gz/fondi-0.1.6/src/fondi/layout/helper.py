
from PIL import ImageDraw, Image, ImageFont
import math


import sys
DEBUGFLAG = '--debug' in sys.argv


# layout
def getTextDimension(text, fontSize):

    winSize = (fontSize*2*len(text),fontSize*2*len(text))
    pilImage = Image.new("RGBA", winSize, color=(0,0,0,0))
    draw = ImageDraw.Draw(pilImage)
    font = ImageFont.truetype("cmu.serif-roman.ttf", fontSize)
    draw.text((winSize[0]//2, winSize[1]//2), text, (255, 255, 255, 255), font=font)

    pilImage = pilImage.crop(pilImage.getbbox())
    return pilImage.width, pilImage.height    


def boundingBox(*objs):
    
    bounding = [math.inf, math.inf, -math.inf, -math.inf]
    for obj in objs:
        x, y, x1, y1 = obj.getBoundingBox()
        bounding[0] = min(bounding[0], x)
        bounding[1] = min(bounding[1], y)
        bounding[2] = max(bounding[2], x1)
        bounding[3] = max(bounding[3], y1)

    return bounding

