import subprocess
import os
import difflib
import threading
from pynhost import grammarbase
from pynhost import api
from pynhost import dynamic
from pynhost import grammarbase
from pynhost.grammars import baseutils, extension

class HTMLGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_tag>': '<>{left}',
        }
        self.context_filters = {
            'html enabled': True,
        }
