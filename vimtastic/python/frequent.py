from pynhost import api
from pynhost import constants, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension

class PyCommandsGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['filtered words'].remove('is')
        self.mapping = {
        '<hom_free> <hom_root>': 'root',
        '<hom_free> <hom_path>': 'path',
        # '<hom_in>': '{}in{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        }