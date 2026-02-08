from django import template

register = template.Library()

@register.filter
def is_in_group(user, group_name):
    """Check if user is in a specific group"""
    return user.groups.filter(name=group_name).exists()

@register.filter
def has_editor_role(user):
    """Check if user has Editor role"""
    return user.groups.filter(name="Editor").exists()
