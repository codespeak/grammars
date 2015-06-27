import time
from pynhost import api
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension


class VimManipGrammar2(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'bottom': '{F11}G$a',
            '<hom_top>': '{F11}ggi',
            '(<hom_grab> | <hom_copy> | <hom_kill> | <hom_select>) <hom_bottom>': self.bottom,
            '(<hom_grab> | <hom_copy> | <hom_kill> | <hom_select>) <hom_top>': self.top,
            # '(<hom_grab> | <hom_copy> | <hom_kill> | <hom_select>) {}'.format(
            #     baseutils.list_to_rule_string(list(vimutils.single_motions))): self.single_motion,
        }

    def bottom(self, words):
        text = (vimutils.FUNCTIONS['RightIfNotFirstCol'] +
                vimutils.FUNCTIONS['GoToVisualMode'] +
                '{F11}G$')
        if words[0] != 'select':
            text += vimutils.commands[words[0]]
            if words[0] == 'copy':
                text += 'i'
        api.send_string(text)

    def top(self, words):
        text = (vimutils.FUNCTIONS['UpIfFirstCol'] +
                vimutils.FUNCTIONS['TrimLineWhitespace'] +
                vimutils.FUNCTIONS['GoToVisualMode'] +
                'gg')
        if words[0] != 'select':
            text += vimutils.commands[words[0]]
            if words[0] == 'copy':
                text += 'i'
        api.send_string(text)

    def single_motion(self, words):
        text = '{F11}' # normal or visual mode
        api.send_string(vimutils.single_motions[words[1]].replace('<m>', vimutils.commands[words[0]]))
        api.send_string(text)