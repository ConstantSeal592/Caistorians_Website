from django.shortcuts import render

def campaign_list(request):
    return render(request, 'marketing/campaign_list.html')

def campaign_form(request):
    return render(request, 'marketing/campaign_form.html')

def loyalty_dashboard(request):
    return render(request, 'marketing/loyalty_dashboard.html')

def promotion_form(request):
    return render(request, 'marketing/promotion_form.html')
