from pynhost import api, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension

class ShortcutsWithFunctionsGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_index> [[(minus | negative)] <num>]': self.index,
            '<hom_comment> [<num> [<hom_fish> <num>]]': self.comment,
            '<hom_change> {0} {0}'.format(baseutils.list_to_rule_string(baseutils.ALPHABET)): self.change,
            '(<hom_increase> | <hom_decrease>) [<num>]': self.increment,
        }

        self.dictionary = baseutils.ALPHABET

    def index(self, words):
        api.send_string('[]{left}')
        if len(words) > 1:
            num = words[-1]  
            if words[-2] in ['minus', 'negative']:
                num = str(-int(num))
            api.send_string(num + '{right}')


    def comment(self, words):
        if len(words) == 1:
            api.send_string('{esc}gccwi')
            return

    def change(self, words):
        text = '{esc}f' + baseutils.ALPHABET[words[1]] + 'r' + baseutils.ALPHABET[words[2]] + 'a'
        api.send_string(text)

    def increment(self, words):
        keys = '{ctrl+a}'
        if words[0] == 'decrease':
            keys = '{ctrl+x}'
        num = ''
        if words[-1].isdigit():
            num = words[-1]
        api.send_string('{esc}' + '{}{}{}a'.format(vimutils.FUNCTIONS['number jump'], num, keys))
