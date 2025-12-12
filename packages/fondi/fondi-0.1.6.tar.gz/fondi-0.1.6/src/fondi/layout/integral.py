
from .helper import boundingBox
from .layout import Layout, MACROS, WHITESPACESIZE
from ..plain import Symbol
from .supersub import SUBSUPSIZE
from ..mathtext import MathText
from PIL import Image

INTEGRALSYMBOLSIZEFACTOR = 2
INTEGRALSYMBOLASPECTRATIO = .4
INTEGRALLOWEROFFSET = .45

class IntegralLayout(Layout):
    def __init__(self, parent, inner="", dx="", lower="", upper="", symbolFileName:str="integral.png"):
        super().__init__()

        self.inner = MathText(inner, parent.fontSize, color=parent.color)
        self.inner_dx = MathText(dx, parent.fontSize, color=parent.color)

        self.lower = MathText(lower, int(parent.fontSize*SUBSUPSIZE), color=parent.color)
        self.upper = MathText(upper, int(parent.fontSize*SUBSUPSIZE), color=parent.color)

        self.fontSize = parent.fontSize
        self.color = parent.color
        
        self.inner.setBottom(0)

        self.symbol = Symbol(symbolFileName, 
                           INTEGRALSYMBOLASPECTRATIO*INTEGRALSYMBOLSIZEFACTOR*self.fontSize, 
                           INTEGRALSYMBOLSIZEFACTOR*self.fontSize, 
                           self.color
        )
        self.symbol.setLeft(0)
        self.symbol.setCenter(y=0)

        self.upper.setLeft(self.symbol.getRight() + WHITESPACESIZE*self.fontSize)
        self.upper.setCenter(y=self.symbol.getTop())
        
        self.lower.setLeft(self.symbol.getRight() - self.symbol.width*INTEGRALLOWEROFFSET + WHITESPACESIZE*self.fontSize)
        self.lower.setCenter(y=self.symbol.getBottom())

        leftInnerPosition = self.symbol.width + max(self.lower.width, self.upper.width)

        self.inner.setLeft(leftInnerPosition)
        self.inner.setCenter(y=0)

        self.inner_dx.setLeft(leftInnerPosition + self.inner.width + self.fontSize*.3)
        self.inner_dx.setCenter(y=0)

        bbox = boundingBox(self.inner, self.symbol, self.inner_dx, self.lower, self.upper)
    
        self.width = int(bbox[2] - bbox[0])
        self.height = int(bbox[3] - bbox[1])

        self.image = Image.new('RGBA', (self.width, self.height))

        self.symbol.paste(self.image, bbox)
        self.lower.paste(self.image, bbox)
        self.upper.paste(self.image, bbox)
        self.inner.paste(self.image, bbox)
        self.inner_dx.paste(self.image, bbox)

        diff = self.lower.getBottom() - self.inner.getBottom()

        self.setBottomLineDiffrence(diff + self.inner.bottomLineDiffrence)

    def handleSuperSub(parent, body, lower, upper):
        return IntegralLayout(parent, *body, lower=lower, upper=upper)


class ContourIntegralLayout(IntegralLayout):
    def __init__(self, parent, inner="", dx="", lower="", upper=""):
        super().__init__(parent, inner, dx, lower, upper, symbolFileName="contour-integral.png")

    def handleSuperSub(parent, body, lower, upper):
        return IntegralLayout(parent, *body, lower=lower, upper=upper, symbolFileName="contour-integral.png")


MACROS["\\int"] = IntegralLayout
MACROS["\\oint"] = ContourIntegralLayout
