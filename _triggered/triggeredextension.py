from pynhost import grammarbase

class TriggeredExtensionGrammar(grammarbase.TriggeredGrammarBase):
    def __init__(self):
        super().__init__()
        self.app_context = ''
        self.mapping = {
            'trigger list': ',{enter}',
        }
