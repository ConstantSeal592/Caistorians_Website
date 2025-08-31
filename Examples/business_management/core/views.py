from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def terms(request):
    return render(request, 'core/terms.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def privacy(request):
    return render(request, 'core/privacy.html')

@login_required
def dashboard(request):
    role = request.user.role
    return render(request, f'core/{role}_dashboard.html')