
from PIL import Image, ImageDraw
from .helper import DEBUGFLAG

MACROS = {}
IMGMODE = "RGBA"
WHITESPACESIZE = 0.15

class Layout:
    """
    
    positioner er venstre nederst. Som et normal koordinatsystem

    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.bottomLineDiffrence = 0
        self.hasBottomLineDiffrence = False

    # get
    def getBottom(self):
        return self.y

    def getTop(self):
        return self.y + self.height

    def getLeft(self):
        return self.x

    def getRight(self):
        return self.x + self.width

    def getBoundingBox(self):
        return self.getLeft(), self.getBottom(), self.getRight(), self.getTop()

    # def getCenter(self):
    #     return self.x, self.y

    # set (Used by special layout)
    def setRight(self, x):
        self.x = x - self.width

    def setLeft(self, x):
        self.x = x
    
    def setTop(self, y):
        self.y = y - self.height

    def setBottom(self, y):
        self.y = y

    def setBottomLineDiffrence(self, dy):
        self.hasBottomLineDiffrence = True
        self.bottomLineDiffrence = dy

    def setCenter(self, x=None, y=None):
        if x is not None: self.x = x - self.width/2
        if y is not None: self.y = y - self.height/2

    def drawBottomLineDiffrenceHelper(self):
        draw = ImageDraw.ImageDraw(self.image, IMGMODE)
        draw.line((0, self.height+self.bottomLineDiffrence-2, self.width, self.height+self.bottomLineDiffrence-2), (255,0,0,255), 2)

    def drawBoundingBox(self):
        draw = ImageDraw.ImageDraw(self.image, IMGMODE)
        draw.line((0, 0, self.width-1, 0, self.width-1, self.height-1, 0, self.height-1, 0, 0), (0,0,255,255), 2)
        

    def paste(self, surface:Image.Image, offset:tuple=(0,0)):
        """ paste self into image """
        return surface.paste(self.image, (int(self.getLeft()-offset[0]), surface.height - int(self.getTop()-offset[1])))


    def prepPasteLeft(self, lastobj=0): # used by MathText
        self.x = lastobj.getRight() + WHITESPACESIZE * self.fontSize
        
        if DEBUGFLAG: self.drawBoundingBox()
        
        if self.hasBottomLineDiffrence:
            
            if DEBUGFLAG: self.drawBottomLineDiffrenceHelper()

            self.y = self.bottomLineDiffrence
    
    
    def handleSuperSub(self, parent, body, lower="", upper=""):
        """must return True when functions is handled in macro and not by the SuperSubLayout"""
        return False

    def copy(self, target):
        # copy all from target to own
        self.image = target.image
        self.x = target.x
        self.y = target.y
        self.hasBottomLineDiffrence = target.hasBottomLineDiffrence
        self.bottomLineDiffrence = target.bottomLineDiffrence
        self.width = target.width
        self.height = target.height
        self.fontSize = target.fontSize
        self.color = target.color