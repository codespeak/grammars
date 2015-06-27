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
        self.settings['regex mode'] = True
        self.mapping = {
            r'\(': self.open_window,
            r'\d+/': '{enter}',
        }

    def open_window(self, words):
        window_names = baseutils.get_open_window_names()
        matches = difflib.get_close_matches('vimtastic', window_names.keys(), cutoff=.2)
        if matches:
            print(matches)
            pid = str(int(window_names[matches[0]], 16))
            subprocess.call(['xdotool', 'windowfocus', pid])
            subprocess.call(['xdotool', 'windowactivate', pid])