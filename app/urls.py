from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('index_t/', views.index_t, name='index_t'),
    path('index_s/', views.index_s, name='index_s'),
    path('index_a/', views.index_a, name='index_a'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('tea1/', views.tea1, name='tea1'),
    path('tea2/', views.tea2, name='tea2'),
    path('reg_score/', views.reg, name='reg'),
    path('stu1/', views.stu1, name='stu1'),
    path('stu2/', views.stu2, name='stu2'),
    path('stu3/', views.stu3, name='stu3'),
    path('stu4/', views.stu4, name='stu4'),
    path('adm1/', views.adm1, name='adm1'),
    path('adm2/', views.adm2, name='adm2'),
    path('update/', views.update, name='update'),
    path('base/', views.base, name='base'),
]
