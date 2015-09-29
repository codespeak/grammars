import subprocess
import re
import os
import time
from pynhost import api
from pynhost.grammars import _locals

def get_open_window_names():
    raw_names = subprocess.check_output(['wmctrl', '-l']).decode('utf8').split('\n')
    split_names = [name.split() for name in raw_names if name]
    name_dict = {}
    for name in split_names:
        if not int(name[1]):
            name_dict[' '.join(name[3:])] = name[0]
    return name_dict

CHAR_MAP = {
    'rib': '.',
    'flat': '_',
    'rice': '(',
    'cake': ')',
    'sail': '{{',
    'boat': '}}',
    'wood': '[',
    'grain': ']',
    'comma': ',',
    "single": "'",
    'double': '"',
    'space': ' ',
    'dirt': ';',
    'trip': ',',
    'pound': '#',
    'star': '*',
    'spine': ':',
    'tight': '-',
    'gun': '/',
    'rose': '\\',
    'coin': '$',
    'chase': '?',
    'bell': '@',
    'exclaim': '!',
}


ALPHABET = {
    'ask': 'a',
    'asked': 'a',
    'bike': 'b',
    'coup': 'c',
    'dam': 'd',
    'eve': 'e',
    'frog': 'f',
    'good': 'g',
    'him': 'h',
    'ice': 'i',
    'jim': 'j',
    'gym': 'j',
    'kite': 'k',
    'kites': 'k',
    'kyte': 'k',
    "kyte's": 'k',
    'live': 'l',
    'mile': 'm',
    'need': 'n',
    'ostrich': 'o',
    'paint': 'p',
    'aint': 'p',
    "ain't": 'p',
    'quite': 'q',
    'risk': 'r',
    'slip': 's',
    'trunk': 't',
    'uniform': 'u',
    'vote': 'v',
    'wig': 'w',
    'x-ray': 'x',
    'young': 'y',
    'zone': 'z',
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
    'stick': '==',
}

VARIABLE_TYPES = [
    'camel',
    'score',
    'title',
    'upper',
    'word',
    'jazz',
    'drive',
    'prop',
    'stretch',
    'say',
]

PATHS = {
    'django': '/home/evan/modules/python/python3/django',
    'virtual': '/home/evan/Modules/Python/Python3/virtualenv',
    'home': '/home',
    'grammars': '/usr/local/lib/python3.4/dist-packages/pynhost/grammars',
    'python': '/home/evan/modules/python/python3',
}

def get_single_character(char, uppercase):
    if char in CHAR_MAP:
        return CHAR_MAP[char]
    if char in ALPHABET:
        if uppercase:
            return ALPHABET[char].upper()
        return ALPHABET[char]
    if len(char) == 1:
        return char

def get_case(words, case):
    if case in ['underscore', 'score']:
        return '_'.join(words)
    if case == 'title':
        return ''.join([word.title() for word in words])
    if case == 'upper':
        return '_'.join([word.upper() for word in words])
    if case == 'camel':
        return words[0].lower() + ''.join([word.title() for word in words[1:]])
    if case == 'word':
        return ''.join(words)
    if case == 'jazz':
        return '.'.join(words)
    if case == 'drive':
        return '-'.join(words)
    if case == 'prop':
        return ' '.join([word.title() for word in words])
    if case == 'stretch':
        return ', '.join(["'{}'".format(word) for word in words])
    if case == 'say':
        return ' '.join(words)

def set_number(words):
    if len(words) > 1:
        return words[-1]
    return '1'

def last_number(words, as_int=True):
    if words[-1].isdigit():
        return int(words[-1]) if as_int else words[-1]
    return 1 if as_int else '1'

def get_clipboard_contents():
    try:
        return subprocess.check_output(['xclip', '-selection', 'c', '-o']).decode('utf8')
    except subprocess.CalledProcessError:
        return ''

def set_clipboard_contents(text):
    p = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE)
    try:
        # works on Python 3 (bytes() requires an encoding)
        p.communicate(input=bytes(text, 'utf-8'))
    except TypeError:
        # works on Python 2 (bytes() only takes one argument)
        p.communicate(input=bytes(text))

def open_shell():
    subprocess.call(['x-terminal-emulator'])

def focus_or_launch_program(title, program_launch_name):
    open_windows = get_open_window_names()
    for name, decimal_id in open_windows.items():
        if re.search(title, name):
            focus_window(decimal_id)
            return 'focus'
    FNULL = open(os.devnull, 'w')
    subprocess.call([program_launch_name], stdout=FNULL, stderr=subprocess.STDOUT)
    return 'launch'

def focus_window(decimal_id):
    pid = str(int(decimal_id, 16))
    subprocess.call(['xdotool', 'windowfocus', pid])
    subprocess.call(['xdotool', 'windowactivate', pid])

def homify_text(word_text):
    return ' '.join(['<hom_{}>'.format(word) for word in word_text.split()])

def list_to_rule_string(alist, homify=True):
    rule_list = []
    for word in alist:
        if homify:
            word = homify_text(word)
        rule_list.append(word)
    return '({})'.format(' | '.join(rule_list))

def open_firefox_url(url):
    result = focus_or_launch_program('Vimperator', 'firefox')
    time.sleep(.5)
    if result == 'focus':
        api.send_string('{escape}{ctrl+t}')
    time.sleep(1)
    api.send_string('{ctrl+l}')
    time.sleep(2.5)
    api.send_string(url + '{enter}')

def get_homophone(word):
    '''
    Replicate <hom> functionality in functions
    '''
    for hom in _locals.HOMOPHONES:
        if word in _locals.HOMOPHONES[hom]:
            return hom
    return word

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
