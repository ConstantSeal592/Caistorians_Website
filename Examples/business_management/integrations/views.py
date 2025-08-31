from django.shortcuts import render

def xero_integration(request):
    return render(request, 'integrations/xero_integration.html')

def calendar_sync_status(request):
    return render(request, 'integrations/calendar_sync_status.html')

def integration_settings(request):
    return render(request, 'integrations/integration_settings.html')
