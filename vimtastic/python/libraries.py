from pynhost import api
from pynhost import constants, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension

class PyCommandsGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['priority'] = 1
        self.mapping = {
        'os.path.join': 'os.path.join(){left}',
        '<hom_sys>': 'sys',
        'shuttle': 'shutil',
        'l xml': 'lxml',
        'os': 'os',
        'sub process': 'subprocess',
        'glob': 'glob',
        'temp file': 'tempfile',
        'zip file': 'zipfile',
        'it or tools': 'itertools',
        'collections': 'collections',
        '(each tree)': 'etree',
        }
    
    def _load_grammar(self):
        return extension.current_language in ['python3', 'python2']

class OSLibraryGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['priority'] = 1
        self.mapping = {
        '<hom_os> <hom_walk>': 'os.walk(){left}',
        '<hom_os> <hom_join>': 'os.path.join(){left}',
        '<hom_os> <hom_relpath>': 'os.path.relpath(){left}'
        }
    
    def _load_grammar(self):
        return extension.current_language in ['python3', 'python2']

class CopyLibraryGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['priority'] = 1
        self.mapping = {
        '<hom_copy> <hom_copy>': 'copy.copy(){left}',
        '<hom_copy> <hom_deep> <hom_copy>': 'copy.deepcopy(){left}',
        }
    
    def _load_grammar(self):
        return extension.current_language in ['python3', 'python2']