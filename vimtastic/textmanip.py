import time
from pynhost import api
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension

class VimManipGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.goto_rule_pieces = [
            '({}) [<num>]'.format(' | '.join([baseutils.homify_text(m) for m in vimutils.motions if m not in vimutils.make_outer_list(vimutils.text_objects)])),
            '(<hom_blue> | <hom_fish> | <hom_bill> | <hom_till> | until) ([<hom_grow>] {} | {}) [<num>]'.format(
                baseutils.list_to_rule_string(list(baseutils.ALPHABET)),
                baseutils.list_to_rule_string(list(baseutils.CHAR_MAP))),
            '(<hom_climb> | <hom_drop>) [<num>]',
            '<hom_matching>',
        ]
        self.motion_rule_pieces = [
            '{} [<num>]'.format(baseutils.list_to_rule_string(list(vimutils.motions))),
            '<num> [(<hom_fish> | to | <hom_through>) <num>]',
            baseutils.list_to_rule_string(list(vimutils.single_motions)),
            '(<hom_blue> | <hom_fish> | <hom_bill> | <hom_till> | <hom_until>) ([<hom_grow>] {} | {}) [<num>]'.format(
                baseutils.list_to_rule_string(list(baseutils.ALPHABET)),
                baseutils.list_to_rule_string(list(baseutils.CHAR_MAP))),
            '<hom_mint> <num>',
        ]

        self.mapping = {
            '({})'.format(' | '.join(self.goto_rule_pieces)): self.goto,
            '(<hom_line> | <hom_lend>) <num>': self.goto_line,
            '(<hom_grab> | <hom_copy> | <hom_kill> | <hom_select>) ({})'.format(' | '.join(self.motion_rule_pieces)): self.movement_func,
            '(<hom_grab> | <hom_copy> | <hom_kill> | <hom_select>) <end>': self.single_action,
            '<hom_surround> ({0}) ({1})'.format(' | '.join(self.motion_rule_pieces), baseutils.list_to_rule_string(list(vimutils.text_objects))): self.surround,
            '<hom_scramble> ({0}) ({0})'.format(baseutils.list_to_rule_string(list(vimutils.text_objects))): self.surround_change,
            'remove {}'.format(baseutils.list_to_rule_string(list(vimutils.text_objects))): self.surround_remove,
            '<hom_paste> [<hom_strip>] [(<num> | (<hom_climb> | <hom_drop>) [<num>])]': self.paste,
            'clear': '{escape}^"_Da',
            '<num> <hom_touch> <num> [(<hom_grab> | <hom_copy> | <hom_kill> | <hom_select>)]': self.goto_word_num,
            'inch': self.paste_block,
        }

    def goto(self, words):
        if words[0] in ['climb', 'drop']:
            vimutils.handle_above_below_goto(words)
            return
        num = '1'
        if words[-1].isdigit():
            num = words.pop()
        words[0] = vimutils.get_motion_homonym(words[0])
        if words[0] in ['up', 'down', 'left', 'right']:
            if float(num) <= 0:
                api.send_string('{' + words[0] + '}' + num)
            for i in range(int(num)):
                api.send_string('{' + words[0] + '}')
            return
        if words[0] == 'matching':
            api.send_string(vimutils.FUNCTIONS['smart escape'] + '%' + 'a') 
        elif words[0] in vimutils.motions:
            vimutils.handle_direction_goto(words, num)
        elif words[0] in vimutils.through:
            c = baseutils.get_single_character(words[-1], words[-2] == 'grow')
            api.send_string('{F11}' + num + vimutils.through[words[0]][0] + c)
            if words[0] in ['bill', 'blue']:
                api.send_string('i')
            else:
                api.send_string('a')

    def movement_func(self, words):
        if len(words) == 1:
            api.send_string('{F11}' + vimutils.commands[words[0]])
            return
        if not words[-1].isdigit():
            words.append('1')
        if words[0] in ['copy', 'surround']:
            api.send_string('{alt+1}') # mark cursor pos
        if ' '.join(words[1:-1]) in vimutils.motions:
            words = vimutils.combine_words(words)
        words[1] = vimutils.get_motion_homonym(words[1])
        if words[1] in vimutils.motions:
            handle_motion(words)
            return
        else:
            if words[1].isdigit():
                handle_line_motion(words)
                return
            elif words[1] == 'mint':
                handle_arg_motion(words)
                return
            if words[1] == 'line':
                handle_single_line(words)
            elif words[1] in vimutils.single_motions:
                api.send_string('{F11}') # normal or visual mode
                api.send_string(vimutils.single_motions[words[1]].replace('<m>', vimutils.commands[words[0]]))
            elif words[1] == 'matching':
                api.send_string('{F11}') # normal or visual mode
                api.send_string(vimutils.FUNCTIONS['smart escape'] + vimutils.commands[words[0]] + '%' + 'a')
            elif words[1] in vimutils.through:
                handle_char_motion(words)

    def surround(self, words):
        if not words[-2].isdigit():
            words.insert(-1, '1')
        num = words[-2]
        text_object = vimutils.text_objects[words[-1]]
        if words[1] == 'line':
            api.send_string('{esc}^ys$' + text_object + 'i')
            return
        motion = vimutils.motions[words[1]]
        editing_command = 'ys' + num + motion + text_object
        if words[1].isdigit():
            pass
        elif words[1] in vimutils.motions:
            if words[1] in ['left', 'back', 'first', 'absolute', 'brink']:
                api.send_string('{escape}ma$a{space}{escape}`a{right}')
                api.send_string(editing_command)
                api.send_string('ma$x`ai')
            elif words[1] in ['right', 'next', 'final', 'ring']:
                api.send_string('{space}{escape}{right}ma')
                api.send_string(editing_command)
                api.send_string('`ai{backspace}')
            else:
                api.send_string('{F2}'+ editing_command)
                time.sleep(.1)
                api.send_string('i')

    def goto_line(self, words):
        api.send_string('{escape}' + words[-1] + 'gg')
        if words[0] == 'line':
            api.send_string('{shift+6}i')
        else:
            api.send_string('{shift+4}a')

    def paste(self, words):
        if len(words) > 1 and words[1] == 'strip':
            contents = baseutils.get_clipboard_contents().strip()
            baseutils.set_clipboard_contents(contents)
            del words[1]
        if len(words) == 1:
            api.send_string('{ctrl+v}')
            return
        if len(words) > 1 and words[1].isdigit():
            api.send_string('{{escape}}{}gg'.format(words[-1]))
        api.send_string('p')

    def matching_motion(self, words):
        motion = vimutils.motions[words[0]]
        api.send_string('{F11}') # normal or visual mode
        if len(words) == 1:
            api.send_string(motion)
            if words[0] in ['grab', 'kill']:
                api.send_string('i')
            return
        api.send_string(vimutils.FUNCTIONS['smart escape'] + motion + '%' + 'a')

    def surround_change(self, words):
        text_object1 = vimutils.text_objects[words[-2]]
        text_object2 = vimutils.text_objects[words[-1]]
        editing_command = '{alt+1}{F2}cs' + text_object1 + text_object2 + 'i{alt+2}'
        api.send_string(editing_command)

    def surround_remove(self, words):
        text_object = vimutils.text_objects[words[-1]]
        editing_command = '{alt+1}{F2}ds' + text_object + 'i{alt+2}'
        api.send_string(editing_command)

    def paste_block(self, words):
        api.send_string('{alt+1}{ctrl+v}{backspace}{alt+2}')

    def goto_word_num(self, words):
        command = ''
        if not words[-1].isdigit():
            command = vimutils.commands[words[-1]].replace('c', 'd')
        if int(words[2]) <= 0:
            return
        action = '{alt+1}{esc}' + words[0] + 'gg^'
        if int(words[2]) > 1:
            action += '{}w'.format(str(int(words[2]) - 1))
        if command:
            action += command + 'iwi{alt+2}'
        else:
            action += 'i'
        api.send_string(action)

    def single_action(self, words):
        api.send_string('{F11}' + vimutils.commands[words[0]])


