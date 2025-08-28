from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import models

def getdb():
    return models.member.objects.all().values()

def GetWidgets():
    membersdb = getdb()
    context = {
        'membersdb': membersdb,
        'data': {
            'x': 1,
            'y': 5,
            'width': 2,
            'height': 2
        }
    }
    
    html = loader.render_to_string("members_widget.html", context)
    return [{'type': 'string', 'html': html}]

def members(request):
    membersdb = getdb()

    template = loader.get_template("members.html")
    context = {
        'membersdb': membersdb
    }
    return HttpResponse(template.render(context, request))