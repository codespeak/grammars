import configparser
import os
from pynhost.grammars import baseutils
from pynhost import grammarbase
from pynhost import api
from pynhost import constants

class ExtensionGrammar(grammarbase.GrammarBase):

    string_delim = "'"
    dirs = {
        'django': '~/Modules/Python/Python3/django/',
        'music': '/home/evan/Music',
        'modules': '~/Modules',
        'root': '/',
        'home': '~',
        'python': '~/Modules/Python/Python3/',
    }
    django_dir = '~/Modules/Python/Python3/django/'
    modules_dir = '~/Modules'
    current_language = 'python3'

    def __init__(self):
        super().__init__()
        self.settings['filtered words'] = [
            'the',
            'is',
            'a',
            'of',
            'at',
        ]
        self.mapping = {
        }

    def set_language(self, words):
        language_map = {
            'python': 'python3',
            'c++': 'c++',
            'c+': 'c++',
            'c plus plus': 'c++',
            'javascript': 'javascript',
        }
        language = language_map[''.join(words[1:])]
        ExtensionGrammar.current_language = language
