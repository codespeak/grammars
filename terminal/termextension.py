from pynhost.grammars import extension

class TerminalExtensionGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.app_context = 'terminal'
