

import ply.lex as lex

tokens = (
    'INCLUDE',
    'STRING',
    'ID',
    'OP',
    'DIRECTIVE',
    'COMMENTSL'
)

#    r'//.*$'

#t_STRING = r"'([^\\']+|\\'|\\\\)*'"
# r'"([^"\n]|(\\"))*"$'
def t_STRING(t):
#    r"'([^\\']+|\\'|\\\\)*'"
    r'".*"|""'
    t.value = t.value[1:-1]
    return t
def t_DIRECTIVE(t):
    r'`[a-zA-Z0-9][a-zA-Z0-9_]*|`'
    t.value = t.value[1:]
    return t
#t_INCLUDE = r'`include'
t_ID = r'[$_a-zA-Z0-9][_a-zA-Z0-9]*'
#t_ID = 'a'

def t_COMMENTSL(t):
#    r'(/\\(.|\n)*?\\/)|(//.*)'
    r'//.*\n'
    pass

def t_COMMENT(t):
    r'/\*.*?\*/'
    pass

def t_BACKSLASH(t):
    r'\\'
    pass

literals = [';', ':', "'", ',', '+', '-', '*', '/', '%', '^', '=', '&', '|', '#', '@', '!', '?', '~', '.']
#t_OP = r'([;:\',+-*/])'
#t_OP = r';:\',+-*/'

#t_ignore = ' \t\n;:\',+-*\\/%^=&|#@!?~.()[]{}<>\0169\0174' + chr(65533)
#t_ignore = ' \t\n;:\',+-*\\/%^=&|#@!?~.()[]{}<>'+chr(65533)
t_ignore = ' \t\n()[]{}<>'+chr(65533)

def t_error(t):
    print("Error: %s" % str(t))

def mk_lexer(**kwargs):
    return lex.lex(**kwargs)


