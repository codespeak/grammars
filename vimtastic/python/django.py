import os
import subprocess
from pynhost import api, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension


class DjangoGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_django> migrate': self.migrate,
            '<hom_django> <hom_block>': self.block,
            '<hom_django> <hom_tag>': '{{%  %}}{left}{left}{left}',
            '<hom_django> <hom_comment>': '{{#  #}}{left}{left}{left}',
            '<hom_django> <hom_variable>': '{{{{  }}}}{left}{left}{left}',
            '<hom_django> <hom_else>': r'{{% else %}}',
            '<hom_django> (<hom_end> | <hom_and>) <hom_if>': r'{{% endif %}}',
            '<hom_django> (<hom_end> | <hom_and>) (4 | <hom_for> | <hom_four>)': r'{{% endfor %}}',
            '121 <hom_field>': 'OneToOneField',
        }

    def migrate(self, words):
        filepath = vimutils.get_clipboard_contents('{F11}{space}1a')
        project_dir = vimutils.get_django_project_root(filepath)
        if project_dir is not None:
            os.chdir(project_dir)
            subprocess.call(['python3', 'manage.py', 'migrate'])
            subprocess.call(['python3', 'manage.py', 'makemigrations'])

    def block(self, words):
        api.send_string(r'{{% block  %}}{{% endblock %}}' + '{left}' * 17)