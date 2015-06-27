from pynhost import api
from pynhost import constants, dynamic
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils, extension
from pynhost.grammars.vimtastic.python import pyextension

class PyCommandsGrammar(pyextension.PyVimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['filtered words'].remove('is')
        self.mapping = {
        '<hom_function> <any> <0->': self.new_function,
        'method [<any> <1->]': self.new_method,
        'class [<any> <1->]': self.new_class,
        'return [is] [<num>]': self.return_value,
        'try': 'try:{enter}',
        'swamp <any>': self.double_underscore,
        'lower': 'lower()',
        '(is instance)': vimutils.FUNCTIONS['SmartSpace'] + 'isinstance(){left}',
        '<hom_enumerate>': vimutils.FUNCTIONS['SmartSpace'] + 'enumerate(){left}',
        '<hom_none>': vimutils.FUNCTIONS['SmartSpace'] + 'None',
        '<hom_true>': [vimutils.FUNCTIONS['SmartSpace'] + 'True'],
        '<hom_false>': [vimutils.FUNCTIONS['SmartSpace'] + 'False'],
        '<hom_in>': '{}in{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        '<hom_and>': '{}and{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        '<hom_or>': '{}or{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        '<hom_is>': '{}is{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        '<hom_import>': '{}import{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        '<hom_quad>': '{}for{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        '<hom_if>': '{}if{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        '<hom_from>': 'from{}'.format(vimutils.FUNCTIONS['EndSpace']),
        '<hom_except>': 'except' + vimutils.FUNCTIONS['EndSpace'],
        '<hom_yield>': 'yield' + vimutils.FUNCTIONS['EndSpace'],
        '<hom_length>': 'len(){left}',
        '<hom_constructor>': 'def __init__(self):{left}{left}',
        '<hom_self>': 'self',
        '<hom_not>': '{}not{}'.format(vimutils.FUNCTIONS['SmartSpace'], vimutils.FUNCTIONS['EndSpace']),
        '<hom_cast> (<hom_string>)': self.cast,
        'range [<num> [<hom_halt> [<num> [<hom_halt> [<num>]]]]]': self.range,
        '(<hom_grab> | <hom_copy> | <hom_kill> | <hom_select>) (<hom_function> | <hom_class>)': self.modify_func_class,
        '<hom_rename> <hom_function>': '{esc}' + vimutils.FUNCTIONS['GoToFunction']  + '^wciw',
        '<hom_dock> <hom_string>': "'''{enter}{enter}'''{up}{tab}",
        }
    
    def _load_grammar(self):
        return extension.current_language in ['python3', 'python2']

    def new_function(self, words):
        if len(words) == 1:
            api.send_string('def ():{left}{left}{left}')
            return
        func_name = vimutils.guess_at_text(words[1:])
        api.send_string('def {}():{{left}}{{left}}'.format(func_name))
        vimextension.VimExtensionGrammar.definitions.append('{}_function'.format(func_name))

    def new_class(self, words):
        if len(words) == 1:
            api.send_string('class ')
            return
        class_name = ''.join([word.title() for word in words[1:]])
        api.send_string('class {}:'.format(class_name))
        vimextension.VimExtensionGrammar.definitions.append('{}_class'.format(class_name))

    def new_method(self, words):
        if len(words) == 1:
            api.send_string('def (self):{left}{left}{left}{left}{left}{left}{left}')
            return
        func_name = baseutils.get_case(words[1:], self.variable_mode)
        api.send_string('def {}(self):{{left}}{{left}}'.format(func_name))

    def new_list(self, words):
        if len(words) == 1:
            api.send_string(' = []{left}{left}{left}{left}{left}')
            return
        list_name = vimutils.create_variable_name(words[1:])
        api.send_string('{} = []{{left}}'.format(list_name))
        vimextension.VimExtensionGrammar.definitions.append('{}_list'.format(list_name))

    def new_dictionary(self, words):
        if len(words) == 1:
            api.send_string(' = {{}}{left}{left}{left}{left}{left}')
            return
        dict_name = vimutils.create_variable_name(words[1:])
        api.send_string(dict_name + ' = ' + '{{}}' + '{left}')
        vimextension.VimExtensionGrammar.definitions.append('{}_dictionary'.format(dict_name))

    def rename(self, words):
        api.send_string('{{escape}}:call GoToObject("{}"){{enter}}^wciw'.format(words[-1]))

    def return_value(self, words):
        api.send_string('return ')
        if words[-1].isdigit():
            api.send_string(words[-1])

    def double_underscore(self, words):
        api.send_string('__{}__'.format(words[-1]))

    def cast(self, words):
        cast_map = {
            'string': 'str',
        }
        api.send_string(cast_map[words[-1]] + '(){left}')

    def range(self, words):
        text = 'range(){left}'
        if len(words) > 1:
            text += words[1]
        if len(words) > 2:
            text += ', '
        if len(words) > 3:
            text += words[3]
        if len(words) > 4:
            text += ', '
        if len(words) > 5:
            text += words[5]
        if len(words) % 2 == 0:
            text += '{right}'
        api.send_string(text)

    def modify_func_class(self, words):
        text = '{esc}'
        if words[-1] == 'function':
            text += vimutils.FUNCTIONS['GoToFunction']
        else:
            text += vimutils.FUNCTIONS['GoToClass']
        text += 'V' + vimutils.FUNCTIONS['SelectIndent']
        if words[0] == 'copy':
            text += 'ya'
        else:
            text += vimutils.commands[words[0]]
        api.send_string(text)
