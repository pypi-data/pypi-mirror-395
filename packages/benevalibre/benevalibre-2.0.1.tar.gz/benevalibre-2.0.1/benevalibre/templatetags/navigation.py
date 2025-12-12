from django import template
from django.utils.module_loading import import_string

register = template.Library()


@register.simple_tag(takes_context=True)
def menu_items(context, menu_path, obj=None):
    menu = import_string("benevalibre.%s" % menu_path)
    return menu.get_items_for_request(context["request"], obj)


@register.inclusion_tag("shared/pagination.html")
def pagination(paginator, page):
    return {
        "page": page,
        "paginator": paginator,
        "elided_page_range": paginator.get_elided_page_range(page.number),
    }
