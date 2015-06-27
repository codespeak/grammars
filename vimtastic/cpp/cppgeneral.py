from pynhost import api, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils


class CPPGeneralGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_nerd> <hom_line> <num>': [dynamic.Num(integer=False), 'gg'],
            '<hom_nerd> new [<num>]': self.new_child,
        }

    def new_child(self, words):
        if words[-1].isdigit():
            api.send_string('{} gg'.format(words[-1]))
        api.send_string('ma')