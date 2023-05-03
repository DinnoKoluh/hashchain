from django import template

register = template.Library()
# custom template tag for going through two lists in html
# https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/
@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

@register.filter
def subtract(value, arg):
    return value - arg