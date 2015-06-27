import time
from pynhost import api, dynamic
from pynhost.grammars import extension, baseutils
from pynhost.grammars.atom import atomextension, atomutils

class AtomTextManipulationGrammar(atomextension.AtomExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '[{}]{}[<num>]'.format(baseutils.list_to_rule_string(atomutils.ACTIONS),
                                   baseutils.list_to_rule_string(atomutils.MOTIONS)): self.do_motion,
            '{} <hom_beer>'.format(baseutils.list_to_rule_string(atomutils.ACTIONS)): self.line_action,
            '{} [<hom_outer>] {}'.format(baseutils.list_to_rule_string(atomutils.ACTIONS),
                        baseutils.list_to_rule_string(atomutils.SURROUND_OBJECTS)): self.do_surround,
            '{} [<hom_outer>] {}'.format(baseutils.list_to_rule_string(atomutils.ACTIONS),
                        baseutils.list_to_rule_string(atomutils.STRING_OBJECTS)): self.do_surround_same,
            '[{}] {} {} [<num>]'.format(baseutils.list_to_rule_string(atomutils.ACTIONS),
                           baseutils.list_to_rule_string(atomutils.INCREMENTAL_LIMITS),
                           baseutils.list_to_rule_string(list(self.search_chars))): self.incremental_search,
            '(<hom_beer> | <hom_grab> | <hom_copy> | <hom_kill> | <hom_select>) <num>': self.single_line,
        }

    def line_goto(self, words):
        api.send_string('{ctrl+g}')
        time.sleep(.3)
        api.send_string(words[-1] + '{enter}')

    def do_motion(self, words):
        if not words[-1].isdigit():
            words.append('1')
        select_default = 's'
        if words[0] not in atomutils.ACTIONS:
            select_default = 'm'
        api.send_string(self.activate + select_default + atomutils.MOTIONS[words[-2]] + words[-1] + '!')
        atomutils.do_action(words[0])

    def line_action(self, words):
        api.send_string('{ctrl+l}')
        atomutils.do_action(words[0])

    def do_surround(self, words):
        text = self.activate + '1-' + atomutils.ACTIONS[words[0]] + '-s-'
        text += ''.join(atomutils.SURROUND_OBJECTS[words[-1]])
        if words[1] != 'outer':
            text += 'i'
        api.send_string(text + '`^')

    def do_surround_same(self, words):
        text = self.activate + '1-' + atomutils.ACTIONS[words[0]]
        if words[1] == 'outer':
            text += '-a-'
        else:
            text += '-i-'
        text += ''.join(atomutils.STRING_OBJECTS[words[-1]]) + '`^'
        api.send_string(text)

    def incremental_search(self, words):
        if not words[-1].isdigit():
            words.append('1')
        action = atomutils.ACTIONS.get(words[0], 'm')
        limit = atomutils.INCREMENTAL_LIMITS[words[-3]]
        search_value = self.search_chars[words[-2]]
        num = words[-1]
        api.send_string(self.activate + '{}-{}-{}-{}`^'.format(num, action, limit, search_value))

    def single_line(self, words):
        api.send_string('{}m{}{}!'.format(self.activate, atomutils.SIMPLE['line'], words[-1]))
        if words[0] != 'beer':
            api.send_string('{ctrl+l}')
            atomutils.do_action(words[0])

class AtomTextManipulationGrammar2(atomextension.AtomExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '(<hom_grab> | <hom_copy> | <hom_kill> | <hom_select>) <num> (<hom_through> | <hom_fish>) <num>': self.multiple_lines,
        }
        self.settings['priority'] = 2

    def multiple_lines(self, words):
        api.send_string('{}m{}{}!'.format(self.activate, atomutils.SIMPLE['line'], str(int(words[1]) - 1)))
        api.send_string('{ctrl+l}')
        api.send_string('{}s{}{}!'.format(self.activate, atomutils.SIMPLE['line'], words[-1]))
        api.send_string('{ctrl+l}')
        atomutils.do_action(words[0])
