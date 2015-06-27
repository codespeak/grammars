from pynhost import api, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils


class IncludeGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'include i/o stream': '#include <iostream>',
        }

    def new_child(self, words):
        if words[-1].isdigit():
            api.send_string('{} gg'.format(words[-1]))
        api.send_string('ma')