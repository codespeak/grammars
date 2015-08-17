from pynhost import api
from pynhost.grammars.atom import atomextension, atomutils
from pynhost.grammars.atom.python import pyextension

class PythonSnippetsGrammar(pyextension.PyExtensionGrammar):

    def __init__(self):
        super().__init__()
        self.app_context = r'Autumntastic.+?\.py'
        self.mapping = {
            '<hom_new> (<hom_func> | <hom_function>)': 'def ():{left}{left}{left}',
            '<hom_new> <hom_class>': 'class :{left}',
            '<hom_new> <hom_read>': "with open(, 'r') as f:" + '{left}' * 12,
            '<hom_new> <hom_method>': 'def (self):' + '{left}' * 7,
            '<hom_new> <hom_initializer>': 'def __init__(self):{left}{left}',
            'sulfur': 'self.',
        }

# def print_even_numbers(fname):
#     with open(fname, 'r') as f:
#         for line in fname:
#             if int(line.strip()) % 2 == 0:
#                 print(line)
