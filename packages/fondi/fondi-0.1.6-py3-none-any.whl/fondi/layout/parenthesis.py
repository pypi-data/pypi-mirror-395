
from ..plain import Image as LayoutImage 
from .helper import boundingBox
from .layout import Layout, IMGMODE, MACROS, WHITESPACESIZE
from ..plain import Symbol
from ..mathtext import MathText
from PIL import Image, ImageDraw

# stroke width
FONTSIZELINEWIDTH = 0.05

# height
PARAHEIGHTCOEFF = 1.2

# width
PARANORMALWIDTHCOEFF = 0.2
PARASQUAREWIDTHCOEFF = 0.5
PARATUBORWIDTHCOEFF = 0.4


class ParenthesisLayout(Layout):
    def __init__(self, parent, inner, openFname='normpara_left.png', closeFname='normpara_right.png'):
        super().__init__()

        self.fontSize = parent.fontSize
        self.color = parent.color

        self.inner = MathText(inner, self.fontSize, self.color)
        self.inner.setCenter(0,self.inner.bottomLineDiffrence*.25)
        
        #paraheight = max(self.inner.height + self.inner.centerline, int(self.fontSize * PARAHEIGHTCOEFF))
        paraheight = max(self.inner.height, int(self.fontSize * .5))
        
        self.left = Symbol(openFname, PARANORMALWIDTHCOEFF*self.fontSize, paraheight, self.color)
        self.left.setCenter(y=0)
        self.left.setRight(self.inner.getLeft()-WHITESPACESIZE*self.fontSize)
        
        self.right = Symbol(closeFname, PARANORMALWIDTHCOEFF*self.fontSize, paraheight, self.color)
        self.right.setCenter(y=0)
        self.right.setLeft(self.inner.getRight()+WHITESPACESIZE*self.fontSize)

        x, y, x1, y1 = boundingBox(self.inner, self.left, self.right)

        self.offset = (x,y)
        self.width = x1 - x
        self.height = y1 - y

        self.image = Image.new(IMGMODE, (int(self.width), int(self.height)))
        
        self.left.paste(self.image, self.offset)
        self.right.paste(self.image, self.offset)
        self.inner.paste(self.image, self.offset)

        #self.image.save('para.png')

        self.setBottomLineDiffrence(self.inner.bottomLineDiffrence)

# class ParenthesisLayout:
#     def __init__(self, parent, inner):
#         super().__init__(parent, inner, 'normpara_left.png', 'normpara_right.png')


class SquareParenthesisLayout(Layout):
    def __init__(self, parent, inner):
        super().__init__()

        self.fontSize = parent.fontSize
        self.color = parent.color

        self.inner = MathText(inner, self.fontSize, self.color)
        self.inner.setCenter(0,0)

        image = Image.new(IMGMODE, (int(PARANORMALWIDTHCOEFF*self.fontSize), int(self.inner.height)+8))
        imd = ImageDraw.ImageDraw(image)
        thickness = int(self.fontSize*FONTSIZELINEWIDTH)
        imd.rectangle((0, 0, thickness, image.height), self.color)
        imd.rectangle((0, 0, image.width, thickness), self.color)
        imd.rectangle((0, image.height-thickness-1, image.width, image.height), self.color)

        self.left = LayoutImage(image)
        self.left.setCenter(y=0)
        self.left.setRight(self.inner.getLeft()-WHITESPACESIZE*self.fontSize)
        
        self.right = LayoutImage(image.transpose(Image.Transpose.FLIP_LEFT_RIGHT))
        self.right.setCenter(y=0)
        self.right.setLeft(self.inner.getRight()+WHITESPACESIZE*self.fontSize)

        x, y, x1, y1 = boundingBox(self.inner, self.left, self.right)

        self.offset = (x,y)
        self.width = x1 - x
        self.height = y1 - y

        self.image = Image.new(IMGMODE, (int(self.width), int(self.height)))
        
        self.left.paste(self.image, self.offset)
        self.right.paste(self.image, self.offset)
        self.inner.paste(self.image, self.offset)

        self.setBottomLineDiffrence(self.inner.bottomLineDiffrence)


MACROS["\\para"] = ParenthesisLayout
MACROS["\\squarepara"] = SquareParenthesisLayout
