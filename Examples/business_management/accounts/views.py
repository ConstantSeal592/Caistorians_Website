from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import StaffCreationForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from salons.models import *
from collections import defaultdict
from salons.models import OpeningHour, StaffShift
from .forms import ManagerCreationForm
def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

def is_staff(user):
    return user.is_authenticated and user.role == 'staff'

@login_required
@user_passes_test(lambda u: u.role == 'manager')
def my_staff_view(request):
    staff_and_managers = CustomUser.objects.filter(
        salon=request.user.salon,
        role__in=['staff', 'manager']
    )
    context = {
        'staff_list': staff_and_managers,
    }
    return render(request, 'accounts/my_staff.html', context)

@login_required
@user_passes_test(is_manager)
def create_staff_view(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            staff_user = form.save(commit=False)
            staff_user.role = 'staff'
            staff_user.salon = request.user.salon
            staff_user.set_password(form.cleaned_data['password1'])
            staff_user.save()

            # Optional: send invitation email
            # send_mail(
            #     'You are invited to join the salon team',
            #     f'Hi {staff_user.username},\n\nYou have been added as staff at {request.user.salon.name}. Your temporary password is: {temp_password}\nPlease log in and change your password.',
            #     'no-reply@yourdomain.com',
            #     [staff_user.email],
            #     fail_silently=False,
            # )

            return redirect('accounts:my_staff')
    else:
        form = StaffCreationForm()
    
    return render(request, 'accounts/create_staff.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'client'  # force role to client on registration
            user.save()
            login(request, user)
            return redirect('dashboard')  # adjust this redirect as needed
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'manager':
                return redirect('accounts:manager_dashboard')
            elif user.role == 'staff':
                return redirect('accounts:staff_dashboard')
            else:
                return redirect('accounts:profile')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def profile_view(request):
    return render(request, 'accounts/profile.html')

def edit_profile(request):
    return render(request, 'accounts/edit_profile.html')

def password_change(request):
    return render(request, 'accounts/password_change.html')

@login_required
def staff_dashboard(request):
    user = request.user
    shifts = StaffShift.objects.filter(staff=user).order_by('weekday')

    return render(request, 'accounts/staff_dashboard.html', {
        'shifts': shifts,
    })

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    salon = request.user.salon

    # Get opening hours grouped by day
    opening_hours = OpeningHour.objects.filter(salon=salon).order_by('day', 'open_time')
    day_groups = defaultdict(list)
    for oh in opening_hours:
        day_groups[oh.day].append(oh)

    # Get staff shifts grouped by day
    shifts = StaffShift.objects.filter(staff__salon=salon).order_by('weekday', 'start_time')
    shifts_by_day = defaultdict(list)
    for shift in shifts:
        shifts_by_day[shift.weekday].append(shift)

    # Combine opening hours and shifts into a structure for the template
    week_data = []
    for day in range(7):
        week_data.append({
            'weekday': day,
            'opening_hours': day_groups.get(day, []),
            'shifts': shifts_by_day.get(day, []),
        })
    services = Service.objects.filter(salon=salon)
    context = {
        'salon': salon,
        'week_data': week_data,
        'services': services,
    }
    return render(request, 'accounts/manager_dashboard.html', context)

@user_passes_test(is_manager)
def view_staff(request):
    staff = CustomUser.objects.filter(salon=request.user.salon, role='staff')
    context = {
        'staff_list': staff,
    }
    return render(request, 'accounts/my_staff.html', context)

def create_manager_view(request):
    if request.method == 'POST':
        form = ManagerCreationForm(request.POST)
        if form.is_valid():
            manager_user = form.save(commit=False)
            manager_user.role = 'manager'
            manager_user.salon = None  # No salon yet
            manager_user.set_password(form.cleaned_data['password1'])
            manager_user.save()

            # Log the manager in
            login(request, manager_user)

            # Redirect to salon creation page
            return redirect('salons:assign_salon', user_id=manager_user.id)
    else:
        form = ManagerCreationForm()
    return render(request, 'accounts/create_manager.html', {'form': form})

@login_required
def staff_delete(request, user_id):
    staff_user = get_object_or_404(User, id=user_id, role='staff')

    # Ensure the logged-in user is a manager and manages the same salon
    if request.user.role != 'manager' or staff_user.salon != request.user.salon:
        return HttpResponseForbidden("You are not authorized to delete this staff member.")

    if request.method == 'POST':
        staff_user.delete()
        return redirect('accounts:my_staff')

    return render(request, 'accounts/staff_confirm_delete.html', {'staff_user': staff_user})
