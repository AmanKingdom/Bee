from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

def homepage(request):
    template = get_template('users-window/index.html')
    html = template.render(locals())
    return HttpResponse(html)

def search(request):
    try:
        search_text = request.GET['search-text']
        print(search_text)
    except:
        search_text = None
    if search_text == "search-result/?search-text=":
        template = get_template('users-window/index.html')
    else:
        template = get_template('users-window/search-result.html')
    html = template.render(locals())
    return HttpResponse(html)
