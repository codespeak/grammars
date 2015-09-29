from pynhost import api
from pynhost.grammars.atom import atomextension, atomutils
from pynhost.grammars.atom.javascript import jsextension

class JavascriptSnippetsGrammar(jsextension.JsExtensionGrammar):

    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_new> (<hom_func> | <hom_function>)': 'function () {{{enter}{enter}}}' + '{left}' * 8,
            '<hom_new> <hom_class>': 'class :{left}',
            '<hom_new> <hom_read>': "with open(, 'r') as f:" + '{left}' * 12,
            '<hom_new> <hom_method>': 'def (self):' + '{left}' * 7,
            '<hom_new> <hom_initializer>': 'def __init__(self):{left}{left}',
            '<hom_scope>': '{{}}{left}{enter}',
            '<hom_loop> <hom_clip>': 'for (var i = 0; i < {ctrl+v}.length; i++) {{{enter}{enter}{back}}}{up}{right}'
        }
