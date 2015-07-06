from pynhost import grammarbase
from pynhost import api
from pynhost import dynamic
import subprocess
import tempfile
import os
import difflib
import time
from pynhost.grammars import baseutils, extension
from pynhost.grammars.terminal import termextension

class TerminalGeneralGrammar(termextension.TerminalExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        '<hom_list>': 'ls | cat -n{enter}',
        '<hom_drop> [<num>]': self.drop,
        '<hom_climb> [<num>]': self.climb,
        '(<hom_left> | <hom_right>) [<num>]': self.left_right,
        'new tab': '{ctrl+shift+t}',
        'explore': 'caja .{enter}',
        'refresh': self.refresh,
        '(<hom_high> | <hom_low>) [<num>]': self.up_down,
        '<hom_terminate>': '{ctrl+z}',
        '<hom_git> <hom_initialize>': 'git init{enter}',
        '<hom_paste>': '{ctrl+shift+v}',
        '<hom_jump> {}'.format(baseutils.list_to_rule_string(baseutils.PATHS)): self.goto_path,
        '<hom_atom>': 'atom ',
        }

    def goto_path(self, words):
        api.send_string('cd ' + baseutils.PATHS[words[1]] + '{enter}')

    def drop(self, words):
        if len(words) == 1:
            api.send_string('cd ')
            return
        _, temp_name = tempfile.mkstemp()
        results = api.send_string('ls > {}'.format(temp_name) + '{enter}')
        time.sleep(.5)
        try:
            with open(temp_name) as f:
                for i, line in enumerate(f, start=1):
                    if i == int(words[1]):
                        api.send_string('cd {}'.format(line.rstrip('\n')) + '{enter}')
                        break
        finally:
            if os.path.isfile(temp_name):
                os.remove(temp_name)

    def climb(self, words):
        num = 1
        if words[-1].isdigit():
            num = int(words[-1])
        api.send_string('cd ..{}'.format('/..' * (num - 1)) + '{enter}')

    def left_right(self, words):
        num = 1
        if words[-1].isdigit():
            num = int(words[-1])
        for i in range(num):
            if words[0] == 'left':
                api.send_string('{ctrl+pageup}')
            else:
                api.send_string('{ctrl+pagedown}')
            if i != num:
                time.sleep(.1)

    def up_down(self, words):
        direction = '{up}'
        if words[0] == 'low':
            direction = '{down}'
        num = 1
        if len(words) > 1:
            num = int(words[-1])
        for i in range(num):
            api.send_string(direction)
            if i + 1 != num:
                time.sleep(.1)

    def refresh(self, words):
        api.send_string('{ctrl+z}')
        time.sleep(.5)
        api.send_string('{up}{enter}')
