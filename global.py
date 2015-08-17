import subprocess
import os
import difflib
import threading
from pynhost import grammarbase
from pynhost import api
from pynhost import dynamic
from pynhost import grammarbase
from pynhost.grammars import baseutils, extension

class GlobalGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        '(<hom_enter> | <hom_slap>) [<num>]': ['{enter}', dynamic.Num().add(-1)],
        '<hom_leap>': '{tab}',
        'space': ' ',
        '(escape | out)': '{escape}',
        '<hom_job> [<num>]': ['{backspace}', dynamic.Num().add(-1)],
        '<hom_tell> [<num>]': ['{delete}', dynamic.Num().add(-1)],
        '<hom_open> <any> <1->': self.open_window,
        '(<hom_num> | number) <num>': self.number,
        '<hom_start> <any> <1->': self.launch_program,
        '<hom_kill> program': '{alt+F4}',
        'maximize': '{alt+F10}',
        'minimize': '{alt+F9}',
        '<hom_repeat> [<num>]': [dynamic.RepeatCommand(count=dynamic.Num(default=1))],
        '<hom_again> [<num>]': dynamic.Num(default=1),
        '<hom_negative> <num>': self.negative_num,
        }
        self.settings['priority'] = 4

    def again(self, words):
        self.command_history[-1].run()

    def literal(self, words):
        api.send_string(' '.join(words[1:]))

    def begin_macro(self, words):
        self._begin_recording_macro(words[-1])

    def finish_macro(self, words):
        self._finish_recording_macro(words[-1])

    def repeat(self, words):
        for command in self.command_history[-int(words[-1]):]:
            command.run()

    def press_keys(self, words):
        api.send_string('{' + '+'.join(words[1:]) + '}')

    def backspace(self, words):
        for i in range(int(baseutils.set_number(words))):
            api.send_string('{backspace}')

    def number(self, words):
        if len(words) == 1:
            api.send_string('num')
            return
        api.send_string(words[-1])

    def open_window(self, words):
        if words[1] in ['vim', 'them', 'pen', 'then', 'than', 'vent'] or words[0] == '(':
            words[1] = 'vimtastic'
        hotkeys = {
            'adam': 'Autumntastic',
            'Adam': 'Autumntastic',
            'autumn': 'Autumntastic',
            'atom': 'Autumntastic',
            'sublime': 'Sublime Text (UNREGISTERED)',
            'some wine': 'Sublime Text (UNREGISTERED)',
            'someone': 'Sublime Text (UNREGISTERED)',
            'upon': 'Sublime Text (UNREGISTERED)',
            'from': '- Google Chrome',
            'home': '- Google Chrome',
            'control': '- Google Chrome',
            'close': '- Google Chrome',
            'thrown': '- Google Chrome',
            'chrome': '- Google Chrome',
            'google chrome': '- Google Chrome',
            'coral': '- Google Chrome',
            'firefox': 'Vimperator',
        }
        api.activate_window(' '.join(words[1:]))

    def mouse_click(self, words):
        api.mouse_click()

    def launch_program(self, words):
        program = ' '.join(words[1:])
        program_names = {
            'firefox': ['firefox'],
            'google-chrome': ['browser', 'chrome', 'google chrome', 'web browser', 'rome', 'role'],
            'gvim': ['vim', 'them', 'with them', 'text editor', 'with him', 'to them'],
            'spotify': ['spotify', 'modified'],
            'caja': ['explorer', 'explore'],
            'atom': ['atom', 'adam'],
        }
        for k, v in program_names.items():
            for name in v:
                if program == name:
                    FNULL = open(os.devnull, 'w')
                    subprocess.call([k], stdout=FNULL, stderr=subprocess.STDOUT)
                    return

    def negative_num(self, words):
        api.send_string(str(-int(words[-1])))

class SpecificOpenGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        '<hom_open> <hom_atom> [<any> <1->]': self.open_atom,
        '<hom_open> <hom_firefox> [<any> <1->]': self.open_firefox,
        }
        self.settings['priority'] = 5

    def open_atom(self, words):
        api.activate_window(['autumntastic'] + words[2:])

    def open_firefox(self, words):
        api.activate_window(['vimperator'] + words[2:])
