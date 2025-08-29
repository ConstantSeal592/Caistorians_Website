from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

MyWidgets = [
    {'type': 'file', 'file': 'widgets/magazine_widget.html', 'parameters': {'width':4, 'height':2}},    ##Wants moving to the magazines app
    {'type': 'file', 'file': 'widgets/aims_widget.html', 'parameters': {'width':2, 'height':2}},
    {'type': 'file', 'file': 'widgets/contact_widget.html', 'parameters': {'width':2, 'height':2}},
    {'type': 'file', 'file': 'widgets/image_widget.html', 'parameters': {'width':2, 'height':2, 'static_img_path': 'frontend/logo.png'}},        ##Wants to become a general purpose img widget
]

def GetWidgets():
    return MyWidgets

from members import views as memViews
from accounts import views as accViews
WidgetProviders = [
    GetWidgets,
    memViews.GetWidgets,
    accViews.GetWidgets
]

def index(request):
    AllWidgets = []
    for provider in WidgetProviders:
        AllWidgets += provider()

    template = loader.get_template("frontend/index.html")
    context = {
        'widgets': AllWidgets
    }
    return HttpResponse(template.render(context, request))