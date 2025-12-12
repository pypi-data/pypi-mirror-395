
from ..plain import Image as LayoutImage 
from .helper import boundingBox
from .layout import Layout, IMGMODE, MACROS, WHITESPACESIZE
from ..plain import Symbol
from ..mathtext import MathText
from PIL import Image, ImageDraw
import math

class SqrtLayout(Layout):
    def __init__(self, parent, *args):
        super().__init__()

        if len(args) == 2:
            print(args)

        self.inner = MathText(args[0], parent.fontSize, color=parent.color)

        self.linewidth = 3
        self.fontSize = parent.fontSize
        self.color = parent.color
        self.padding = self.fontSize//5
        self.height = int(self.inner.height+self.padding)

        self.angle = math.radians(60)

        c = self.inner.height/math.sin(self.angle)
        line1 = (0,self.height/2), (math.cos(self.angle)*c/2, self.height)
        line2 = line1[1], (math.cos(self.angle)*c+line1[0][0], 0)

        self.width = int(self.inner.width + self.linewidth*2 + line2[1][0] + self.padding)

        line3 = line2[1], (self.width, line2[1][1])
        
        lines = *line1, *line2, *line3

        self.inner.setBottom(0)
        self.inner.setLeft(line3[0][0]+self.padding/2)

        self.image = Image.new('RGBA', (self.width, self.height))
        draw = ImageDraw.ImageDraw(self.image)

        self.inner.paste(self.image, (0,0))

        draw.line(lines, fill=self.color, width=self.linewidth, joint="curve")


MACROS["\\sqrt"] = SqrtLayout
