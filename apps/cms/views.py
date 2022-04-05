from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from apps.basefunction.models import VisitNumber, DayNumber, UserIP
from django.core.paginator import Paginator




# Create your views here.

def monitor_userip_view(request):
    page = int(request.GET.get('p', 1))
    posts = UserIP.objects.all().order_by('-create_time')
    paginator = Paginator(posts, settings.ONE_PAGE_NEWS_COUNT)
    page_obj = paginator.page(page)
    day_count =DayNumber.objects.filter(day=timezone.now().date())
    ip_count_num = day_count[0].count if day_count else 0

    context = {
        "list_data": page_obj.object_list,
        "day_time": timezone.now().date(),
        "ip_count_num": ip_count_num
    }
    context_data = get_pagination_data(paginator, page_obj)
    context.update(context_data)
    return render(request, 'cms/monitor/userip_manage.html', context=context)

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