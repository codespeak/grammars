from pynhost import grammarbase
from pynhost import api
from pynhost.grammars import baseutils, extension


class LettersGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.dictionary = baseutils.ALPHABET
        self.mapping = {
            '[<hom_grow>] {}'.format(baseutils.list_to_rule_string(baseutils.ALPHABET, True)): self.letters,
            'capital [{}]'.format(baseutils.list_to_rule_string(baseutils.ALPHABET, True)): self.letters,
            'labor [{}]'.format(baseutils.list_to_rule_string(baseutils.ALPHABET, True)): self.letters,
        }
        self.capital = False
        
    def letters(self, words):
        letter = baseutils.ALPHABET[words[-1]]
        if len(words) > 1 or self.capital:
            api.send_string(letter.upper())
            return
        api.send_string(letter)

    def capital_on(self, words):
        self.capital = True
        if len(words) > 1:
            self.letters(words[1:])

    def capital_off(self, words):
        self.capital = False
        if len(words) > 1:
            self.letters(words[1:])
