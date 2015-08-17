from pynhost import api
from pynhost import dynamic
from pynhost.grammars import baseutils, extension
from pynhost.grammars.web.django import djangoextension

class DjangoTemplateGrammar(djangoextension.DjangoExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '(<hom_template>|<hom_temp>) <hom_variable>': '{{{{  }}}}{left}{left}{left}',
            '(<hom_template>|<hom_temp>) <hom_block>': '{{% block  %}}{left}{left}{left}',
        }
