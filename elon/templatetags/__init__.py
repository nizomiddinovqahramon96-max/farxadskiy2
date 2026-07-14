from django import template
from ..models import Like

register = template.Library()

@register.filter
def has_liked(user, elon):
    if not user.is_authenticated:
        return False
    return Like.objects.filter(user=user, elon=elon).exists()
