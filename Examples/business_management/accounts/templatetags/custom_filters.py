import calendar
from django import template

register = template.Library()

@register.filter
def get_day_name(day_number):
    try:
        return calendar.day_name[int(day_number)]
    except (ValueError, IndexError, TypeError):
        return ''
