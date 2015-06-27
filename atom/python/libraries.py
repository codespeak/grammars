from pynhost import api
from pynhost import constants, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension
from pynhost.grammars.atom.python import pyextension

class PyCommandsGrammar(pyextension.PyExtensionGrammar):
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

class OSLibraryGrammar(pyextension.PyExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['priority'] = 1
        self.mapping = {
            '<hom_os> <hom_walk>': 'os.walk(){left}',
            '<hom_os> <hom_join>': 'os.path.join(){left}',
            '<hom_os> <hom_relpath>': 'os.path.relpath(){left}'
        }

class CopyLibraryGrammar(pyextension.PyExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['priority'] = 1
        self.mapping = {
            '<hom_copy> <hom_copy>': 'copy.copy(){left}',
            '<hom_copy> <hom_deep> <hom_copy>': 'copy.deepcopy(){left}',
        }
