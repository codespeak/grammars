import subprocess
import os
import difflib
import threading
from pynhost import grammarbase
from pynhost import api
from pynhost import dynamic
from pynhost import grammarbase
from pynhost.grammars import baseutils, extension

class ContextManagerGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_enable> <hom_html>': self.enable_html,
            '<hom_disable> <hom_html>': self.disable_html,
            '<hom_enable> <hom_django>': self.enable_django,
            '<hom_disable> <hom_django>': self.disable_html,
        }


    def enable_html(self, words):
        self._change_global_context('html enabled', True)

    def disable_html(self, words):
        self._change_global_context('html enabled', False)

    def enable_django(self, words):
        self._change_global_context('django enabled', True)

    def disable_django(self, words):
        self._change_global_context('django enabled', False)
