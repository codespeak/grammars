from pynhost.grammars import baseutils, extension

class ContextsGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'language (<hom_python> [(2 | 3)] | javascript | (c++ | c+ | c plus plus) | <hom_haskell>)': self.set_language,
        }

    def set_language(self, words):
        self._change_global_context('language', words[-1])
