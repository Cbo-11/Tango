from django import template
from rango.models import Catagory

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_catagory_list():
    return {'cats': Catagory.objects.all()}