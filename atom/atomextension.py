from pynhost.grammars import extension
from pynhost.grammars import baseutils as bu

class AtomExtensionGrammar(extension.ExtensionGrammar):

    activate = '{ctrl+alt+8}'
    search_chars = bu.merge_dicts(bu.OPERATORS, bu.ALPHABET, bu.CHAR_MAP)

    def __init__(self):
        super().__init__()
        self.app_context = 'Autumntastic'
        self.mappings = {
            'nonzero': '0',
        }
