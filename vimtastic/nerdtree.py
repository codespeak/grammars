from pynhost import api, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils


class NerdTreeGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_nerd> <hom_line> <num>': [dynamic.Num(integer=False), 'gg'],
            '<hom_nerd> new [<num>]': self.new_child,
            '<hom_nerd> [to] <hom_bookmarks>': 'B',
            '<hom_nerd> [to] <hom_create>': '{enter}{enter}i',
            '<hom_nerd> [to] delete': 'mdy',
            '<hom_nerd> [to] vertical': 'v',
            '<hom_nerd> [to] horizontal': 'i',
            '<hom_nerd> [to] refresh': 'R',
            '<hom_nerd> [to] (parent | parents)': 'p',
            '<hom_nerd> [to] <hom_root>': 'P',
            '<hom_nerd> [to] close': 'x',
            '<hom_nerd> [to] <hom_climb>': 'u',
            '<hom_nerd> [to] <num> enter': [dynamic.Num(integer=False), 'gg{enter}'],
            '<hom_poke> [to] <num>': [dynamic.Num(integer=False), 'gg{enter}'],
            'focalin': '11gg{enter}',
            '<hom_nerd> (<hom_django> | <hom_modules> | <hom_root> | <hom_home> | <hom_python>)': self.go_to_dir,
            '<hom_nerd> [to] <hom_copy>': 'mc',
            '<hom_nerd> [to] <hom_toggle>': '{esc}:NERDTreeToggle{enter}',
        }

    def new_child(self, words):
        if words[-1].isdigit():
            api.send_string('{} gg'.format(words[-1]))
        api.send_string('ma')

    def go_to_dir(self, words):
        target_dir = vimextension.VimExtensionGrammar.dirs[words[-1]]
        api.send_string(':cd {}'.format(target_dir) + '{enter}' + 'CD')
