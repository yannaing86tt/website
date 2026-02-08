from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages


def home(request):
    from .models import Post
    posts = Post.objects.filter(status="published").order_by("-published_at", "-created_at")[:6]
    return render(request, "home.html", {"posts": posts})


def is_staff(user):
    return user.is_authenticated and user.is_staff


def is_superadmin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_staff, login_url="/panel/login/")
def panel_dashboard(request):
    from .models import Post
    from .models_media import MediaItem
    
    # Get statistics
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status="published").count()
    draft_posts = Post.objects.filter(status="draft").count()
    total_media = MediaItem.objects.count()
    
    # Get recent posts
    recent_posts = Post.objects.all().order_by("-updated_at")[:5]
    
    context = {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": draft_posts,
        "total_media": total_media,
        "recent_posts": recent_posts,
    }
    
    return render(request, "panel/dashboard.html", context)


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


# User Management Views (Superadmin only)
@user_passes_test(is_superadmin, login_url="/panel/")
def user_list(request):
    users = User.objects.filter(is_staff=True).order_by("-date_joined")
    return render(request, "panel/users_list.html", {"users": users})


@user_passes_test(is_superadmin, login_url="/panel/")
def user_create(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        role = request.POST.get("role", "staff")
        is_active = request.POST.get("is_active") == "on"
        
        # Validation
        if not username:
            messages.error(request, "Username is required")
            return render(request, "panel/user_form.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "panel/user_form.html")
        
        if password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "panel/user_form.html")
        
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return render(request, "panel/user_form.html")
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_active=is_active
        )
        
        # Set role
        if role == "superadmin":
            user.is_superuser = True
            user.save()
        elif role == "editor":
            editor_group, _ = Group.objects.get_or_create(name="Editor")
            user.groups.add(editor_group)
        
        messages.success(request, f"User {username} created successfully")
        return redirect("/panel/users/")
    
    return render(request, "panel/user_form.html")


@user_passes_test(is_superadmin, login_url="/panel/")
def user_edit(request, user_id):
    try:
        user_obj = User.objects.get(id=user_id, is_staff=True)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect("/panel/users/")
    
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        role = request.POST.get("role", "staff")
        is_active = request.POST.get("is_active") == "on"
        
        # Update user
        user_obj.email = email
        user_obj.is_active = is_active
        
        # Update role
        user_obj.groups.clear()
        if role == "superadmin":
            user_obj.is_superuser = True
        else:
            user_obj.is_superuser = False
            if role == "editor":
                editor_group, _ = Group.objects.get_or_create(name="Editor")
                user_obj.groups.add(editor_group)
        
        user_obj.save()
        
        messages.success(request, f"User {user_obj.username} updated successfully")
        return redirect("/panel/users/")
    
    return render(request, "panel/user_form.html", {"user_obj": user_obj})


@user_passes_test(is_superadmin, login_url="/panel/")
def user_delete(request, user_id):
    try:
        user_obj = User.objects.get(id=user_id, is_staff=True)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect("/panel/users/")
    
    # Prevent deleting yourself
    if user_obj.id == request.user.id:
        messages.error(request, "You cannot delete yourself")
        return redirect("/panel/users/")
    
    if request.method == "POST":
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f"User {username} deleted successfully")
        return redirect("/panel/users/")
    
    return render(request, "panel/user_delete.html", {"user_to_delete": user_obj})
