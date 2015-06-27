from pynhost import grammarbase
from pynhost.grammars import baseutils

class Grammar(grammarbase.GrammarBase):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '(go to <hom_sleep>)': self.go_to_sleep,
        }

    def go_to_sleep(self, words):
        self._change_global_context('language', words[-1])
