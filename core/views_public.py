from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown as md
import bleach

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS.union({
    "p", "div", "span", "pre", "code",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li",
    "blockquote",
    "br", "hr",
    "table", "thead", "tbody", "tr", "th", "td",
    "a",
    "input",
})
ALLOWED_ATTRS = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "a": ["href", "title", "rel", "target"],
    "div": ["class"],
    "span": ["class"],
    "p": ["class"],
    "ul": ["class"],
    "ol": ["class"],
    "li": ["class"],
    "pre": ["class"],
    "code": ["class"],
    "input": ["type", "checked", "disabled", "class"],
    "h1": ["id"], "h2": ["id"], "h3": ["id"], "h4": ["id"], "h5": ["id"], "h6": ["id"],
    "th": ["colspan", "rowspan"],
    "td": ["colspan", "rowspan"],
}
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

@login_required(login_url="/login/")
def posts_list(request):
    posts = Post.objects.filter(status="published").order_by("-published_at", "-created_at")
    return render(request, "posts_list.html", {"posts": posts})

@login_required(login_url="/login/")
def post_detail(request, slug):
    post = get_object_or_404(Post, status="published", slug=slug)
    html = md.markdown(
        post.content or "",
        extensions=[
            "fenced_code", "tables", "nl2br",
            "codehilite",
            "admonition",
            "attr_list",
            "md_in_html",
            "pymdownx.tasklist",
        ],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "codehilite"},
            "pymdownx.tasklist": {"custom_checkbox": True, "clickable_checkbox": False},
        },
    )
    safe_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    return render(request, "post_detail.html", {"post": post, "content_html": safe_html})
