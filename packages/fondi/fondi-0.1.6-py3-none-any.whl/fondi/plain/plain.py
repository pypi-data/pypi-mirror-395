
from PIL import ImageDraw, Image, ImageFont
from ..layout import Layout
from .helper import replaceColorRandom
import os
from ..fileloader import loadFile

REGULAR = set(['+', '-', '>', '<', '=', '·', '{', '}', '(', ')', '[', ']'])

def isNum(x:str) -> bool:
    try:
        float(x)
        return True
    except ValueError:
        return False

# ------------------------------------------------------------------------------
# |                               Standard Text                                |
# ------------------------------------------------------------------------------
# tal må ikke være italic!
class PlainText(Layout):
    
    def __init__(self, text, fontSize, color, center=False, italic=True):
        super().__init__()

        lowerOffset = 0

        self.text = text
        self.fontSize = fontSize
        self.color = color

        winSize = (fontSize*3*len(text),fontSize*3*len(text))
        self.image = Image.new("RGBA", winSize, color=(0,0,0,0))
        
        if len(text) == 0:
            self.width = 0
            self.height = 0
            return

        draw = ImageDraw.Draw(self.image)
        
        if isNum(text) or text in REGULAR or (not italic):
            font = ImageFont.truetype(loadFile("NewCM10-Regular.otf"), fontSize)
        else:
            font = ImageFont.truetype(loadFile("NewCM10-Italic.otf"), fontSize)
        
        draw.text((winSize[0]//2, winSize[1]//2), text, self.color, font=font, anchor="ms")
        
        bbox = self.image.getbbox()
        lowerOffset = bbox[3] - winSize[1]//2

        
        # if any([i in text for i in 'pqjy']):
        #     lowerOffset += fontSize*0

        # if 'q' in text:
        #     lowerOffset += 20

        #self.image.save('debug/no-crop-{}.png'.format(text))
        bbox = list(bbox)
        if text[0] == " ":
            bbox[0] -= fontSize*0.25
        if text[-1] == " ":
            bbox[2] += fontSize*0.25


        self.image = self.image.crop(bbox)
        
        self.width = self.image.width
        self.height = self.image.height

        self.setBottomLineDiffrence(-lowerOffset)

        self.image = replaceColorRandom(self.image)
        #self.image.save('debug/test-plain-{}.png'.format(str(self.text)))


    def __repr__(self):
        return self.text
