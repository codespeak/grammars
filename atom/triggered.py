from pynhost import api, dynamic, grammarbase
from pynhost.grammars.atom import atomextension
from pynhost.grammars.atom import atomutils as au
from pynhost.grammars import baseutils

class TriggeredGrammar(atomextension.AtomExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_trigger> <hom_string>': self.stringify,
        }

    def stringify(self, words):
        self._handler.triggered['command']['before'].append("'")
        self._handler.triggered['command']['after'].append("'")
