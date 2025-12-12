
from .layout import *
from ..mathtext import MathText
from ..plain.helper import replaceColorRandom
from .helper import boundingBox
from PIL import Image, ImageDraw
import math

# class FracLayout(Layout):

#     def __init__(self, parent, top, bottom):
#         super().__init__()

#         self.fontSize = parent.fontSize
#         self.color = parent.color

#         self.top = MathText(top, int(self.fontSize*FRACSHRINKCOEFF), self.color)
#         self.bottom = MathText(bottom, int(self.fontSize*FRACSHRINKCOEFF), self.color)

#         linewidth = int(FRACFONTWIDTHCOEFF * self.fontSize)
#         self.padding = FRACPADDINGCOEFF * self.fontSize + linewidth/2
#         self.width = max(self.bottom.width, self.top.width)
#         self.height = self.bottom.height + self.top.height + self.padding * 2


#         # draw
#         self.image = Image.new(IMGMODE, (int(self.width), int(self.height)))

#         self.top.setBottom(self.padding)
#         self.top.setCenter(x=self.width/2)
        
#         self.bottom.setTop(-self.padding)
#         self.bottom.setCenter(x=self.width/2)

#         x, y, x1, y1 = boundingBox(self.bottom, self.top)
#         self.setBottomLineDiffrence(y + self.fontSize/4)

#         # paste
#         self.top.paste(self.image, (x,y))
#         self.bottom.paste(self.image, (x,y))

#         # draw line
#         imd = ImageDraw.ImageDraw(self.image)
#         imd.line((0, self.height+y, self.width, self.height+y), self.color, width=linewidth)

#         self.image = replaceColorRandom(self.image)
#         #self.image.save('debug/test-frac.png')


#     def __repr__(self):
#         return '({})/({})'.format(self.top, self.bottom)


GAPPROCENT = 0.1

class TextDecorationLayout(Layout):

    def __init__(self, parent, content, decoration):
        super().__init__()

        self.fontSize = parent.fontSize
        self.color = parent.color

        self.content = MathText(content, self.fontSize, self.color)
        self.decoration = decoration

        self.image = self.content.image
        self.width = int(self.content.width)
        self.height = int(self.content.height)

    def __pasteAtCenter__(self, img:Image, newimg, y:int):
        x = (newimg.size[0] - img.size[0]) // 2
        newimg.paste(img, (x, y, img.size[0]+x, y + img.size[1]))

    def drawAtTopCenter(self, img:Image):
        
        # make the original image bigger
        newimg = Image.new(IMGMODE, (max(self.image.size[0], img.size[0]), self.image.size[1]+img.size[1] + int(self.fontSize * GAPPROCENT)), (0,0,0,0))

        y = img.size[1]
        x = (newimg.size[0] - self.image.size[0]) // 2
        
        self.__pasteAtCenter__(img, newimg, 0)
        self.__pasteAtCenter__(self.image, newimg, img.size[1] + int(self.fontSize * GAPPROCENT))
        
        
        self.height += img.size[1] + int(self.fontSize * GAPPROCENT)

        # self.setBottomLineDiffrence(-img.size[1])

        self.image = newimg
        self.width = newimg.size[0]
        self.height = newimg.size[1]



    # def __repr__(self):
    #     return '{}({})'.format(self.decoration, self.content)


class DotLayout(TextDecorationLayout):
    def __init__(self, parent, content):
        super().__init__(parent, content, 'dot')
        # draw dot
        
        dotsize = int(self.fontSize*0.2)

        img = ImageDraw.ImageDraw(Image.new(IMGMODE, (dotsize + 1, dotsize + 1)))
        img.ellipse((0, 0, dotsize, dotsize), fill=self.color)
        self.drawAtTopCenter(img.im)

class DDotLayout(TextDecorationLayout):
    def __init__(self, parent, content):
        super().__init__(parent, content, 'ddot')
        # draw dot
        
        dotsize = int(self.fontSize*0.2)
        gap = int(dotsize * 0.6)

        img = ImageDraw.ImageDraw(Image.new(IMGMODE, (dotsize*2 + gap + 1, dotsize + 1)))
        img.ellipse((0, 0, dotsize, dotsize), fill=self.color)
        img.ellipse((dotsize + gap, 0, dotsize*2 + gap, dotsize), fill=self.color)
        
        self.drawAtTopCenter(img.im)

class BarLayout(TextDecorationLayout):
    def __init__(self, parent, content):
        super().__init__(parent, content, 'bar')
        # draw line
        
        linewidth = max(1, int(self.fontSize*0.1))

        img = ImageDraw.ImageDraw(Image.new(IMGMODE, (int(self.content.width), linewidth)))
        img.line((0, 0, int(self.content.width), 0), fill=self.color, width=linewidth)
        
        self.drawAtTopCenter(img.im)


class TildeLayout(TextDecorationLayout):
    def __init__(self, parent, content):
        super().__init__(parent, content, 'tilde')
        # draw line
        
        linewidth = max(1, int(self.fontSize*0.1))
        amplitude = int(self.fontSize*0.1)
        wavelength = int(self.fontSize*0.4)

        img = ImageDraw.ImageDraw(Image.new(IMGMODE, (int(self.content.width), amplitude*2)))
        points = []
        for x in range(0, int(self.content.width)):
            y = amplitude + int(amplitude * 0.9 *  -1 *  math.sin(2 * math.pi * x / wavelength))
            points.append((x, y))
        img.line(points, fill=self.color, width=linewidth)
        
        self.drawAtTopCenter(img.im)

MACROS["\\dot"] = DotLayout
MACROS["\\ddot"] = DDotLayout
MACROS["\\tilde"] = TildeLayout
MACROS["\\bar"] = BarLayout

#     "\\frac": FracLayout,
#     "\\super": SuperLayout,
#     "\\sub": SubLayout,
#     "\\supersub": SuperSubLayout,
#     "\\subsuper": SubSuperLayout,
#     "\\para": ParenthesisLayout
