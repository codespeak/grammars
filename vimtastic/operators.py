from pynhost import api, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils

class OperatorGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '[<hom_short>] {} [<num>]'.format(baseutils.list_to_rule_string(vimutils.OPERATORS)): self.operator,
        }

    def operator(self, words):
        text = ''
        if words[0] == 'short':
            text += vimutils.OPERATORS[words[1]]
        else:
            text += '{}{}{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.OPERATORS[words[0]], vimutils.FUNCTIONS['EndSpace'])
        if words[-1].isdigit():
            text += words[-1]
        api.send_string(text)
