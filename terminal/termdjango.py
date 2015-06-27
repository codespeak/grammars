import time
from pynhost import api, dynamic
from pynhost.grammars import extension, baseutils
from pynhost.grammars.terminal import termextension


class TerminalDjangoGrammar(termextension.TerminalExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_django> run': self.run_server,
            '<hom_django> start <hom_project>': 'django-admin.py startproject ',
            '<hom_django> start application': 'python3 manage.py startapp ',
        }

    def run_server(self, words):
        api.send_string('python3 manage.py runserver{enter}')
        time.sleep(.5)
        result = baseutils.focus_or_launch_program('Vimperator', 'firefox')
        time.sleep(.5)
        if result == 'focus':
            api.send_string('{esc}{ctrl+t}')
        time.sleep(1)
        api.send_string('{ctrl+l}')
        time.sleep(5.5)
        api.send_string('127.0.0.1:8000{enter}')

    def new_child(self, words):
        if words[-1].isdigit():
            api.send_string('{} gg'.format(words[-1]))
        api.send_string('ma')

    def go_to_dir(self, words):
        pass
