from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import messages

from .models import Post


def is_staff(user):
    return user.is_authenticated and user.is_staff


def can_delete_posts(user):
    """Only superadmins can delete posts"""
    return user.is_authenticated and user.is_superuser


def make_slug(raw: str) -> str:
    raw = (raw or "").strip()
    # allow unicode, replace spaces with hyphen, remove weird chars
    s = slugify(raw, allow_unicode=True)
    return s or raw.replace(" ", "-")


@user_passes_test(is_staff, login_url="/panel/login/")
def post_list(request):
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    posts = Post.objects.all()
    if q:
        posts = posts.filter(title__icontains=q)
    if status in ("draft", "published"):
        posts = posts.filter(status=status)

    return render(request, "panel/posts_list.html", {
        "posts": posts, 
        "q": q, 
        "status": status,
        "can_delete": can_delete_posts(request.user)
    })


@user_passes_test(is_staff, login_url="/panel/login/")
def post_create(request):
    error = ""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        slug = request.POST.get("slug", "").strip()
        content = request.POST.get("content", "")
        status = request.POST.get("status", "draft")
        video_url = request.POST.get("video_url", "").strip()
        cover_image = request.FILES.get("cover_image")

        if not title:
            error = "Title မဖြစ်မနေလိုပါတယ်"
        else:
            if not slug:
                slug = make_slug(title)
            else:
                slug = make_slug(slug)

            # slug unique check
            if Post.objects.filter(slug=slug).exists():
                error = "Slug တူနေပါတယ် (တစ်ခုထဲပဲရှိရမယ်) — slug ကိုပြောင်းပါ"

        if not error:
            Post.objects.create(
                title=title,
                slug=slug,
                content=content,
                status=status,
                video_url=video_url,
                cover_image=cover_image,
                author=request.user,
                published_at=timezone.now() if status == "published" else None,
            )
            messages.success(request, f"Post '{title}' created successfully!")
            return redirect("/panel/posts/")

    return render(request, "panel/post_form.html", {"mode": "create", "post": None, "error": error})


@user_passes_test(is_staff, login_url="/panel/login/")
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    error = ""

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        slug = request.POST.get("slug", "").strip()
        post.content = request.POST.get("content", "")
        post.status = request.POST.get("status", "draft")
        post.video_url = request.POST.get("video_url", "").strip()

        if not title:
            error = "Title မဖြစ်မနေလိုပါတယ်"
        else:
            post.title = title
            new_slug = make_slug(slug or title)
            if Post.objects.exclude(id=post.id).filter(slug=new_slug).exists():
                error = "Slug တူနေပါတယ် — slug ကိုပြောင်းပါ"
            else:
                post.slug = new_slug

        cover_image = request.FILES.get("cover_image")
        if cover_image:
            post.cover_image = cover_image

        if not error:
            if post.status == "published" and post.published_at is None:
                post.published_at = timezone.now()
            if post.status == "draft":
                post.published_at = None

            post.save()
            messages.success(request, f"Post '{post.title}' updated successfully!")
            return redirect("/panel/posts/")

    return render(request, "panel/post_form.html", {"mode": "edit", "post": post, "error": error})


@user_passes_test(can_delete_posts, login_url="/panel/")
def post_delete(request, post_id):
    """Only superadmins can delete posts"""
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        title = post.title
        post.delete()
        messages.success(request, f"Post '{title}' deleted successfully!")
        return redirect("/panel/posts/")

    return render(request, "panel/post_delete.html", {"post": post})
