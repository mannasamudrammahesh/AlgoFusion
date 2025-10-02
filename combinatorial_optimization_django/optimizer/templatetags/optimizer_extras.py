from django import template
import json
import pprint as pp

register = template.Library()

@register.filter
def pprint(value):
    """Pretty print filter for template"""
    return pp.pformat(value, indent=2)