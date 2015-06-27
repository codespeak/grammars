import collections
from pynhost import api
from pynhost.grammars.vimtastic import vimutils
from pynhost.grammars import baseutils, extension

class VimExtensionGrammar(extension.ExtensionGrammar):
    vim_enabled = True
    current_var = None
    variable_mode = 'score'
    definitions = []
    def __init__(self):
        super().__init__()
        self.app_context = 'vimtastic'
        self.extensions = {
            'python3': '.py',
            'python2': '.py',
            'javascript': '.js',
        }

    def _check_grammar(self):
        return VimExtensionGrammar.vim_enabled

    def get_file_extension(self, words):
        api.send_string(self.extensions[extension.ExtensionGrammar.current_language])