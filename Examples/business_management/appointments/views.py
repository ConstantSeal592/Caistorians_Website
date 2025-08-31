from django.shortcuts import render

def booking_form(request):
    return render(request, 'appointments/booking_form.html')

def booking_confirm(request):
    return render(request, 'appointments/booking_confirm.html')

def booking_success(request):
    return render(request, 'appointments/booking_success.html')

def my_appointments(request):
    return render(request, 'appointments/my_appointments.html')

def appointment_detail(request, id):
    return render(request, 'appointments/appointment_detail.html')

def queue_status(request):
    return render(request, 'appointments/queue_status.html')
