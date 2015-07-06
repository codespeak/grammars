import time
from pynhost import api, dynamic
from pynhost.grammars import extension, baseutils
from pynhost.grammars.atom import atomextension, atomutils


class AtomShortcutGrammar(atomextension.AtomExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_nerd> <hom_focus>': '{ctrl+0}',
            '<hom_nerd> <hom_new>': 'a',
            '<hom_nerd> <hom_move>': 'm',
            '<hom_nerd> <hom_duplicate>': 'd',
            '<hom_nerd> <hom_delete>': '{del}',
        }

    def delete_line(self, words):
        num = int(words[-1]) if words[-1].isdigit() else 1
