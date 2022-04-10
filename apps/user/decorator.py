from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
import jwt

# 引入自己建的数据库model类
from apps.user.models import User


def auth_permission_required(perm):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # 格式化权限
            perms = (perm,) if isinstance(perm, str) else perm

            if request.user.is_authenticated:
                # 正常登录用户判断是否有权限
                if not request.user.has_perms(perms):
                    raise PermissionDenied
            else:
                try:
                    auth = request.META.get('HTTP_AUTHORIZATION').split()
                except AttributeError:
                    return JsonResponse({'status': 0, 'err': '缺少参数Token'})
                    # return JsonResponse({"code": 401, "message": "No authenticate header"})

                # 用户通过API获取数据验证流程
                if auth[0].lower() == 'token':
                    try:
                        dict = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
                        name = dict.get('data').get('name')
                    except jwt.ExpiredSignatureError:
                        return JsonResponse({'status': 0, 'err': 'Token已过期'})
                        # return JsonResponse({"status_code": 401, "message": "Token expired"})
                    except jwt.InvalidTokenError:
                        return JsonResponse({'status': 0, 'err': '无效的Token'})
                    except Exception as e:
                        return JsonResponse({'status': 0, 'err': '获取用户失败'})

                    try:
                        user = User.objects.get(name=name)
                    except User.DoesNotExist:
                        return JsonResponse({'status': 0, 'err': "用户不存在"})

                    if user.account_status != 1:
                        return JsonResponse({'status': 0, 'err': "账户异常"})

                    # # Token登录的用户判断是否有权限
                    # if not user.has_perms(perms):
                    #     return JsonResponse({'status': 0, 'err': "未授权用户，被拒绝访问"})
                else:
                    return JsonResponse({'status': 0, 'err': "不支持身份验证类型"})

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def get_user(req):
    auth = req.META.get('HTTP_AUTHORIZATION').split()
    dict = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
    username = dict.get('data').get('username')
    try:
        user = User.objects.get(name=username)
    except User.DoesNotExist:
        return JsonResponse({'status': 0, 'err': "用户不存在"})

    return user
