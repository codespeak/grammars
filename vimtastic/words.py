from pynhost import api
from pynhost.grammars import baseutils, extension
from pynhost.grammars.vimtastic import vimextension

class WordsGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '{} <any> <1->'.format(baseutils.list_to_rule_string(baseutils.VARIABLE_TYPES)): self.word_sep,
        }
        self.settings['filtered words'] = []

    def word_sep(self, words):
        # hom_words = [baseutils.get_homophone(w) for w in words[1:]]
        word = baseutils.get_case(words[1:], words[0])
        api.send_string(word)
        vimextension.VimExtensionGrammar.definitions.append('{}_variable'.format(word))