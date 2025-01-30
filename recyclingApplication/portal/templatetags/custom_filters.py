from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter
def urlencode_without_page(query_string):
    # Removes duplicate 'page' parameters from the query string.
    params = query_string.split("&")
    filtered_params = [p for p in params if not p.startswith("page=")]
    return "&".join(filtered_params)