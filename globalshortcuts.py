import subprocess
import os
import difflib
import threading
from pynhost import grammarbase
from pynhost import api
from pynhost import dynamic
from pynhost import grammarbase
from pynhost.grammars import baseutils, extension

class GlobalShortcutsGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        '<hom_django> <end>': 'django',
        '<hom_click>': self.click,
        '<hom_mouse> (<hom_high> | <hom_right> | <hom_down> | <hom_left>) <num>': self.mouse_move,
        }

    def click(self, words):
        num = '1'
        if words[-1].isdigit():
            num = words[-1]
        api.mouse_click('left', 'both', num)

    def mouse_move(self, words):
        x = 0
        y = 0
        if words[1] == 'high': y -= int(words[-1])
        elif words[1] == 'right': x += int(words[-1])
        elif words[1] == 'low': y += int(words[-1])
        elif words[1] == 'left': x -= int(words[-1])
        api.mouse_move(x, y)