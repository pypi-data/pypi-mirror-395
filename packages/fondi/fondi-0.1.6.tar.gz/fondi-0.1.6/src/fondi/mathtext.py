
from .parser.tokens import *
from .layout.helper import boundingBox
from .plain.helper import replaceColorRandom
from .plain import PlainText, Symbol
from .layout import Layout
from .parser import *
from .layout import *

from PIL import Image
import time

"""

For hvert nyt objekt laves et nyt koordinatsystem

"""

# ------------------------------------------------------------------------------
# |                             Text with parser                               |
# ------------------------------------------------------------------------------
class MathText(Layout):

    def __init__(self, text, fontSize, color):
        super().__init__()

        startTime = time.time()

        self.text = text
        self.fontSize = fontSize
        self.color = color

        self.line: list = [] #for plus og minus

        self.__parse__(text)
        self.__draw__()

        #print('Tid ({}):'.format(text),round((time.time() - startTime)*1000, 2),'ms')

    
    def __parse__(self, text):
        

        # 0,4x^{3}+2*x^{2}+5*x+c_{0}
        # #super{0,4x}{3}#super{+2x}{2}#sub{+5*x+c_}{0}
        # just in time compiler?
        text = text.replace('*', '·')
        tokens = parse(text)

        self.line = []
        for clss, tok in tokens:
            if tok == " " or tok == "": continue
            
            if clss == PLAINTEXT: # it is not an argument
                self.line.append(PlainText(tok.replace('{','').replace('}', ''), self.fontSize, self.color))

            elif clss == ARGUMENT:
                self.line.append(MathText(tok, self.fontSize, self.color))

            elif clss == FULLCOMMAND:
                self.line.append(MACROS[tok["name"]](self, *tok["args"]))
    
            elif clss == OPERATION:
                self.line.append(PlainText(tok.replace('{','').replace('}', ''), self.fontSize, self.color, center=True))


    def __repr__(self):
        s = ''
        for i in self.line:
            s += repr(i)
        return s


    def __draw__(self):
        # self.image = Image.new(IMGMODE, (int(self.width), int(self.height)))
        if len(self.text) == 0:
            self.image = Image.new(IMGMODE, (0, 0))
            self.width = 0
            self.height = 0
            return

        maxCenterLine = 0
        for i, obj in enumerate(self.line): #objects ready to be assembled to the right
            obj.prepPasteLeft(self.line[i-1])
            maxCenterLine = min(maxCenterLine, obj.bottomLineDiffrence)

        self.setBottomLineDiffrence(maxCenterLine)

        x, y, x1, y1 = boundingBox(*self.line)
        self.width = x1 - x
        self.height = y1 - y

        self.image = Image.new(IMGMODE, (int(self.width), int(self.height)))

        for i, obj in enumerate(self.line): #objects ready to be assembled to the right
            obj.paste(self.image, (x,y))

        # self.image = self.image.crop(self.image.getbbox())
        self.image = replaceColorRandom(self.image)
        #self.image.save('debug/test-{}.png'.format(self.text))
