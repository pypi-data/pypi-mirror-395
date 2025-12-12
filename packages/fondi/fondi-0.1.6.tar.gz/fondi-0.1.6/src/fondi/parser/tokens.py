
import math

BIDIRECTIONALCMD = 'bicmd'
COMMAND = 'macro'
FULLCOMMAND = 'fmacro'
PLAINTEXT = 'char'
ARGUMENT = 'arg'
OPERATION = 'opera'

TOKENSCOLOR = {
    BIDIRECTIONALCMD:'\033[91m',
    COMMAND: '\033[92m',
    ARGUMENT: '\033[94m',
    OPERATION: '\033[93m',
    FULLCOMMAND: '\033[1m\033[92m',
    PLAINTEXT: "",
}

TOKENS = {
    "\\frac": (COMMAND, 2),
    "\\super": (COMMAND, 2),
    "\\sub": (COMMAND, 2),
    "\\supersub": (COMMAND, 3),
    "\\subsuper": (COMMAND, 3),
    "\\para": (COMMAND, 1),
    "\\squarepara": (COMMAND, 1),
    "\\cases": (COMMAND, math.inf),
    "\\int": (COMMAND, 2),
    "\\oint": (COMMAND, 2),
    "\\ln": (COMMAND, 1),
    "\\log": (COMMAND, 1),
    "\\sin": (COMMAND, 1),
    "\\cos": (COMMAND, 1),
    "\\tan": (COMMAND, 1),
    "\\cdot": (COMMAND, 0),
    "\\text": (COMMAND, 1),
    "\\sqrt": (COMMAND, 1),
    "\\quad": (COMMAND, 0),
    "\\,": (COMMAND, 0),
    "\\:": (COMMAND, 0),
    "\\;": (COMMAND, 0),
    "\\!": (COMMAND, 0),
    "\\smallSpace": (COMMAND, 0),
    "\\qquad": (COMMAND, 0),
    "\\dot": (COMMAND, 1),
    "\\ddot": (COMMAND, 1),
    "\\tilde": (COMMAND, 1),
    "\\bar": (COMMAND, 1),
    "^_": BIDIRECTIONALCMD,
    "_^": BIDIRECTIONALCMD,
    "^": BIDIRECTIONALCMD,
    "_": BIDIRECTIONALCMD,
    "+": OPERATION,
    "-": OPERATION,
    "*": OPERATION,
    "·": OPERATION,
    "=": OPERATION,
    ">": OPERATION,
    "<": OPERATION,
}

SHORTCUTTOKENS = {
    "^": "\\super",
    "_": "\\sub",
    "^_": "\\supersub",
    "_^": "\\subsuper",
}

DOUBLECOMMANDS = {
    ('^', '_'): "^_",
    ('_', '^'): "_^"
}

PARENTHESIS = [
    ("(",')', '\\para'),
    ('[', ']', '\\squarepara'),
]

### MORE TOKENS
TOKENS["\\alpha"] = (COMMAND, 0)
TOKENS["\\beta"] = (COMMAND, 0)
TOKENS["\\gamma"] = (COMMAND, 0)
TOKENS["\\Gamma"] = (COMMAND, 0)
TOKENS["\\delta"] = (COMMAND, 0)
TOKENS["\\Delta"] = (COMMAND, 0)
TOKENS["\\eta"] = (COMMAND, 0)
TOKENS["\\epsilon"] = (COMMAND, 0)
TOKENS["\\theta"] = (COMMAND, 0)
TOKENS["\\kappa"] = (COMMAND, 0)
TOKENS["\\mu"] = (COMMAND, 0)
TOKENS["\\lambda"] = (COMMAND, 0)
TOKENS["\\tau"] = (COMMAND, 0)
TOKENS["\\sigma"] = (COMMAND, 0)
TOKENS["\\Sigma"] = (COMMAND, 0)
TOKENS["\\phi"] = (COMMAND, 0)
TOKENS["\\chi"] = (COMMAND, 0)
TOKENS["\\psi"] = (COMMAND, 0)
TOKENS["\\omega"] = (COMMAND, 0)
TOKENS["\\Omega"] = (COMMAND, 0)
TOKENS["\\pi"] = (COMMAND, 0)
TOKENS["\\prime"] = (COMMAND, 0)
TOKENS["\\left"] = (COMMAND, 0)
TOKENS["\\right"] = (COMMAND, 0)
TOKENS["\\differentialD"] = (COMMAND, 0)

### ESCAPE TOKENS
TOKENS["\\{"] = (COMMAND, 0)
TOKENS["\\}"] = (COMMAND, 0)
TOKENS["\\("] = (COMMAND, 0)
TOKENS["\\)"] = (COMMAND, 0)
TOKENS["\\["] = (COMMAND, 0)
TOKENS["\\]"] = (COMMAND, 0)