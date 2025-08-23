from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import models

def members(request):
    membersdb = models.member.objects.all().values()

    template = loader.get_template("members,html")
    context = {
        'membersdb': membersdb
    }
    return HttpResponse(template.render(context, request))