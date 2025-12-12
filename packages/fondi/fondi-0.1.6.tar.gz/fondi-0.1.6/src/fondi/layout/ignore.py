from .text import PlainText
class Ignore(PlainText):
    def __init__(self, parent):
        super().__init__('', parent.fontSize, parent.color)
