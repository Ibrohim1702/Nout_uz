from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from dashboard.models import User


def index(requests):
    user = requests.user
    if user.is_anonymous:
        return redirect("dashboard_login")
    ctx = {
        "user": user,
        "home": True
    }
    return render(requests, 'dashboard/base.html', ctx)


def register(requests):
    if requests.POST:
        password = requests.POST.get('pass')
        password_conf = requests.POST.get('pass_conf')
        username = requests.POST.get('username')
        name = requests.POST.get('name')
        phone = requests.POST.get('phone')

        if password_conf != password:
            return redirect("dashboard_register")

        user = User()
        user.user_name = username
        user.name = name
        user.phone = phone
        user.set_password(password)
        user.save()

        user = authenticate(requests, user_name=username, password=password)
        login(requests, user)
        return redirect("dashboard_home")

    return render(requests, 'dashboard/register.html')


def dashboard_login(requests):
    if requests.POST:
        password = requests.POST.get('pass')
        username = requests.POST.get('username')

        user = User.objects.filter(user_name=username).first()
        if not user:
            raise ValueError("User not found")

        if user.check_password(password):
            user = authenticate(requests, user_name=username, password=password)
            login(requests, user)
            return redirect("dashboard_home")
        else:
            raise ValueError("Password error")
    return render(requests, 'dashboard/login.html')


def dashboard_logout(requests):
    user = requests.user
    if user.is_anonymous:
        return redirect("dashboard_login")
    logout(requests)
    return redirect('dashboard_login')