def handle_single_line(words):
    api.send_string('{F11}') # normal or visual mode
    merged = ' '.join(words[:-1])
    merged_map = {
        'kill line': '{escape}"_ddi',
        'select line': '{F12}V',
        'kill climb': '{escape}{up}"_ddi',
        'select climb': '{up}{F12}V',
        'kill drop': '{escape}{down}"_ddi',
        'select drop': '{down}{F12}V',
    }
    if merged in merged_map:
        api.send_string(merged_map[merged])
        return
    if words[1] == 'line':
        api.send_string(words[-1])
    api.send_string(vimutils.single_motions[words[1]].replace('<m>', vimutils.commands[words[0]]))

def handle_char_motion(words):
    editing_command = ''
    char = baseutils.get_single_character(words[-2], words[-3] == 'grow')
    if 'grow' in words:
        char = char.upper()
    num = words[-1]
    editing_command += (num + vimutils.commands[words[0]] +
        vimutils.through[words[1]][0] + char)
    if words[1] in ['bill', 'blue']: # grab or kill
        if words[0] == 'copy':
            api.send_string('{space}{escape}mz' + editing_command + '{alt+1}{F11}`zxi{alt+2}')
        else:
            api.send_string('{space}{escape}ma' + editing_command + '{delete}')
    else:
        if words[0] in ['grab', 'kill']: # grab or kill
            api.send_string('{alt+1}{space}{escape}{right}' + editing_command + '{alt+2}{alt+3}')
        else:
            api.send_string('{alt+1}{space}{escape}{right}' + editing_command + 'i{alt+2}{delete}')

