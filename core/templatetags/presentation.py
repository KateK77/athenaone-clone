from django import template
from core.presentation import money, readable

register = template.Library()
register.filter('money', money)
register.filter('readable', readable)
