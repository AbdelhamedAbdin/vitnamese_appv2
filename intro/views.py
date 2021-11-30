from django.shortcuts import render
from django.http import HttpResponse


def intro(request):
    return render(request, 'intro/intro.html', {'i': 'Introduction section'})
