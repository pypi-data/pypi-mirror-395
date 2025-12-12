from django import template

register = template.Library()


@register.inclusion_tag("shared/icon.html", takes_context=False)
def icon(name, **kwargs):
    kwargs["name"] = name
    return kwargs
