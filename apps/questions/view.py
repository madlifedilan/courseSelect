from django.http import HttpResponse
from django.shortcuts import render
from time import time

# Create your views here.

ips = [None]
last = 0


def isCraw(func):
    def wrapper(*args, **kwargs):
        global ips, last
        agent = args[0].META.get('HTTP_USER_AGENT')
        if 'Mozilla' not in agent and 'Safari' not in agent and 'Chrome' not in agent:
            return HttpResponse('NO')
        else:
            ip = args[0].META.get('REMOTE_ADDR')  # 客户端IP地址
            now = time()
            if ip == ips[0] and now - last < 1:
                return HttpResponse('NO')
            last = now
            ips.pop()
            ips.append(ip)
            return func(*args, **kwargs)

    return wrapper
