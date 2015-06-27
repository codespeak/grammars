import configparser
import os
import time
import subprocess
from pynhost.grammars import baseutils, extension
from pynhost import grammarbase
from pynhost import api
from pynhost import dynamic
from pynhost import constants

class VimperatorGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.app_context = 'vimperator'
        self.mapping = {
            '<hom_high>': '{escape}{escape}{ctrl+b}',
            '(<hom_low> | below)': '{escape}{escape}{space}',
            '<hom_back> [<num>]': ['{escape}{shift+h}', dynamic.Num().add(-1)],
            '<hom_next>': '{escape}{shift+l}',
            '<hom_link>': '{escape}{escape}f',
            '<hom_new> <hom_link>': '{escape}{escape}{shift+f}',
            'spectacular': '{ctrl+l}{backspace}',
            '<hom_copy> url': self.copy_url,
            '(<hom_right> | <hom_left>) [<num>]': self.change_tab,
            'left [<num>]': ['{escape}gT', dynamic.Num().add(-1)],
            'close <end>': '{esc}{esc}{ctrl+w}',
            'new tab': '{escape}{ctrl+t}',
            '{}': self.goto_url,
            'top': '{escape}gg',
            'bottom': '{escape}G',
            'refresh': '{F5}',
            '<num>': self.number,
            '<hom_run> <hom_django>': '{esc}{esc}{ctrl+l}http://127.0.0.1:8000/{enter}',
        }

        self.dictionary = {
            'google': 'google.com',
            'news': 'news.google.com',
            'reddit': 'reddit.com',
            'read it': 'reddit.com',
            'red it': 'reddit.com',
            'read': 'reddit.com',
            'something awful': 'forums.somethingawful.com',
            'gmail': 'gmail.com',
            'meet up': 'meetup.com',
            'compose email': 'https://mail.google.com/mail/u/0/#inbox?compose=new',
            'weather': 'weather.gov',
            'local weather': 'http://forecast.weather.gov/MapClick.php?lat=40.8493278056348&lon=-73.93575753168392&site=all&smap=1',
        }

    def copy_url(self, words):
        api.send_string('{escape}{escape}{ctrl+l}')
        time.sleep(.1)
        api.send_string('{ctrl+a}')
        time.sleep(.3)
        api.send_string('{ctrl+c}')
        
    def goto_url(self, words):
        api.send_string('{escape}{escape}{ctrl+l}')
        time.sleep(.1)
        api.send_string('{backspace}' + words[-1] + '{enter}')

    def number(self, words):
        for i, digit in enumerate(words[0]):
            if i != 0:
                time.sleep(.3)
            api.send_string(digit)

    def change_tab(self, words):
        direction = 'gt'
        if words[0] == 'left':
            direction = 'gT'
        num = int(baseutils.set_number(words))
        for i in range(num):
            if i != 0:
                time.sleep(.1)
            api.send_string('{escape}{escape}' + direction)
