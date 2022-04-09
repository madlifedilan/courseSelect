#encoding: utf-8
from django import template
from datetime import datetime
from django.utils.timezone import now as now_func,localtime
register = template.Library()

@register.filter
def datetime_timezone_format(value):
    return "{}年{}月{}日".format(value.year, value.month, value.day)

@register.filter
def calculate_index(value, arg):
    return value + (arg - 1) * 10

@register.filter
def time_format(value):
    if not isinstance(value,datetime):
        return value
    return localtime(value).strftime("%Y/%m/%d %H:%M:%S")

@register.filter
def dashboard_time(value):
    if not isinstance(value,datetime):
        return value
    return localtime(value).strftime("%m-%d")

@register.filter
def add_increase(value, arg):
    return value + arg