def get_motion(words):
    if words[-1].isdigit():
        motion = vimutils.motions[' '.join(words[1:-1])]
    else:
        motion = vimutils.motions[' '.join(words[1:])]
    return motion

def handle_motion(words, surround=False):
    motion = vimutils.motions[words[1]]
    num = words[-1]
    command = vimutils.commands[words[0]]
    editing_command = num + command + motion
    if words[0] == 'select':
        api.send_string('{F11}' + editing_command)
        return
    else:
        if words[1] in ['left', 'back', 'first', 'absolute']:
            if command == 'y': # copy
                api.send_string('{space}{escape}ma' + editing_command + 'mb`ax`bi')
            else:
                api.send_string('{space}{escape}ma' + editing_command + '{delete}')
        elif words[1] == 'brink':
            if command == 'y': # copy
                api.send_string('{space}{escape}ma{left}ge{right}' + command + '`a`axa')
            else:
                api.send_string('{space}{escape}ma{left}ge{right}' + command.replace('c', 'd') + '`aa{backspace}')            
        elif words[1] in ['right', 'next', 'ring', 'final']:
            if command in ['c', '"_c']: # grab or kill
                api.send_string('{alt+1}{space}{escape}{right}' + editing_command + '{alt+2}{alt+3}')
            else:
                api.send_string('{alt+1}{space}{escape}{right}' + editing_command + 'i{alt+2}{delete}')
        else:
            if motion in ['iw', 'aw']:
                api.send_string('{F2}')
            else:
                api.send_string('{esc}')
            api.send_string(editing_command)
            if command == 'y':
                api.send_string('i{alt+2}') #return from whence we came

def handle_line_motion(words):
    command = vimutils.commands[words[0]]
    s = sorted(words[1::2], key=int)
    api.send_string('{alt+1}{F11}')
    if command in ['"_c', 'c', '{F12}']:
        if command == '"_c': #kill
            api.send_string(':{},{}d"_d'.format(s[0], s[-1]) + '{enter}i{alt+2}')
        elif command == 'c': # grab
            api.send_string(':{},{}d'.format(s[0], s[-1]) + '{enter}i{alt+2}')
        else: # select
            api.send_string('{}GV{}G'.format(s[0], s[-1]))
    else:
        api.send_string(':{},{}{}'.format(s[0], s[-1], command) + '{enter}i{alt+2}')

def handle_arg_motion(words):
    command = vimutils.commands[words[0]].replace('c', 'd')
    api.send_string('{alt+1}{escape}l?')
    api.send_string(r'({enter}{alt+4}') #go to first word in paren, mark closing paren with t
    if words[-1] != '1':
        api.send_string(str(int(words[-1]) - 1) + r'/,{enter}w')
    api.send_string('{alt+6}') # move mark t to next comma if it's closer
    api.send_string(command + '`t')
    if command in ['"_d', 'd']:
        api.send_string(r'{alt+5}')
    else:
        api.send_string('i{alt+1}')
