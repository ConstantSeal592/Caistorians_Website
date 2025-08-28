from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

MyWidgets = [
    {'type': 'file', 'file': 'magazine_widget.html', 'parameters': {'width':4, 'height':2}},    ##Wants moving to the magazines app
    {'type': 'file', 'file': 'aims_widget.html', 'parameters': {'width':2, 'height':2}},
    {'type': 'file', 'file': 'contact_widget.html', 'parameters': {'width':2, 'height':2}},
    {'type': 'file', 'file': 'image_widget.html', 'parameters': {'width':2, 'height':2, 'static_img_path': 'frontend/logo.png'}},        ##Wants to become a general purpose img widget
]

def GetWidgets():
    return MyWidgets

from members import views as memViews
WidgetProviders = [
    GetWidgets,
    memViews.GetWidgets
]

def index(request):
    AllWidgets = []
    for provider in WidgetProviders:
        AllWidgets += provider()

    template = loader.get_template("index.html")
    context = {
        'widgets': AllWidgets
    }
    return HttpResponse(template.render(context, request))