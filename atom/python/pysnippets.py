from pynhost import api
from pynhost.grammars.atom import atomextension, atomutils
from pynhost.grammars.atom.python import pyextension

class PythonSnippetsGrammar(pyextension.PyExtensionGrammar):

    def __init__(self):
        super().__init__()
        self.app_context = r'Autumntastic.+?\.py'
        self.mapping = {
            '<hom_new> (<hom_func> | <hom_function>)': self.new_function,
            '<hom_new> <hom_class>': 'class :{left}',
            '<hom_new> <hom_method>': 'def (self):' + '{left}' * 7,
            '<hom_new> <hom_initializer>': 'def __init__(self):{left}{left}',
            'sulfur': 'self.',
        }

    def new_function(self, words):
        text = 'def (){left}{left}'
        api.send_string(text)
