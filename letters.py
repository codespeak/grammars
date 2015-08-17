from pynhost import grammarbase
from pynhost import api
from pynhost.grammars import baseutils, extension


class LettersGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.dictionary = baseutils.ALPHABET
        self.mapping = {
            '[<hom_grow>] {} [<num>]'.format(baseutils.list_to_rule_string(baseutils.ALPHABET, True)): self.letters,
            'capital [{} [<num>]] '.format(baseutils.list_to_rule_string(baseutils.ALPHABET, True)): self.capital_on,
            'labor [{} [<num>]]'.format(baseutils.list_to_rule_string(baseutils.ALPHABET, True)): self.capital_off,
        }
        self.capital = False

    def letters(self, words):
        num = int(words.pop()) if words[-1].isdigit() else 1
        letter = baseutils.ALPHABET[words[-1]]
        if len(words) > 1 or self.capital:
            api.send_string(letter.upper())
            return
        for i in range(num):
            api.send_string(letter)

    def capital_on(self, words):
        self.capital = True
        if len(words) > 1:
            self.letters(words[1:])

    def capital_off(self, words):
        self.capital = False
        if len(words) > 1:
            self.letters(words[1:])
