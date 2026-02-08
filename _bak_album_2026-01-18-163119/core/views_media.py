from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test

from .models_media import MediaItem
from .forms_media import MediaItemForm

def is_staff(user):
    return user.is_authenticated and user.is_staff

# ===== Panel =====
@user_passes_test(is_staff, login_url="/panel/login/")
def panel_media_list(request):
    items = MediaItem.objects.order_by("-created_at")
    return render(request, "panel/media_list.html", {"items": items})

@user_passes_test(is_staff, login_url="/panel/login/")
@require_http_methods(["GET","POST"])
def panel_media_new(request):
    if request.method == "POST":
        form = MediaItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/panel/media/")
    else:
        form = MediaItemForm()
    return render(request, "panel/media_form.html", {"form": form, "mode": "new"})

@user_passes_test(is_staff, login_url="/panel/login/")
@require_http_methods(["GET","POST"])
def panel_media_edit(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)
    if request.method == "POST":
        form = MediaItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("/panel/media/")
    else:
        form = MediaItemForm(instance=item)
    return render(request, "panel/media_form.html", {"form": form, "mode": "edit", "item": item})

@user_passes_test(is_staff, login_url="/panel/login/")
@require_http_methods(["POST"])
def panel_media_delete(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)
    item.delete()
    return redirect("/panel/media/")

# ===== Public =====
def media_list(request, kind=None):
    qs = MediaItem.objects.filter(status="published").order_by("-published_at","-created_at")
    if kind in ("audio","video"):
        qs = qs.filter(kind=kind)
    return render(request, "media_list.html", {"items": qs, "kind": kind})

def media_detail(request, slug):
    item = get_object_or_404(MediaItem, status="published", slug=slug)
    return render(request, "media_detail.html", {"item": item})
