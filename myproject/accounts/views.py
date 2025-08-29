from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, LoginForm

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/accounts/profile/")  # the actual path

    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


from django.views.decorators.http import require_POST
@require_POST
def logout_view(request):
    logout(request)
    return render(request, "accounts/index.html")



def index_view(request):
    return render(request, "accounts/index.html")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def billing_setup_view(request):
    if request.method == "POST":
        # Grab form data
        card_number = request.POST.get("card_number")
        expiry = request.POST.get("expiry")
        cvv = request.POST.get("cvv")
        address = request.POST.get("address")

        # For now, just print to console or save in DB model later
        print("Billing Info:", card_number, expiry, cvv, address)

        # Redirect back to profile after saving
        return redirect("profile")

    return render(request, "accounts/billing_setup.html")



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def profile_view(request):
    user = request.user
    today = timezone.now().date()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")

        if password and password == confirm_password:
            user.set_password(password)

        user.email = email
        user.phone = phone
        user.dob = dob
        user.save()
        return redirect("profile")

    return render(request, "accounts/profile.html", {"today": today})



def GetWidgets():
    return [{'type': 'file', 'file': 'widgets/account_widget.html', 'parameters': {'width':1, 'height':1}}]