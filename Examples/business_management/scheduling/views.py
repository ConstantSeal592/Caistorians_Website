from django.shortcuts import render

def staff_calendar(request):
    return render(request, 'scheduling/staff_calendar.html')

def shift_form(request):
    return render(request, 'scheduling/shift_form.html')

def leave_request(request):
    return render(request, 'scheduling/leave_request.html')

def leave_list(request):
    return render(request, 'scheduling/leave_list.html')
