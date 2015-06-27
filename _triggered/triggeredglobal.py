from pynhost import api, dynamic
from pynhost.grammars._triggered import triggeredextension

class BeforeAsyncGrammar(triggeredextension.TriggeredExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.app_context = ''
        self.mapping = {
            'trigger repeat': 1,
        }

class AfterAsyncGrammar(triggeredextension.TriggeredExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.app_context = ''
        self.settings['timing'] = 'after'
        self.mapping = {
            '<hom_trigger> <hom_sequence>': ',{enter}',
        }

class BothAsyncGrammar(triggeredextension.TriggeredExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.app_context = ''
        self.settings['timing'] = 'both'
        self.even_count = True
        self.mapping = {
            '<hom_trigger> <hom_string>': self.smart_apostrophe,
            '<hom_trigger> <hom_clear>': dynamic.ClearTriggered(),
        }

    def smart_apostrophe(self, words):
        text = "'"
        if not self.even_count:
            text += '{esc}bea{space}{esc}"_ct\'{right}'
        api.send_string(text)
        self.even_count = not self.even_count

