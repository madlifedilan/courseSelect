from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
import datetime


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




def get_dashboard_visitor_chart():
    days_list = []
    visit_list = []
    max_num = 0
    week_total_num = 0
    day_visit_num = 0
    for index in range(6, -1, -1):
        day, format_date = get_before_date(index)
        days_list.append(int(day))
        daynumber_item = DayNumber.objects.filter(day=format_date)
        if daynumber_item:
            day_visit_num = daynumber_item[0].count
        visit_list.append(day_visit_num)
        week_total_num += day_visit_num
        max_num = day_visit_num if day_visit_num > max_num else max_num
    context = {
        'visit_week_total_number': day_visit_num,
        'date_time_list': days_list,
        'week_data_list': visit_list,
        'suggested_max': max_num
    }
    return context

def get_before_date(day):
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=-day)
    re_day = (today + offset).strftime("%d")
    re_date = (today + offset).strftime("%Y-%m-%d")
    return re_day, re_date
