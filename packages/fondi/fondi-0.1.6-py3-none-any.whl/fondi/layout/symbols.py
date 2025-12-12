
from .layout import *
from ..mathtext import MathText
from ..plain.helper import replaceColorRandom
from ..plain import Symbol, PlainText
from .helper import boundingBox
from .ignore import Ignore
from PIL import Image, ImageDraw
#https://www.ascii-code.com/characters/greek

# class Delta(Symbol):
#     def __init__(self, parent):
#         super().__init__('/path/to/file')

class Alpha(PlainText):
    def __init__(self, parent):
        super().__init__('α', parent.fontSize, parent.color)

class Beta(PlainText):
    def __init__(self, parent):
        super().__init__('β', parent.fontSize, parent.color)

class Gamma(PlainText):
    def __init__(self, parent):
        super().__init__('γ', parent.fontSize, parent.color)

class UGamma(PlainText):
    def __init__(self, parent):
        super().__init__('Γ', parent.fontSize, parent.color)

class UDelta(PlainText):
    def __init__(self, parent):
        super().__init__('Δ', parent.fontSize, parent.color)

class Delta(PlainText):
    def __init__(self, parent):
        super().__init__('δ', parent.fontSize, parent.color)

class Eta(PlainText):
    def __init__(self, parent):
        super().__init__('η', parent.fontSize, parent.color)

class Epsilon(PlainText):
    def __init__(self, parent):
        super().__init__('ε', parent.fontSize, parent.color)

class Theta(PlainText):
    def __init__(self, parent):
        super().__init__('θ', parent.fontSize, parent.color)

class Kappa(PlainText):
    def __init__(self, parent):
        super().__init__('κ', parent.fontSize, parent.color)

class Mu(PlainText):
    def __init__(self, parent):
        super().__init__('μ', parent.fontSize, parent.color)

class Lambda(PlainText):
    def __init__(self, parent):
        super().__init__('λ', parent.fontSize, parent.color)

class Tau(PlainText):
    def __init__(self, parent):
        super().__init__('τ', parent.fontSize, parent.color)

class Sigma(PlainText):
    def __init__(self, parent):
        super().__init__('σ', parent.fontSize, parent.color)

class USigma(PlainText):
    def __init__(self, parent):
        super().__init__('Σ', parent.fontSize, parent.color)

class Phi(PlainText):
    def __init__(self, parent):
        super().__init__('φ', parent.fontSize, parent.color)

class Chi(PlainText):
    def __init__(self, parent):
        super().__init__('χ', parent.fontSize, parent.color)

class Psi(PlainText):
    def __init__(self, parent):
        super().__init__('ψ', parent.fontSize, parent.color)

class Omega(PlainText):
    def __init__(self, parent):
        super().__init__('ω', parent.fontSize, parent.color)

class UOmega(PlainText):
    def __init__(self, parent):
        super().__init__('Ω', parent.fontSize, parent.color)

class Pi(PlainText):
    def __init__(self, parent):
        super().__init__('π', parent.fontSize, parent.color)

class Prime(PlainText):
    def __init__(self, parent):
        super().__init__("'", parent.fontSize, parent.color)



MACROS["\\alpha"] = Alpha
MACROS["\\beta"] = Beta
MACROS["\\gamma"] = Gamma
MACROS["\\Gamma"] = UGamma
MACROS["\\delta"] = Delta
MACROS["\\Delta"] = UDelta
MACROS["\\eta"] = Eta
MACROS["\\epsilon"] = Epsilon
MACROS["\\theta"] = Theta
MACROS["\\kappa"] = Kappa
MACROS["\\mu"] = Mu
MACROS["\\lambda"] = Lambda
MACROS["\\tau"] = Tau
MACROS["\\sigma"] = Sigma
MACROS["\\Sigma"] = USigma
MACROS["\\phi"] = Phi
MACROS["\\chi"] = Chi
MACROS["\\psi"] = Psi
MACROS["\\omega"] = Omega
MACROS["\\Omega"] = UOmega
MACROS["\\pi"] = Pi
MACROS["\\prime"] = Prime

### ESCAPES
class StartCurlyBracket(PlainText):
    def __init__(self, parent):
        super().__init__('{', parent.fontSize, parent.color)

class EndCurlyBracket(PlainText):
    def __init__(self, parent):
        super().__init__('}', parent.fontSize, parent.color)

class StartSquareBracket(PlainText):
    def __init__(self, parent):
        super().__init__('[', parent.fontSize, parent.color)

class EndSquareBracket(PlainText):
    def __init__(self, parent):
        super().__init__(']', parent.fontSize, parent.color)

class StartBracket(PlainText):
    def __init__(self, parent):
        super().__init__('(', parent.fontSize, parent.color)

class EndBracket(PlainText):
    def __init__(self, parent):
        super().__init__(')', parent.fontSize, parent.color)



MACROS["\\{"] = StartCurlyBracket
MACROS["\\}"] = EndCurlyBracket
MACROS["\\("] = StartBracket
MACROS["\\)"] = EndBracket
MACROS["\\["] = StartSquareBracket
MACROS["\\]"] = EndSquareBracket
MACROS["\\left"] = Ignore
MACROS["\\right"] = Ignore

class DifferentialD(PlainText):
    def __init__(self, parent):
        super().__init__("d", parent.fontSize, parent.color, italic=False)

MACROS["\\differentialD"] = DifferentialD