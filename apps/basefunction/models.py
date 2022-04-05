from django.db import models
from django.utils import timezone


# 用户的IP
class UserIP(models.Model):
    ip_address = models.CharField(max_length=30)
    ip_location = models.CharField(max_length=30)
    end_point = models.CharField(default='/', max_length=30)
    date = models.DateTimeField(default=timezone.now)


# 网站总访问次数
class VisitNumber(models.Model):
    count = models.IntegerField(default=0)


# 单日访问量统计
class DayNumber(models.Model):
    day = models.DateField(default=timezone.now)
    count = models.IntegerField(default=0)
