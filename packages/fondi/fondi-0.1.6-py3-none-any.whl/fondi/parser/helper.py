
from .tokens import *
import sys
DEBUGFLAG = '--debug' in sys.argv
NOPRINTFLAG = '--noprint' in sys.argv

# parser
# def getParameters(text, count=-1, openchar='{', closechar='}'):

#     args = []
#     pointer = 0
#     depth = 0
#     end = 0
#     for i, c in enumerate(text):
#         if count != -1 and (len(args) >= count):
#             break

#         if c == openchar:
#             depth += 1
            
#             if depth == 1:
#                 pointer = i+1
        
#         if c == closechar:
#             depth -= 1

#             if depth == 0:
#                 end = i
#                 args.append(text[pointer:i])

#     return args, end


def cprint(l):
    s = ''
    for clss, tok in l:

        if clss[0] == COMMAND:
            s += TOKENSCOLOR[clss[0]] + tok + '\033[0m'

        elif clss == FULLCOMMAND:
            s += TOKENSCOLOR[clss] + tok["name"] +''.join(['{'+i+'}' for i in tok["args"]]) + '\033[0m'

        elif clss == ARGUMENT:
            s += TOKENSCOLOR[clss] + '{'+tok+'}' + '\033[0m'

        elif type(tok) is str:
            s += TOKENSCOLOR[clss] + tok + '\033[0m'

    print(s)
