import subprocess
import time
import os
from pynhost import api, dynamic, utilities
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils

class VimGeneralGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        '<hom_save>': 'zz',
        '<hom_scratch> [<num>]': self.undo,
        '<hom_redo> [<num>]': self.redo,
        '[<num>] <hom_halt> [<num>]': self.args,
        '(norm | normal)': '{escape}',
        '(<hom_shoot> | <hom_ball>)': self.indent,
        '(debug | to bug)': self.debug,
        '<hom_recur>': '{escape}mbi{F6}{escape}`b"apa(){left}',
        'mode (camel | score | title | upper)': self.change_variable_mode,
        '<hom_stack> [(function | class | variable | list | dictionary)] [<num>]': self.definition_stack,
        '(search | <hom_relapse>) [(<num> | <any> <1->)]': self.search,
        '<hom_replace> [<any> <1->]': self.replace,
        '<hom_buff> <hom_shell>': self.launch_shell,
        }

        self.dictionary = baseutils.CHAR_MAP

    def args(self, words):
        if words[0].isdigit():
            api.send_string(words[0])
        api.send_string(', ')
        if words[-1].isdigit():
            api.send_string(words[-1])

    def change_variable_mode(self, words):
        vimextension.VimExtensionGrammar.variable_mode = words[-1]

    def debug(self, words):
        api.send_string('zz')
        clipboard_contents = baseutils.get_clipboard_contents()
        api.send_string("{escape}:let @+ = expand('%:p'){enter}")
        subprocess.call(['x-terminal-emulator'])
        time.sleep(1)
        api.send_string('python3 {ctrl+shift+v}{enter}')
        baseutils.set_clipboard_contents(clipboard_contents)

    def set_main(self, words):
        self._set_setting('main_file', vimutils.get_current_window_path())

    def definition_stack(self, words):
        num = 1
        if words[-1].isdigit():
            num = int(words[-1])
        word_type = 'all'
        if len(words) > 1:
            if not words[-1].isdigit():
                word_type = words[-1]
            elif words[-2] != 'stack':
                word_type = words[-2]
        count = 0
        for definition in reversed(vimextension.VimExtensionGrammar.definitions):
            if word_type == 'all' or definition.endswith(word_type):
                count += 1
            if count == num:
                api.send_string('_'.join(definition.split('_')[:-1]))
                if word_type == 'function':
                    api.send_string('()')
                return

    def indent(self, words):
        indent_commands = {
            'shoot': '{alt+h}',
            'ball': '{alt+l}',
        }
        cmd = indent_commands[words[0]]
        num = baseutils.set_number(words)
        if num == '1':
            api.send_string(cmd)
            return
        api.send_string('{escape}' + num + indent_commands[words[0]] + 'i')

    def undo(self, words):
        num = '1'
        if words[-1].isdigit():
            num = words[-1]
        api.send_string('{esc}' + num + 'ui')

    def redo(self, words):
        num = '1'
        if words[-1].isdigit():
            num = words[-1]
        api.send_string('{esc}' + num + '{ctrl+r}a')
        
    def search(self, words):
        search_char = '/'
        if words[0] == 'relapse':
            search_char = '?'
        num = '1'
        if len(words) > 2 and words[1].isdigit():
            num = words[1]
            del words[1]             
        api.send_string('{esc}' + num + search_char)
        if len(words) > 1:
            # case insensitive
            api.send_string('\c' + vimutils.guess_at_text(words[1:]) + '{enter}i')

    def replace(self, words):
        if len(words) == 1:
            api.send_string('{esc}:%s///g{left}{left}{left}')
            return
        api.send_string(r'{alt+1}{esc}:%s/\<{ctrl+r+w}\>/'+ vimutils.guess_at_text(words[1:]) + '/g{enter}i{alt+2}')

    def launch_shell(self, words):
        buff_path = vimutils.get_clipboard_contents("{escape}:let @+ = expand('%:p'){enter}")
        subprocess.call(['x-terminal-emulator'])
        time.sleep(1)
        print(os.path.split(buff_path))
        api.send_string('cd ' + os.path.split(buff_path)[0] + '{enter}')