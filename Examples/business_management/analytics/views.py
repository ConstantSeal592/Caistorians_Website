from django.shortcuts import render

def analytics_dashboard(request):
    return render(request, 'analytics/analytics_dashboard.html')

def staff_analytics(request):
    return render(request, 'analytics/staff_analytics.html')

def financial_report(request):
    return render(request, 'analytics/financial_report.html')

def service_stats(request):
    return render(request, 'analytics/service_stats.html')
