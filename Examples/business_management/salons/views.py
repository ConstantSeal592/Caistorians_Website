from django.shortcuts import render, get_object_or_404, redirect
from .models import Salon
from .forms import SalonForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import CustomUser
from .models import Salon
from .forms import SalonForm
from .forms import *
from .models import Service
from .forms import ServiceForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Salon
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.forms import modelformset_factory
from datetime import date
from django.contrib import messages




def salon_list(request):
    return render(request, 'salons/salon_list.html')

def salon_detail(request, pk):
    return render(request, 'salons/salon_detail.html')

def service_list(request, pk):
    salon = get_object_or_404(Salon, pk=pk)
    services = salon.services.all()
    return render(request, 'salons/service_list.html', {
        'salon': salon,
        'services': services
    })

from .forms import ServiceForm

@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)

    # Ensure only the salon’s manager can edit
    if request.user.role != 'manager' or request.user.salon != service.salon:
        return redirect('core:manager_dashboard')

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('salons:service_list', pk=service.salon.pk)
    else:
        form = ServiceForm(instance=service)

    return render(request, 'salons/service_edit.html', {'form': form, 'service': service})

def opening_hours_list(request):
    # You can customize the queryset as needed (e.g., only for current user's salon)
    opening_hours = OpeningHour.objects.all()
    return render(request, 'salons/opening_hours_list.html', {'opening_hours': opening_hours})

@login_required
def service_form(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.salon = salon
            service.save()
            return redirect('salons:service_list', pk=salon.id)
    else:
        form = ServiceForm()

    return render(request, 'salons/service_form.html', {'form': form, 'salon': salon})


def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

@user_passes_test(is_manager)
def staff_list(request):
    staff = CustomUser.objects.filter(salon=request.user.salon, role='staff')
    return render(request, 'salons/staff_list.html', {'staff_list': staff})

@login_required
@user_passes_test(is_manager)
def service_list(request, pk):
    salon = get_object_or_404(Salon, pk=pk)

    if request.user.role != 'manager' or request.user.salon != salon:
        return redirect('core:manager_dashboard')

    services = salon.services.all()
    return render(request, 'salons/service_list.html', {'salon': salon, 'services': services})

from datetime import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import OpeningHourFormSet
from .models import OpeningHour

@login_required
@user_passes_test(is_manager)
def edit_opening_hours(request):
    salon = request.user.salon

    qs = OpeningHour.objects.filter(salon=salon).order_by('day', 'open_time')

    if request.method == 'POST':
        formset = OpeningHourFormSet(request.POST, queryset=qs)
        if formset.is_valid():
            instances = formset.save(commit=False)

            # Ensure all entries belong to this salon
            for instance in instances:
                instance.salon = salon
                instance.save()

            # Handle deletions
            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('salons:opening_hours_list')  # adjust if needed
    else:
        if not OpeningHour.objects.filter(salon=salon).exists():
            for day in range(7):
                OpeningHour.objects.create(salon=salon, day=day, open_time=time(9, 0), close_time=time(17, 0))
        formset = OpeningHourFormSet(queryset=qs)

    return render(request, 'salons/edit_opening_hours.html', {'formset': formset})


@login_required
@user_passes_test(is_manager)
def holiday_edit_view(request, holiday_id):
    salon = request.user.salon
    holiday = get_object_or_404(HolidayOpeningHour, id=holiday_id, salon=salon)
    
    if request.method == 'POST':
        form = HolidayOpeningHourForm(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
            return redirect('salons:holiday_list')
    else:
        form = HolidayOpeningHourForm(instance=holiday)
    
    return render(request, 'salons/holiday_form.html', {'form': form, 'holiday': holiday})

@login_required
@user_passes_test(is_manager)
def holiday_delete_view(request, holiday_id):
    salon = request.user.salon
    holiday = get_object_or_404(HolidayOpeningHour, id=holiday_id, salon=salon)
    
    if request.method == 'POST':
        holiday.delete()
        return redirect('salons:holiday_list')
    
    return render(request, 'salons/holiday_confirm_delete.html', {'holiday': holiday})


@login_required
@user_passes_test(is_manager)
def holiday_list_view(request):
    holidays = HolidayOpeningHour.objects.filter(salon=request.user.salon)
    return render(request, 'salons/holiday_list.html', {'holidays': holidays})

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import HolidayOpeningHour
from .forms import HolidayOpeningHourForm

def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

@login_required
@user_passes_test(is_manager)
def holiday_create_view(request):
    salon = request.user.salon
    if request.method == 'POST':
        form = HolidayOpeningHourForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            if HolidayOpeningHour.objects.filter(salon=salon, date=date).exists():
                messages.error(request, f"A holiday already exists for {date}.")
            else:
                holiday = form.save(commit=False)
                holiday.salon = salon
                holiday.save()
                messages.success(request, "Holiday created successfully.")
                return redirect('salons:holiday_list')
    else:
        form = HolidayOpeningHourForm()

    return render(request, 'salons/holiday_form.html', {'form': form})

def salon_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'newest')

    salons = Salon.objects.all()

    if query:
        salons = salons.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query)
        )

    if sort == 'name_asc':
        salons = salons.order_by('name')
    elif sort == 'name_desc':
        salons = salons.order_by('-name')
    else:  # default to newest
        salons = salons.order_by('-created_at')

    paginator = Paginator(salons, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'salons': page_obj,     # will be used as `salons` in template
        'query': query,
        'sort': sort,
    }
    return render(request, 'salons/salon_list.html', context)



    



