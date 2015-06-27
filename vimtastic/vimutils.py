import time
import os
import subprocess
from pynhost.grammars import baseutils, _locals
from pynhost import api

LEADER = '\\'

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

DIRECTION_MAP = {
    'high': 'k',
    'right': 'l',
    'low': 'j',
    'left': 'h',
}

FUNCTIONS = {
    'MarkInsertPos': '{alt+1}',
    'GoToInsertPos': '{alt+2}',
    'smart escape': '{F2}',
    'SmartEscape': '{F2}',
    'SmartSpace': '{F3}',
    'set mark': '{F6}',
    'return to mark': '{F7}',
    'TrimLineWhitespace': '{F8}',
    'align above': '{alt+7}',
    'AlignWithAbove': '{alt+7}',
    'FilenameToClipboard': '{}1'.format(LEADER),
    'number jump': '{}2'.format(LEADER),
    'RightIfNotFirstCol': '{}3'.format(LEADER),
    'UpIfFirstCol': '{}4'.format(LEADER),
    "GoToFunction": '{}5'.format(LEADER),
    "GoToClass": '{}6'.format(LEADER),
    "SelectIndent": '{}7'.format(LEADER),
    'GoToVisualMode': '{F12}',
    'GoToInsertMode': '{0}{0}{0}5'.format(LEADER),
    'DeleteLineIfEmpty': '{0}{0}{0}'.format(LEADER) + '{F5}',
    'left': format(LEADER) + '{F1}',
    'down': format(LEADER) + '{F2}',
    'up': format(LEADER) + '{F3}',
    'right': format(LEADER) + '{F4}',
    'EndSpace': format(LEADER) + '{F5}',
}

def get_single_character(char):
    if char in CHAR_MAP:
        char = CHAR_MAP[char]
    if len(char) == 1:
        return char

def search(char, forwards):
    if forwards:
        return ('/' + char + '{enter}')
    return ('?' + char + '{enter}')

def get_text_from_register(reg_name):
    assert len(reg_name) == 1 and reg_name != 'b'
    api.send_string("{escape}:let @b = @+{enter}")
    api.send_string(":let @+ = @{}{{enter}}".format(reg_name))
    text = pyperclip.paste()
    api.send_string(":let @+ = @b{enter}")
    return text

def get_current_window_path():
    api.send_string("{escape}:let @c = expand('%:p'){enter}")
    return get_text_from_register('c')

def handle_above_below_goto(words):
    api.send_string('{escape}')
    if len(words) == 2:
        api.send_string(words[1] + 'gg')
    if words[0] == 'climb':
        api.send_string('{shift+o}')
    else:
        api.send_string('o')

def handle_direction_goto(words, num):
    # if words[0] in basic_directions:
    #     api.send_string(basic_directions[words[0]])
    api.send_string('{F11}')
    if words[0] in right_motions:
        api.send_string('{right}')
    editing_command = num + motions[words[0]]
    api.send_string(editing_command)
    # api.send_string('mb`ax`b')
    if words[0] in ['final', 'right', 'ring', 'brink']:
        api.send_string('a')
    else:
        api.send_string('i')

def purge(word_list):
    new_list = []
    for word in word_list:
        if word not in ['and']:
            new_list.append(word)
    return new_list

def insert_mode(func):
    pass

def insert_mode(func):
    pass

def insert_mode(func):
    pass     

commands = {
    'grab': 'c',
    'copy': 'y',
    'kill': '"_c',
    'select': '{F12}',
    'surround': 'ys',
}

motions = {
    'high': '{up}',
    'right': '{right}',
    'low': '{down}',
    'left': '{left}',
    'next': 'w',
    'ring': 'e',
    'back': 'b',
    'brink': 'ge',
    'first': '{shift+6}',
    'final': '{shift+4}',
    'absolute': '0',
    'word': 'iw',
    'outer word': 'aw',
    'pair': 'i)',
    'outer pair': 'a)',
    'block': 'i]',
    'outer block': 'a]',
    'brace': 'i}}',
    'outer brace': 'a}}',
    'single': "i'",
    'outer single': "a'",
    'double': 'i"',
    'outer double': 'a"',
    'tag': 'i>',
    'outer tag': 'a>',
    }

single_motions = {
    'file': 'gg<m>G$a',
    'line': '<m><m>',
    'climb': '{up}<m><m>i',
    'drop': '{down}<m><m>i',
}

through = {
    'blue': 'Fi',
    'fish': 'fi',
    'bill': 'Ti',
    'till': 'ti',
    'until': 'ti',
}

text_objects = {
    'single': "'",
    'double': '"',
    'pair': ')',
    'brace': '}}',
    'block': ']',
    'tag': 't',
    'word': 'w',
}

left_motions = [
    'left',
]

right_motions = [
    'right',
    'next',
    'ring',
]

motion_homophones = {
    'left': ['last', 'lift'],
    'right': ['light', 'rights'],
    'up': ['hi', 'high', 'up', 'highs'],
    'down': ['low', 'down'],
}

def get_motion_homonym(word):
    for motion in motion_homophones:
        if word in motion_homophones[motion]:
            return motion
    return word

def create_variable_name(words):
    var_name = ''
    for word in purge(words):
        if word in baseutils.ALPHABET:
            var_name += baseutils.ALPHABET[word]
        elif word in baseutils.CHAR_MAP:
            var_name += baseutils.CHAR_MAP[word]
        elif word in OPERATORS:
            var_name += OPERATORS[word]
        else:
            var_name += word
    return var_name

def combine_words(words):
    new_words = [words[0], '', words[-1]]
    for i, word in enumerate(words[1:-1]):
        if i != 0:
            new_words[1] += ' '
        new_words[1] += word
    return new_words

def guess_at_text(words):
    words = [baseutils.get_homophone(word) for word in words]
    if words[0] in baseutils.VARIABLE_TYPES and len(words) > 1:
        return baseutils.get_case(words[1:], words[0])
    return create_variable_name(words)

def make_outer_list(alist):
    new_list = []
    for text_object in alist:
        new_list.extend([text_object, 'outer {}'.format(text_object)])
        if text_object in _locals.HOMOPHONES:
            for hom in _locals.HOMOPHONES[text_object]:
                new_list.extend([hom, 'outer {}'.format(hom)])
    return new_list

def get_clipboard_contents(keys):
    clipboard_contents = baseutils.get_clipboard_contents()
    api.send_string(keys)
    time.sleep(.1)
    new_contents = baseutils.get_clipboard_contents()
    baseutils.set_clipboard_contents(clipboard_contents)
    return new_contents

def get_django_project_root(fullpath):
    path_list = fullpath.split('/')
    while len(path_list) > 1:
        if path_list[-2] == 'django':
            return '/'.join(path_list)
        path_list = path_list[:-1]
