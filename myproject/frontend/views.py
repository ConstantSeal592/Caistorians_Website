from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from members.models import member

# Create your views here.
def index(request):
    membersdb = member.objects.all().values()

    template = loader.get_template("index.html")
    context = {
        'membersdb': membersdb
    }
    return HttpResponse(template.render(context, request))

    return render(request, 'index.html')