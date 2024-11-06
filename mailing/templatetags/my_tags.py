from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.simple_tag()
def manager_groups():
    return Group.objects.get(name='manager')


@register.simple_tag()
def user_groups():
    return Group.objects.get(name='user')


@register.simple_tag()
def day():
    return 'day'
