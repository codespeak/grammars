import subprocess
import time
import os
from pynhost import api, grammarbase

from pynhost.grammars import baseutils, extension

class CharsGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '{} [<num>]'.format(baseutils.list_to_rule_string(baseutils.CHAR_MAP)): self.print_char,
        }

    def print_char(self, words):
        num = 1
        if len(words) == 2:
            num = int(words[-1])
        chars = baseutils.CHAR_MAP[words[0]] * num
        api.send_string(chars)
