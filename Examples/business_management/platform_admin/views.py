from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import ManagerCreationForm, ManagerEditForm
from accounts.models import CustomUser

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def create_manager_view(request):
    if request.method == 'POST':
        form = ManagerCreationForm(request.POST)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.role = 'manager'
            manager.set_password(form.cleaned_data['password1'])
            manager.save()
            return redirect('platform_admin:list_managers')
    else:
        form = ManagerCreationForm()
    return render(request, 'platform_admin/create_manager.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def list_managers_view(request):
    managers = CustomUser.objects.filter(role='manager')
    return render(request, 'platform_admin/list_managers.html', {'managers': managers})

@login_required
@user_passes_test(is_admin)
def edit_manager_view(request, user_id):
    manager = get_object_or_404(CustomUser, id=user_id, role='manager')
    if request.method == 'POST':
        form = ManagerEditForm(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('platform_admin:list_managers')
    else:
        form = ManagerEditForm(instance=manager)
    return render(request, 'platform_admin/edit_manager.html', {'form': form, 'manager': manager})


def is_manager(user):
    return user.role == 'manager'

@user_passes_test(is_manager)
def view_staff(request):
    staff = CustomUser.objects.filter(salon=request.user.salon, role='staff')
    # render staff list template
