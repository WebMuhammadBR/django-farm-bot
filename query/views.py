from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:
        return redirect("farmer_report")
    return redirect("login")


@login_required(login_url="login")
def farmer_report(request):
    return render(request, "query/farmer_report.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("farmer_report")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        remember_me = request.POST.get("remember_me")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)  # 14 kun
            else:
                request.session.set_expiry(0)
            return redirect("farmer_report")

        messages.error(request, "Login yoki parol noto'g'ri. Qayta urinib ko'ring.")

    return render(request, "query/login.html")
