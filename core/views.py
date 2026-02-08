from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect


def home(request):
    from .models import Post
    posts = Post.objects.filter(status="published").order_by("-published_at", "-created_at")[:6]
    return render(request, "home.html", {"posts": posts})
def is_staff(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff, login_url="/panel/login/")
def panel_dashboard(request):
    return render(request, "panel/dashboard.html")


def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("/panel/")

    error = ""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect("/panel/")
        error = "Login မအောင်မြင်ပါ။ (staff user ဖြစ်ရမယ်)"

    return render(request, "panel/login.html", {"error": error})


def panel_logout(request):
    logout(request)
    return redirect("/panel/login/")
