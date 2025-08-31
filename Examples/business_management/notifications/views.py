from django.shortcuts import render

def notification_settings(request):
    return render(request, 'notifications/notification_settings.html')

def email_preview(request):
    return render(request, 'notifications/email_preview.html')
