import tempfile
from pynhost.grammars.vimtastic import vimutils, vimextension


class HaskellVimExtensionGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        }

        self.context_filters = {
            'language': 'haskell'
        }
        self.home_dir = '/home/evan/Modules/haskell'

    def compile_haskell(filename):
        errs = []
        _, temp_name = tempfile.mkstemp()
        results = api.send_string(' {} | tee -a {} 1>&2'.format(filename, temp_name) + '{enter}')
