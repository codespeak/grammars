from pynhost import api, dynamic
from pynhost.grammars.atom import atomextension
from pynhost.grammars.atom import atomutils as au
from pynhost.grammars import baseutils

class OperatorGrammar(atomextension.AtomExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '[<hom_short>] {} [<num>]'.format(
                baseutils.list_to_rule_string(baseutils.OPERATORS)): self.operator,
        }

    def operator(self, words):
        text = ''
        if words[0] == 'short':
            text += baseutils.OPERATORS[words[1]]
        else:
            text += '{}{}{}'.format(au.OTHER['beginningConditionalSpace'],
                                    baseutils.OPERATORS[words[0]],
                                    au.OTHER['endConditionalSpace'])
        if words[-1].isdigit():
            text += words[-1]
        api.send_string(text)
