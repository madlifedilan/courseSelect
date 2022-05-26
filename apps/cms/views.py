from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
import datetime

from apps.basefunction.models import VisitNumber, DayNumber, UserIP
from django.core.paginator import Paginator


def cms_dashboard(request):
    context = {}
    context.update(get_dashboard_visitor_ip_table())
    context.update(get_dashboard_top_data())
    context.update(get_dashboard_visitor_chart())
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
    for index in range(6, -1, -1):
        day, format_date = get_before_date(index)
        days_list.append(int(day))
        daynumber_item = DayNumber.objects.filter(day=format_date)
        day_visit_num = 0
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


def monitor_userip_view(request):
    page = int(request.GET.get('p', 1))
    posts = UserIP.objects.all().order_by('-day')
    paginator = Paginator(posts, settings.ONE_PAGE_NEWS_COUNT)
    page_obj = paginator.page(page)
    day_count = DayNumber.objects.filter(day=timezone.now().date())
    ip_count_num = day_count[0].count if day_count else 0

    context = {
        "list_data": page_obj.object_list,
        "day_time": timezone.now().date(),
        "ip_count_num": ip_count_num
    }
    context_data = get_pagination_data(paginator, page_obj)
    context.update(context_data)
    return render(request, 'cms/userip.html', context=context)


def get_pagination_data(paginator, page_obj, around_count=2):
    current_page = page_obj.number
    num_pages = paginator.num_pages

    left_has_more = False
    right_has_more = False

    if current_page <= around_count + settings.ONE_PAGE_NEWS_COUNT:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)

    if current_page >= num_pages - around_count - 1:
        right_pages = range(current_page + 1, num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + around_count + 1)

    return {
        # left_pages：代表的是当前这页的左边的页的页码
        'left_pages': left_pages,
        # right_pages：代表的是当前这页的右边的页的页码
        'right_pages': right_pages,
        'current_page': current_page,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'num_pages': num_pages
    }


def ViewUser(request):
    banUserList = cache.get('black', [])
    context = {
        'banUserList': banUserList
    }
    return render(request, 'cms/ViewUser.html', context=context)
