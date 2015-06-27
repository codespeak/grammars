import subprocess
import time

from pynhost import api
from pynhost.grammars import baseutils
from pynhost.grammars.atom import atomextension
from pynhost.grammars.atom import atomutils as au
from pynhost.grammars.atom.python import pyextension

class PythonGeneralGrammar(pyextension.PyExtensionGrammar):

    def __init__(self):
        super().__init__()
        self.app_context = r'Autumntastic.+?\.py'
        self.mapping = {
            '(<hom_debug>|to bug)': self.debug,
            '{} (<hom_function> | <hom_class>)'.format(
                baseutils.list_to_rule_string(au.ACTIONS)): self.modify_function,
        }

    def modify_function(self, words):
        api.send_string(au.OTHER['select{}'.format(words[-1].title())])
        au.do_action(words[0])

    def debug(self, words):
        api.send_string('{ctrl+s}')
        clipboard_contents = baseutils.get_clipboard_contents()
        api.send_string(au.OTHER['filePathToClipboard'])
        subprocess.call(['x-terminal-emulator'])
        time.sleep(1)
        api.send_string('python3 {ctrl+shift+v}{enter}')
        baseutils.set_clipboard_contents(clipboard_contents)
