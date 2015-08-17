from pynhost import api
from pynhost.grammars import baseutils
from pynhost.grammars.atom import atomextension, atomutils
from pynhost.grammars import extension

class WordsGrammar(extension.ExtensionGrammar):

    def __init__(self):
        super().__init__()
        self.mapping = {
            '{} <any> <1->'.format(baseutils.list_to_rule_string(baseutils.VARIABLE_TYPES)): self.word_sep,
        }
        self.settings['filtered words'] = []

    def word_sep(self, words):
        word = baseutils.get_case(words[1:], words[0])
        api.send_string(word)
