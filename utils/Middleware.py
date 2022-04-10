import time
from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse
from django.core.cache import cache


# 频率限制访问
class IpLimitMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        ip = request.META.get("REMOTE_ADDR")

        # 获取黑名单
        black_list = cache.get('black', [])

        if ip in black_list:
            return HttpResponse("黑名单用户！")

        requests = cache.get(ip, [])

        # 如果值存在，且当前时间 - 最后一个时间 > 30 则清洗掉这个值  这里我们插入请求的时间为头插
        while requests and time.time() - requests[-1] > 30:
            requests.pop()

        # 若没有存在值，则添加，过期时间为30秒，这个过期时间与上面判断的30 保持一致
        requests.insert(0, time.time())
        cache.set(ip, requests, timeout=30)

        # 如果访问次数大于50次，加入黑名单，封2分钟
        if len(requests) > 30:
            black_list.append(ip)
            cache.set('black', black_list, timeout=60 * 2)

        # 限制访问次数为 10 次
        print(len(requests))
        if len(requests) > 10:
            return HttpResponse("请求过于频繁，请稍后重试！")
