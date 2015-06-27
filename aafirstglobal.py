import subprocess
import os
import difflib
import threading
from pynhost import grammarbase
from pynhost import api
from pynhost import dynamic
from pynhost import grammarbase
from pynhost.grammars import baseutils, extension

class FirstGlobalGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['filtered words'] = []
        self.mapping = {
        '<hom_say> <any> <1->': self.literal,
        }

    def literal(self, words):
        api.send_string(' '.join(words[1:]))
