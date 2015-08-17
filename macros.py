from pynhost import grammarbase
from pynhost import api
from pynhost.grammars import baseutils, extension


class MacrosGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.dictionary = baseutils.ALPHABET
        self.mapping = {
            '<hom_macro> <hom_record> <any> <1>': self.start_macro,
            '<hom_macro> <hom_save>': self.finish_macro,

        }
        self.capital = False

    def start_macro(self, words):
        self._begin_recording_macro('macro {}'.format(baseutils.homify_text(words[-1])))

    def finish_macro(self, words):
        self._finish_recording_macros()
