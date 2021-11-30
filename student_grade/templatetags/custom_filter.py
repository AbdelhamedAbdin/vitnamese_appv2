from django import template
from django.utils import translation
import pandas as pd

register = template.Library()


@register.filter
def gender(value, arg):
    current_lang = translation.get_language().replace("-", "_")
    # print(pd.DataFrame(value.filter(error_number=arg).exclude(error_number__isnull=True).values_list('student__gender_'+current_lang, 'id', 'image')))
    return value.filter(error_number=arg).exclude(error_number__isnull=True).values_list('student__gender_'+current_lang, 'id', 'image')


@register.filter
def grade(value, arg):
    return value.filter(error_number=arg).exclude(error_number__isnull=True).values_list('student__grade', 'id', 'image')


@register.filter
def regular(value, arg):
    current_lang = translation.get_language().replace("-", "_")
    return value.filter(error_number=arg).exclude(error_number__isnull=True).values_list('character__regularity_'+current_lang, 'id', 'image')


@register.filter
def complex(value, arg):
    current_lang = translation.get_language().replace("-", "_")
    return value.filter(error_number=arg).exclude(error_number__isnull=True).values_list('character__complexity_'+current_lang, 'id', 'image')


# control tapping activation
@register.filter
def splitter(value, arg):
    obj = value.split(arg)
    return list(filter(None, obj))
