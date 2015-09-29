from pynhost import api
from pynhost import constants, dynamic
from pynhost.grammars import baseutils, extension
from pynhost.grammars.atom.rust import rustextension

class RustTerminalGrammar(rustextension.RustExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['priority'] = 1
        self.app_context = '(terminal|cmd)'
        self.mapping = {
            '<hom_cargo> <hom_binary>': 'cargo new  --bin' + '{left}' * 6,
            '<hom_cargo> <hom_library>': 'cargo new ',
        }
