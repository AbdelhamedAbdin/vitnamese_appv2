from django.http import HttpResponseRedirect
import re

lang_seek = re.compile(r'/[a-z-]+/')


def decoratorDirect(func):
    def wrapper(request, *args):
        if request.path == '/' or request.path == lang_seek.match(request.path).group() and request.GET == {}:
            if 'page_number' not in request.GET:
                return HttpResponseRedirect('/?page_number=1')
        return func(request, *args)
    return wrapper


def decoratorDirectError(func):
    def wrapper(request, *args):
        if request.path == str(lang_seek.match(request.path).group()+'error/') and request.GET == {}:
            if 'page_number' not in request.GET:
                return HttpResponseRedirect(str(request.path) + '?page_number=1')
        return func(request, *args)
    return wrapper
