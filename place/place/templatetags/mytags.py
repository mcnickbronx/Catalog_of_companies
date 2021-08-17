from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def checked(context, name, val):
    get_list = context['request'].GET.getlist(name+"[]")
    if val in get_list:
        return 'checked'
    else:
        return ''


@register.simple_tag(takes_context=True)
def active(context, url_name):
    pattern = url_name
    path = context['request'].path
    if path == '/':
        path = '/home'
    if pattern in path:
        return 'active'
    else:
        return ''
