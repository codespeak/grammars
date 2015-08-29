import time
from pynhost import api, dynamic
from pynhost.grammars import extension, baseutils
from pynhost.grammars.atom import atomextension
from pynhost.grammars.atom import atomutils as au

class AtomShortcutGrammar(atomextension.AtomExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_atom> <hom_refresh>': '{ctrl+alt+r}',
            '<hom_scratch> [<num>]': ['{ctrl+z}', dynamic.Num().add(-1)],
            '<hom_redo> [<num>]': ['{ctrl+y}', dynamic.Num().add(-1)],
            '<hom_save>': '{ctrl+s}',
            '<hom_debug> <hom_panel>': '{ctrl+shift+i}',
            '<hom_clear> (<hom_select>|<hom_selection>)': au.OTHER['clearSelect'],
            '<hom_wave>': au.OTHER['clearSelect'] + '{end}:{enter}',
            '<hom_stop>': au.OTHER['clearSelect'] + '{end}{enter}{back}',
            '<hom_braces>': '{{}}',
            '<hom_scope>': '{{{enter}{enter}}}{up}{tab}',
            '<hom_pair>': '()',
            '<hom_call>': '(){left}',
            '<hom_block>': '[]',
            '<hom_index>': '[]{left}',
            '<hom_dict>': 'dict',
            '<hom_show>': 'print(){left}',
            '<hom_carb>': '{escape}f(a',
            '<hom_join> <hom_line>': 'J',
            '<hom_string>': "''{left}",
            '<hom_link>': ': ',
            '<hom_tab>': '{tab}',
            '<hom_straight>': '',
            '<hom_bow> [<num>]': ['{ctrl+shift+alt+5}', dynamic.Num().add(-1)],
            '<hom_shield> [<num>]': ['{ctrl+shift+alt+4}', dynamic.Num().add(-1)],
            '<hom_dell> [<num>]': ['{del}', dynamic.Num().add(-1)],
            '<hom_punch>': au.OTHER['clearSelect'] + '{ctrl+d}{back}',
            '<hom_brain>': au.OTHER['clearSelect'] + '{ctrl+d}{ctrl+c}' + au.OTHER['clearSelect'],
            '<hom_green> [<num>]': self.delete_line,
            '<hom_fuzzy>': '{ctrl+t}',
            '<hom_plant> [to] <hom_new>': '{ctrl+n}',
            '<hom_plant> [to] <hom_close>': '{ctrl+w}',
            '<hom_plant> [to] (<hom_left> | <hom_right>) [<num>]': self.tab_direction,
            '<hom_sort> <end>': 'sort',
            '<hom_care>': 'char',
            '<hom_climb>': '{ctrl+shift+enter}',
            '<hom_drop>': '{end}{enter}',
            '(<hom_duplicate> | <hom_dupe>) [<hom_below>]': '{ctrl+D}',
            '(<hom_duplicate> | <hom_dupe>) <hom_above>': '{up}{ctrl+D}',
            '<hom_high> [<num>]': ['{up}', dynamic.Num().add(-1)],
            '<hom_right> [<num>]': ['{right}', dynamic.Num().add(-1)],
            '<hom_low> [<num>]': ['{down}', dynamic.Num().add(-1)],
            '<hom_left> [<num>]': ['{left}', dynamic.Num().add(-1)],
            '<hom_punch>': au.OTHER['clearSelect'] + '{ctrl+d}{back}',
            '<hom_comment>': '{ctrl+alt+Z}',
            '<hom_halt>': ', ',
            'selfhood': 'self.',
            '<hom_swap> <hom_high>': '{ctrl+up}',
            '<hom_swap> <hom_low>': '{ctrl+down}',
            '<hom_search>': '{ctrl+f}',
            '<hom_bounce>': '{F3}'
        }
        self.settings['priority'] = 3

    def delete_line(self, words):
        num = int(words[-1]) if words[-1].isdigit() else 1
        for i in range(num):
            api.send_string('{ctrl+l}')
        api.send_string('{back}{left}')

    def line_goto(self, words):
        api.send_string('{ctrl+g}')
        time.sleep(.3)
        api.send_string(words[-1] + '{enter}')

    def tab_direction(self, words):
        direction = '{ctrl+shift+tab}'
        if 'right' in [words[-1], words[-2]]:
            direction = '{ctrl+tab}'
        num = baseutils.last_number(words)
        for i in range(num):
            api.send_string(direction)
            if i + 1 < num:
                time.sleep(.2)

    def gogo(self, words):
        api.send_string('2-2-{}-ff$$'.format(words[-1]))
