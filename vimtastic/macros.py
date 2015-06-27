from pynhost.grammars import baseutils, extension
from pynhost.grammars.vimtastic import vimextension

class VimMacrosGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['filtered words'].append('to')
        self.dictionary = baseutils.ALPHABET
        self.mapping = {
            '<hom_macro> <hom_record> {}'.format(baseutils.list_to_rule_string(baseutils.ALPHABET)): self.record_macro,
            '<hom_macro> <hom_save>': self.save_macros,
        }
        self.settings['filtered words'].append('and')

    def record_macro(self, words):
        self._begin_recording_macro('<hom_macro> <hom_{}>'.format(words[-1]))

    def save_macros(self, words):
        self._finish_recording_macros()    
