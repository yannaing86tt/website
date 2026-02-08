from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages


def register_view(request):
    """Public user registration - no email verification"""
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        
        # Validation
        if not username:
            messages.error(request, "Username is required")
            return render(request, "register.html")
        
        if len(username) < 3:
            messages.error(request, "Username must be at least 3 characters")
            return render(request, "register.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "register.html")
        
        if not password:
            messages.error(request, "Password is required")
            return render(request, "register.html")
        
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return render(request, "register.html")
        
        if password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")
        
        # Create user (is_staff=False for public users)
        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=False,
            is_active=True
        )
        
        # Auto-login after registration
        login(request, user)
        messages.success(request, f"Welcome {username}! Your account has been created.")
        return redirect("/")
    
    return render(request, "register.html")


def login_view(request):
    """Public user login"""
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to next parameter or home
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")


def logout_view(request):
    """Public user logout"""
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("/")
