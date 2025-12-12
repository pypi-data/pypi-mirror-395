
from .layout import *
from ..mathtext import MathText
from ..plain.helper import replaceColorRandom
from .helper import boundingBox
from PIL import Image, ImageDraw

FRACFONTWIDTHCOEFF = 0.05
FRACPADDINGCOEFF = 0.1
FRACSHRINKCOEFF = 0.75

class FracLayout(Layout):

    def __init__(self, parent, top, bottom):
        super().__init__()

        self.fontSize = parent.fontSize
        self.color = parent.color

        self.top = MathText(top, int(self.fontSize*FRACSHRINKCOEFF), self.color)
        self.bottom = MathText(bottom, int(self.fontSize*FRACSHRINKCOEFF), self.color)

        linewidth = int(FRACFONTWIDTHCOEFF * self.fontSize)
        self.padding = FRACPADDINGCOEFF * self.fontSize + linewidth/2
        self.width = max(self.bottom.width, self.top.width)
        self.height = self.bottom.height + self.top.height + self.padding * 2


        # draw
        self.image = Image.new(IMGMODE, (int(self.width), int(self.height)))

        self.top.setBottom(self.padding)
        self.top.setCenter(x=self.width/2)
        
        self.bottom.setTop(-self.padding)
        self.bottom.setCenter(x=self.width/2)

        x, y, x1, y1 = boundingBox(self.bottom, self.top)
        self.setBottomLineDiffrence(y + self.fontSize/4)

        # paste
        self.top.paste(self.image, (x,y))
        self.bottom.paste(self.image, (x,y))

        # draw line
        imd = ImageDraw.ImageDraw(self.image)
        imd.line((0, self.height+y, self.width, self.height+y), self.color, width=linewidth)

        self.image = replaceColorRandom(self.image)
        #self.image.save('debug/test-frac.png')


    def __repr__(self):
        return '({})/({})'.format(self.top, self.bottom)

MACROS["\\frac"] = FracLayout

#     "\\frac": FracLayout,
#     "\\super": SuperLayout,
#     "\\sub": SubLayout,
#     "\\supersub": SuperSubLayout,
#     "\\subsuper": SubSuperLayout,
#     "\\para": ParenthesisLayout
