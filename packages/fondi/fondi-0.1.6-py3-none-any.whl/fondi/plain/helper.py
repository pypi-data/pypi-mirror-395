
from random import randint
import numpy as np


def randomColor():
    return (randint(0,255), randint(0,255), randint(0,255), 255)

def replaceColorRandom(image,ogcolor=(0,0,0,0)):
    return image
    replacement_color = randomColor()
    data = np.array(image)
    data[(data == ogcolor).all(axis = -1)] = replacement_color
    return Image.fromarray(data)
