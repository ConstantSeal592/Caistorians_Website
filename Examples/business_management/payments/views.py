from django.shortcuts import render

def payment_form(request):
    return render(request, 'payments/payment_form.html')

def payment_success(request):
    return render(request, 'payments/payment_success.html')

def payment_history(request):
    return render(request, 'payments/payment_history.html')

def refund_policy(request):
    return render(request, 'payments/refund_policy.html')
