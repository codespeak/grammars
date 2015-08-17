from pynhost import api
from pynhost import dynamic
from pynhost.grammars import baseutils, extension
from pynhost.grammars.web.django import djangoextension

class DjangoTemplateGrammar(djangoextension.DjangoExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            '<hom_new> <hom_model>': 'class (models.Model):' + '{left}' * 15,
            '<hom_foreign key>': 'models.ForeignKey(){left}',
            '<hom_character> <hom_field>': 'models.CharField(){left}',
            '(121|one to one|one-to-one|1 to 1) field': 'models.OneToOneField(){left}',
            '<hom_import> <hom_models>': 'from django.db import models',
            '<hom_import> <hom_user>': 'from django.contrib.auth.models import User',
            '<hom_import> <hom_render>': 'from django.shortcuts import render',
            '<hom_integer> <hom_field>': 'models.IntegerField(){left}',
        }
        self.settings['priority'] = 6
