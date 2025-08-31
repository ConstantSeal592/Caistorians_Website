from django.shortcuts import render

def settings_form(request):
    return render(request, 'settings_manager/settings_form.html')

def working_hours_form(request):
    return render(request, 'settings_manager/working_hours_form.html')

def tax_settings(request):
    return render(request, 'settings_manager/tax_settings.html')
