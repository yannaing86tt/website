from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max

from .models_media import MediaItem, MediaTrack
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
    tracks = item.tracks.all()
    return render(request, "media_detail.html", {"item": item, "tracks": tracks})


@user_passes_test(is_staff, login_url="/panel/login/")
@require_http_methods(["GET","POST"])
def panel_media_tracks(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip() or "Track"
        order_raw = (request.POST.get("order") or "").strip()
        audio = request.FILES.get("audio_file")

        if order_raw.isdigit():
            order = int(order_raw)
        else:
            last = item.tracks.aggregate(m=Max("order"))["m"] or 0
            order = last + 1

        if audio:
            MediaTrack.objects.create(item=item, title=title, order=order, audio_file=audio)
            return redirect("panel_media_tracks", pk=item.pk)

    tracks = item.tracks.all()
    return render(request, "panel/media_tracks.html", {"item": item, "tracks": tracks})


@user_passes_test(is_staff, login_url="/panel/login/")
@require_http_methods(["POST"])
def panel_media_track_delete(request, pk):
    t = get_object_or_404(MediaTrack, pk=pk)
    item_pk = t.item_id
    t.delete()
    return redirect("panel_media_tracks", pk=item_pk)
