import subprocess
import time
import os
from pynhost import api, dynamic, utilities
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils

class VimGeneralGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):

        self.tags = {
            'form': 'form',
            'button': 'button',
            'div': 'div',
            'body': 'body',
            'head': 'head',
            'paragraph': 'p',
            'list item': 'li',
        }

        self.attrs = [
            'class',
            'id',
            'type',
            'role',
            'action',
        ]

        super().__init__()
        self.mapping = {
        '<hom_mark> <hom_link>': '<a href="">{left}{left}',
        '<hom_mark> <hom_close> <hom_div>': '</div>',
        '<hom_mark> <hom_tag>': '<>{left}',
        '<hom_mark> {} [<hom_close>]'.format(baseutils.list_to_rule_string(self.tags)): self.tag,
        '<hom_mark> {}'.format(baseutils.list_to_rule_string(self.attrs)): self.create_attribute,
        }

    def tag(self, words):
        text = '<'
        if words[-1] == 'close':
            text += '/'
        text += self.tags[' '.join(words[1:])]
        text += '>'
        if words[-1] != 'close':
            text += '{left}'
        api.send_string(text)

    def create_attribute(self, words):
        text = vimutils.FUNCTIONS['SmartSpace'] + words[1] + '=""{left}'
        api.send_string(text)
