
from .layout import *
from ..mathtext import MathText
from ..plain.helper import replaceColorRandom
from ..plain import Symbol
from .parenthesis import PARATUBORWIDTHCOEFF
from .helper import boundingBox
from PIL import Image
import math

DISTSPACE = .75
PARAPADDING = 0.25
DISTLINES = 2

class Cases(Layout):

    def __init__(self, parent, *args):
        super().__init__()
        
        # ---prep cases---
        if len(args) % 2 == 0:
            cases = [(args[i*2], args[i*2+1]) for i in range(len(args)//2)]
        else:
            cases = [(args[i*2], args[i*2+1]) for i in range(len(args)//2-1)] + [(args[-1], 'else')]

        self.fontSize = parent.fontSize
        self.color = parent.color
        
        self.cases = []
        for case, para in cases:
            left = MathText(case, self.fontSize, self.color)
            left.setLeft(0)
            right = MathText(para, self.fontSize, self.color)
            self.cases.append(
                (left, right, max(left.height, right.height))
            )

        # draw
        maxWidth = math.ceil(max([i[0].width for i in self.cases]))
        
        GAPSIZE = WHITESPACESIZE * self.fontSize * DISTLINES
        sumHeight = parent.fontSize * PARAPADDING
        for left, right, height in self.cases:
            sumHeight += height
            right.setLeft(maxWidth+DISTSPACE*self.fontSize)
            right.setBottom(-sumHeight)
            left.setBottom(-sumHeight)
            sumHeight += GAPSIZE

        sumHeight += parent.fontSize * PARAPADDING - GAPSIZE
        self.para = Symbol('tuborpara_left.png', PARATUBORWIDTHCOEFF*self.fontSize, int(sumHeight), self.color)
        self.para.setRight(self.cases[0][0].getLeft()-WHITESPACESIZE*self.fontSize)
        self.para.setTop(0)

        self.height = sumHeight

        x, y, x1, y1 = boundingBox(self.para, *[i[0] for i in self.cases], *[i[1] for i in self.cases])

        self.offset = (x,y)
        self.width = x1 - x
        self.height = y1 - y
        self.image = Image.new(IMGMODE, (int(self.width), int(self.height)))

        self.para.paste(self.image, self.offset)
        for left, right, _ in self.cases:
            left.paste(self.image, self.offset)
            right.paste(self.image, self.offset)

        self.setBottomLineDiffrence(-self.height/2 + self.fontSize/4) # HVORFOR 4????

        #self.image.save('debug/cases.png')


MACROS["\\cases"] = Cases

#     "\\frac": FracLayout,
#     "\\super": SuperLayout,
#     "\\sub": SubLayout,
#     "\\supersub": SuperSubLayout,
#     "\\subsuper": SubSuperLayout,
#     "\\para": ParenthesisLayout


