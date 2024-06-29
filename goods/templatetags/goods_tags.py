from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re
from django import template
from django.utils.http import urlencode


from carts.models import Cart
from goods.models import Categories


register = template.Library()

@register.simple_tag()
def tag_categories():
    return Categories.objects.all()

@register.simple_tag(takes_context=True) #все контестные переменные доступны(context из контролера)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.filter(name='highlight')
@stringfilter
def highlight(text, words):
    words = words.split()
    for word in words:
        text = re.sub(r'(%s)' % re.escape(word), r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return mark_safe(text)

