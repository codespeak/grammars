from pynhost import api
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension


class VariablesGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_variable> ({} | <hom_num>)': self.set_variable,
            '<hom_loop>': self.var_for_loop,
            #'<hom_check>': self.var_if,
            'england': self.var_elif,
            'extension': self.get_file_extension
        }

        self.dictionary = baseutils.ALPHABET

    def set_variable(self, words):
        vimextension.VimExtensionGrammar.current_var = words[-1]

    def var_for_loop(self, words):
        if vimextension.VimExtensionGrammar.current_var is not None:
            api.send_string('for {} in '.format(vimextension.VimExtensionGrammar.current_var))

    def var_if(self, words):
        if vimextension.VimExtensionGrammar.current_var is not None:
            api.send_string('if {} '.format(vimextension.VimExtensionGrammar.current_var))

    def var_elif(self, words):
        if vimextension.VimExtensionGrammar.current_var is not None:
            api.send_string('elif {} '.format(vimextension.VimExtensionGrammar.current_var))