def salon_detail(request, pk):
    salon = get_object_or_404(Salon, pk=pk)
    opening_hours = salon.regular_hours.all().order_by('day', 'open_time')
    today = date.today()
    holidays = salon.holiday_hours.filter(date__gte=today).order_by('date')
    
    context = {
        'salon': salon,
        'opening_hours': opening_hours,
        'holidays': holidays,
    }
    return render(request, 'salons/salon_detail.html', context)


def salon_create(request):
    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            salon = form.save(commit=False)
            salon.save()

            # Assign the salon to the logged-in manager
            manager = request.user
            manager.salon = salon
            manager.save()

            # Redirect somewhere, e.g., manager dashboard
            return redirect('accounts:manager_dashboard')
    else:
        form = SalonForm()
    return render(request, 'salons/create_salon.html', {'form': form})


@login_required
def salon_edit(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    # Check if current user is manager of this salon
    if request.user.role != 'manager' or request.user.salon != salon:
        return redirect('accounts:manager_dashboard')  # Or 403 Forbidden page

    if request.method == 'POST':
        form = SalonForm(request.POST, instance=salon)
        if form.is_valid():
            form.save()
            return redirect('accounts:manager_dashboard')
    else:
        form = SalonForm(instance=salon)

    return render(request, 'salons/edit_salon.html', {'form': form, 'salon': salon})


@user_passes_test(is_manager)
def staff_detail(request, staff_id):
    staff_member = get_object_or_404(CustomUser, id=staff_id, salon=request.user.salon, role='staff')
    return render(request, 'salons/staff_detail.html', {'staff': staff_member})


from accounts.models import CustomUser

def assign_salon_view(request, user_id):
    manager = get_object_or_404(CustomUser, id=user_id, role='manager')

    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            salon = form.save()
            manager.salon = salon
            manager.save()
            return redirect('accounts:manager_dashboard')  # Or wherever you want
    else:
        form = SalonForm()

    return render(request, 'salons/assign_salon.html', {
        'form': form,
        'manager': manager
    })




from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Salon

@login_required
def salon_delete(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    # Optional: Restrict deletion to managers who own the salon
    if request.user.role != 'manager' or request.user.salon != salon:
        return redirect('accounts:manager_dashboard')  # or raise 403

    if request.method == 'POST':
        salon.staff_members.all().delete()
        salon.delete()
        return redirect('salons:salon_list') ########################################################################     When money is involved, payout to all staff and owner upon deletion.

    return render(request, 'salons/salon_confirm_delete.html', {'salon': salon})

@login_required
@user_passes_test(is_manager)
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)

    # Ensure only the manager of the salon can delete
    if request.user.role != 'manager' or service.salon != request.user.salon:
        return redirect('core:manager_dashboard')

    if request.method == 'POST':
        service.delete()
        return redirect('salons:service_list', pk=request.user.salon.id)

    return render(request, 'salons/service_confirm_delete.html', {'service': service})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StaffShiftForm
from .models import StaffShift

from datetime import date, timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.timezone import now
from datetime import timedelta
from .forms import StaffShiftForm
from .models import StaffShift, StaffShiftException

@login_required
def manage_shifts(request):
    user = request.user
    today = now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday

    # Fetch all recurring shifts
    shifts = StaffShift.objects.filter(staff=user).order_by('weekday')

    if request.method == 'POST':
        form = StaffShiftForm(request.POST, user=request.user)
        if form.is_valid():
            weekday = form.cleaned_data['weekday']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            repeat = form.cleaned_data.get('repeat', False)

            shift, created = StaffShift.objects.get_or_create(
                staff=user,
                weekday=weekday,
                defaults={
                    'start_time': start_time,
                    'end_time': end_time,
                    'repeat_weekly': repeat,
                }
            )

            if not created:
                shift.start_time = start_time
                shift.end_time = end_time
                shift.repeat_weekly = repeat

            shift.staff = user  # ensure it's set before validation
            shift.full_clean()  # runs clean() to validate against opening hours
            shift.save()

            return redirect('salons:manage_shifts')
    else:
        form = StaffShiftForm(user=request.user)

    # Build next week's schedule based on repeat pattern
    upcoming_schedule = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        weekday = day.weekday()

        # Get recurring shifts for this weekday
        day_shifts = StaffShift.objects.filter(
            staff=user,
            weekday=weekday,
            repeat_weekly=True
        ).exclude(
            staffshiftexception__date=day
        )

        for shift in day_shifts:
            upcoming_schedule.append({
                'date': day,
                'weekday': weekday,
                'start': shift.start_time,
                'end': shift.end_time,
                'shift': shift
            })

    return render(request, 'salons/manage_shifts.html', {
        'shifts': shifts,
        'form': form,
        'upcoming_schedule': upcoming_schedule
    })



@login_required
def skip_shift(request, shift_id, date_str):
    shift = get_object_or_404(StaffShift, id=shift_id, staff=request.user)
    skip_date = date.fromisoformat(date_str)

    # Create an exception
    StaffShiftException.objects.get_or_create(
        shift=shift,
        date=skip_date,
        defaults={'reason': 'User skipped'}
    )
    return redirect('salons:manage_shifts')


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=HolidayOpeningHour)
def remove_conflicting_shifts(sender, instance, **kwargs):
    salon = instance.salon
    holiday_date = instance.date
    day_of_week = holiday_date.weekday()  # 0=Monday

    shifts = StaffShift.objects.filter(
        staff__salon=salon,
        weekday=day_of_week,
        start_time__lt=instance.close_time,
        end_time__gt=instance.open_time,
        repeat_weekly=True
    )

    for shift in shifts:
        StaffShiftException.objects.get_or_create(
            shift=shift,
            date=holiday_date,
            defaults={'reason': 'Holiday conflict'}
        )