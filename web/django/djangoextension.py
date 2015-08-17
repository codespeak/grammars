from pynhost import api
from pynhost import dynamic
from pynhost.grammars import baseutils, extension

class DjangoExtensionGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        
        self.context_filters = {
            'django enabled': True,
        }
