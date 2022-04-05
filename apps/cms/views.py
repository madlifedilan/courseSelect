from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from apps.basefunction.models import VisitNumber, DayNumber, UserIP
from django.core.paginator import Paginator


def cms_dashboard(request):
    context = {}
    context.update(get_dashboard_visitor_ip_table())
    context.update(get_dashboard_top_data())
    return render(request, 'cms/dashboard.html', context=context)


# 获取用户IP表单
def get_dashboard_visitor_ip_table():
    visitor_data = UserIP.objects.filter(day=timezone.now().date())
    total_visit = len(visitor_data)
    if len(visitor_data):
        visitor_data = visitor_data[:7]
    context = {
        'visitor_data_list': visitor_data,
    }
    return context


# 获取4个小卡片的数据
def get_dashboard_top_data():
    day_visit_ip_set = set()
    day_visit_ip_list = UserIP.objects.filter(day=timezone.now().date())
    if day_visit_ip_list:
        for user_ip_item in day_visit_ip_list:
            if user_ip_item.ip_address not in day_visit_ip_set:
                day_visit_ip_set.add(user_ip_item.ip_address)
    day_visit_ip_num = len(day_visit_ip_set)
    day_visit_num = DayNumber.objects.filter(day=timezone.now().date())[0].count
    total_visit_num = VisitNumber.objects.filter(id=1)[0].count
    context = {
        "day_visit_ip_num": day_visit_ip_num,
        "day_visit_num": day_visit_num,
        "total_visit_num": total_visit_num
    }
    return context
