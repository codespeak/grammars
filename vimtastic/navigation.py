from pynhost import api
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import extension, baseutils

class NavigationGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '(<hom_window> <hom_left> | when delhi)': '{escape}{ctrl+h}a',
            '<hom_window> <hom_right>': '{escape}{ctrl+l}a',
            '<hom_window> <hom_high>': '{escape}{ctrl+k}a',
            '<hom_window> <hom_low>': '{escape}{ctrl+j}a',
            '<hom_window>close': '{escape}:q!{enter}',
        }