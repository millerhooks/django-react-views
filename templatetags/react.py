import json as jsonlib

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def json(value):
    uncleaned = jsonlib.dumps(value)
    return mark_safe(uncleaned)


def react_template_tag(context):
    context['react_root_id'] = 'react_root'
    return context


register.inclusion_tag("react/react_root.html", takes_context=True, name="react_root")(react_template_tag)
register.inclusion_tag("react/react_scripts.html", takes_context=True, name="react_scripts")(react_template_tag)
register.inclusion_tag("react/react_full.html", takes_context=True, name="react")(react_template_tag)
