from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
import markdown as md
import bleach


def is_staff(user):
    return user.is_authenticated and user.is_staff


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


@csrf_exempt
@require_POST
@user_passes_test(is_staff, login_url="/panel/login/")
def md_preview(request):
    text = request.POST.get("text", "") or ""
    html = md.markdown(
        text,
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
    return JsonResponse({"html": safe_html})
