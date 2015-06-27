import os
import subprocess
from pynhost import api, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension


class PyVimExtensionGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        }

        self.context_filters = {
            'language': 'python'
        }

