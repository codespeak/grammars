from pynhost import api
from pynhost import constants, dynamic
from pynhost.grammars import baseutils, extension
from pynhost.grammars.atom import atomextension

class RustExtensionGrammar(atomextension.AtomExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['priority'] = 1
        # self.context_filters = {
        #     'language': 'rust',
        # }
