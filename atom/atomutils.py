import time
from pynhost import api, dynamic

ACTIONS = {
    'select': 's',
    'copy': 'y',
    'paste': 'p',
    'kill': 'd',
    'grab': 'c',
}

MOTIONS = {
    'next': '!',
    'back': '$',
    'neat': '#',
    'band': '@',
    'final': '%',
    'first': '^',
    'absolute': '&',
    'left': 'h',
    'low': 'j',
    'high': 'k',
    'right': 'l',
}

SIMPLE = {
    'line': '*',
}

OTHER = {
    'beginningConditionalSpace': '{ctrl+alt+shift+1}',
    'endConditionalSpace': '{ctrl+alt+shift+2}',
    'filePathToClipboard': '{ctrl+alt+shift+3}',
    'clearSelect': '{ctrl+alt+shift+8}',
    'selectFunction': '{ctrl+alt+shift+9}',
    'selectClass': '{ctrl+alt+shift+0}',
}

OPERATORS = {
    'plus': '+',
    'times': '*',
    'minus': '-',
    'over': '/',
    'divided by': '/',
    'mod': '%',
    'modulo': '%',
    'remainder': '%',
    'small': '<',
    'smaller': '<',
    'small equal': '<=',
    'smaller equal': '<=',
    'big': '>',
    'bigger': '>',
    'big equal': '>=',
    'bigger equal': '>=',
    'equals': '=',
    'compare': '==',
    'compared': '==',
}

SURROUND_OBJECTS = {
    'pair': ('(', ')'),
    'braces': ('{{', '}}'),
    'block': ('[', ']'),
    'fence': ('<', '>'),
}

STRING_OBJECTS = {
    'single': "'",
    'double': '"',
    'triple': "'''",
}

INCREMENTAL_LIMITS = {
    'fish': "f",
    'through': "f",
    'until': 't',
    'till': 't',
    'bill': 'T',
    'blue': 'F',
}

def do_action(action):
    if action == 'copy':
        api.send_string('{ctrl+c}')
    elif action in ('grab', 'cut'):
        api.send_string('{ctrl+x}')
    elif action == 'paste':
        api.send_string('{ctrl+v}')
    elif action == 'kill':
        api.send_string('{back}')
