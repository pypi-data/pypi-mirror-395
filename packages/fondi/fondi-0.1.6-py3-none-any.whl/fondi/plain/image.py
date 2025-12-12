
from PIL import Image
from ..layout import Layout
import os

class Image(Layout):

    def __init__(self, image:Image):
        super().__init__()
        self.image = image
        self.width = self.image.width
        self.height = self.image.height