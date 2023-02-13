from django import template

register = template.Library()


@register.filter
def my_filter(v1, v2):
    return v1 * v2


@register.simple_tag
def my_tag1(v1, v2, v3):
    return v1 * v2 * v3

