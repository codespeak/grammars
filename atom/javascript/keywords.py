from pynhost.grammars.atom import atomextension, atomutils
from pynhost.grammars.atom.javascript import jsextension

class JavascriptKeywordsGrammar(jsextension.JsExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.settings['filtered words'] = []
        self.settings['priority'] = 5
        self.mapping = {
            '<hom_quad>': 'for' + atomutils.OTHER['endConditionalSpace'],
            '<hom_in>': atomutils.OTHER['beginningConditionalSpace'] + 'in' + atomutils.OTHER['endConditionalSpace'],
            '<hom_and>': atomutils.OTHER['beginningConditionalSpace'] + '&&' + atomutils.OTHER['endConditionalSpace'],
            '<hom_assert>': 'assert' + atomutils.OTHER['endConditionalSpace'],
            '<hom_break>': 'break{enter}',
            '<hom_return>': 'return{}'.format(atomutils.OTHER['endConditionalSpace']),
            '<hom_continue>': 'continue{enter}',
            '<hom_as>': atomutils.OTHER['beginningConditionalSpace'] + 'as' + atomutils.OTHER['endConditionalSpace'],
            '<hom_far>': atomutils.OTHER['beginningConditionalSpace'] + 'var' + atomutils.OTHER['endConditionalSpace'],
            '<hom_try>': 'try:{enter}',
            '<hom_not>': atomutils.OTHER['beginningConditionalSpace'] + 'not' + atomutils.OTHER['endConditionalSpace'],
            '<hom_or>': atomutils.OTHER['beginningConditionalSpace'] + '||' + atomutils.OTHER['endConditionalSpace'],
            '<hom_is>': atomutils.OTHER['beginningConditionalSpace'] + 'is' + atomutils.OTHER['endConditionalSpace'],
            '<hom_none>': 'None',
            '<hom_false>': 'false',
            '<hom_true>': 'true',
            '<hom_if>': atomutils.OTHER['beginningConditionalSpace'] + 'if' + atomutils.OTHER['endConditionalSpace'],
            '<hom_with>': atomutils.OTHER['beginningConditionalSpace'] + 'with' + atomutils.OTHER['endConditionalSpace'],
            '<hom_else>': atomutils.OTHER['beginningConditionalSpace'] + 'else',
            '<hom_from>': atomutils.OTHER['beginningConditionalSpace'] + 'from' + atomutils.OTHER['endConditionalSpace'],
            '<hom_raise>': atomutils.OTHER['beginningConditionalSpace'] + 'raise' + atomutils.OTHER['endConditionalSpace'],
            '<hom_except>': atomutils.OTHER['beginningConditionalSpace'] + 'except' + atomutils.OTHER['endConditionalSpace'],
            '<hom_index> <hom_error>': atomutils.OTHER['beginningConditionalSpace'] + 'IndexError',
            '(<hom_runtime> | <hom_run> <hom_time>) <hom_error>': atomutils.OTHER['beginningConditionalSpace'] + 'RuntimeError',
            '<hom_pop>': 'pop',
            '<hom_cast> <hom_integer>': 'parseInt(){left}',
            '<hom_cast> <hom_string>': 'parseStr(){left}',
            '<hom_strip>': 'strip',
        }
