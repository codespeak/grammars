from pynhost import api
from pynhost import constants, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension

class JavascriptGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        'function [<any> <1->]': self.new_function,
        # 'method [<any> <1->]': self.new_method,
        # 'list [<any> <1->]': self.new_list,
        # 'class [<any> <1->]': self.new_class,
        # 'dictionary [<any> <1->]': self.new_dictionary,
        # 'return [is] [<num>]': self.return_value,
        # 'rename': 'rename (function | class)',
        # 'try': 'try:{enter}',
        }
    
        self.context_filters = {
            'language': 'javascript'
        }

    def new_function(self, words):
        if len(words) == 1:
            api.send_string('function () {{{left}{left}{left}{left}')
            return
        func_name = vimutils.create_variable_name(words[1:])
        api.send_string('function {}() '.format(func_name) + '{{{left}{left}{left}')
        vimextension.VimExtensionGrammar.definitions.append('{}_function'.format(func_name))

    # def new_class(self, words):
    #     if len(words) == 1:
    #         api.send_string('class ')
    #         return
    #     class_name = ''.join([word.title() for word in words[1:]])
    #     api.send_string('class {}:'.format(class_name))
    #     vimextension.VimExtensionGrammar.definitions.append('{}_class'.format(class_name))

    # def new_method(self, words):
    #     if len(words) == 1:
    #         api.send_string('def (self):{left}{left}{left}{left}{left}{left}{left}')
    #         return
    #     func_name = baseutils.get_case(words[1:], self.variable_mode)
    #     api.send_string('def {}(self):{{left}}{{left}}'.format(func_name))

    # def new_list(self, words):
    #     if len(words) == 1:
    #         api.send_string(' = []{left}{left}{left}{left}{left}')
    #         return
    #     list_name = vimutils.create_variable_name(words[1:])
    #     api.send_string('{} = []{{left}}'.format(list_name))
    #     vimextension.VimExtensionGrammar.definitions.append('{}_list'.format(list_name))

    # def new_dictionary(self, words):
    #     if len(words) == 1:
    #         api.send_string(' = {{}}{left}{left}{left}{left}{left}')
    #         return
    #     dict_name = vimutils.create_variable_name(words[1:])
    #     api.send_string(dict_name + ' = ' + '{{}}' + '{left}')
    #     vimextension.VimExtensionGrammar.definitions.append('{}_dictionary'.format(dict_name))

    # def rename(self, words):
    #     api.send_string('{{escape}}:call GoToObject("{}"){{enter}}^wciw'.format(words[-1]))

    # def return_value(self, words):
    #     api.send_string('return ')
    #     if words[-1].isdigit():
    #         api.send_string(words[-1])
