from django.conf import settings

def site_settings(request):
    """Add site settings to all templates"""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'FOOTER_NAME': settings.FOOTER_NAME,
        'TELEGRAM_URL': settings.TELEGRAM_URL,
        'FACEBOOK_URL': settings.FACEBOOK_URL,
    }
