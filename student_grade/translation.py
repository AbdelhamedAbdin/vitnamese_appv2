from modeltranslation.translator import translator, TranslationOptions
from .models import *


class StudentTranslationOptions(TranslationOptions):
    fields = ('gender',)


class CharacterTranslationOptions(TranslationOptions):
    fields = ('character', 'regularity', 'complexity')


class ResponseTranslationOptions(TranslationOptions):
    fields = ('error_type', 'error_number', 'error_class', 'error_unit')
    related = True
    related_fields = ['student', 'character']


translator.register(Student, StudentTranslationOptions)
translator.register(Character, CharacterTranslationOptions)
translator.register(Response, ResponseTranslationOptions)
