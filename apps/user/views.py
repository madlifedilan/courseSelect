from django.core.cache import cache
from django.db.models import Avg, Sum
from django.shortcuts import render, redirect
from ratelimit.decorators import ratelimit
from .models import Course, Teacher, Student, User, Score, Admin, Department
from .forms import UserForm, RegisterForm
from apps.base.tracking_view import web_tracking

course_reg_id = 0
student_inform_reg = []
student_inform = []
course_student_inform = []
course_inform_check = []
course_inform = []
course_score_id = 0
course_score_inform = []


def index(request):
    pass
    return render(request, 'login/index.html')


def index_t(request):
    pass
    return render(request, 'login/index_t.html')


def index_s(request):
    student = request.session['user_id']
    scores = Score.objects.filter(scoreStudent=student)
    GPA = 0

    averageScore = scores.aggregate(Avg('score_date'))['score_date__avg']
    credit = scores.aggregate(Sum('scoreCredit'))['scoreCredit__sum']
    for score in scores:
        if score.score_date >= 90:
            GPA += 4.0 * score.scoreCredit / credit
            break
        elif score.score_date >= 85:
            GPA += 3.7 * score.scoreCredit / credit
            break
        elif score.score_date >= 80:
            GPA += 3.3 * score.scoreCredit / credit
            break
        elif score.score_date >= 75:
            GPA += 3.0 * score.scoreCredit / credit
            break
        elif score.score_date >= 70:
            GPA += 2.7 * score.scoreCredit / credit
            break
        elif score.score_date >= 65:
            GPA += 2.3 * score.scoreCredit / credit
            break
        elif score.score_date >= 60:
            GPA += 2.0 * score.scoreCredit / credit
            break
        else:
            pass
            break

    context = {
        "credit": credit,
        "averageScore": averageScore,
        "GPA": GPA
    }

    return render(request, 'login/index_s.html', context=context)


def index_a(request):
    pass
    return render(request, 'login/index_a.html')


def tea1(request):
    if request.method == "POST":
        courseID = request.POST.get("courseID")
        courseName = request.POST.get("courseName")
        courseSeriesNumber = request.POST.get("courseSeries")
        courseCredit = request.POST.get("courseCredit")
        teacherName = request.POST.get("teacherName")
        course_obj = Course.objects.create(courseID=courseID, courseName=courseName,
                                           courseSeriesNumber=courseSeriesNumber, courseCredit=courseCredit)
        teacher_obj = Teacher.objects.get(teacherName=teacherName)
        course_obj.courseTeacher.add(teacher_obj)
    return render(request, 'login/tea1.html')


def tea2(request):
    global student_inform_reg, course_reg_id, student_inform, course_student_inform
    student_inform_reg = []
    course_reg_id = 0
    student_inform = []
    course_student_inform = []
    if request.method == "GET":
        teacher_id = request.session['user_id']
        course_inform = Course.objects.filter(courseTeacher__id=teacher_id)
        context = {
            "course_inform": course_inform,
        }
        return render(request, 'login/tea2.html', context=context)
    else:
        course_reg_id = request.POST.get("course_id")
        course_student_inform = Student.objects.filter(course__id=course_reg_id)
        for cs in course_student_inform:
            a = cs.id
            student_inform.append(a)
        for s in student_inform:
            a = Student.objects.filter(id=s).first()
            student_inform_reg.append(a)
        context = {
            "student_inform_reg": student_inform_reg
        }
        return render(request, 'login/reg_score.html', context=context)


def tea3(request):
    global course_id, course_student_inform
    course_id = 0
    course_student_inform = []
    if request.method == "GET":
        teacher_id = request.session['user_id']
        course_inform = Course.objects.filter(courseTeacher__id=teacher_id)
        context = {
            "course_inform": course_inform,
        }
        return render(request, 'login/tea3.html', context=context)
    else:
        course_id = request.POST.get("course_id")
        course_student_inform = Score.objects.filter(scoreCourseID=course_id)
        context = {
            "course_student_inform": course_student_inform
        }
    return render(request, 'login/teacher_score.html', context=context)


def teacher_score(request):
    if request.method == "GET":
        context = {
            "student_inform_reg": course_student_inform
        }
        return render(request, 'login/teacher_score.html', context=context)
    else:
        context = {
            "student_inform_reg": course_student_inform
        }
    return


def reg(request):
    global student_inform_reg, course_reg_id
    if request.method == "GET":
        context = {
            "student_inform_reg": student_inform_reg
        }
        return render(request, 'login/reg_score.html', context=context)
    else:
        score = request.POST.get("score")
        student_id = request.POST.get("student_id")
        teacher_id = request.session['user_id']
        student_obj = Student.objects.get(studentID=student_id)
        teacher_obj = Teacher.objects.get(teacherID=teacher_id)
        idid = student_obj.id_id
        course_obj = Course.objects.get(id=course_reg_id)
        cname = course_obj.courseName
        ccredit = course_obj.courseCredit
        new_score = Score.objects.create(scoreCourse=cname, score_date=score,
                                         scoreStudent_id=idid, scoreCredit=ccredit, scoreTeacher=teacher_obj,
                                         scoreCourseID=course_reg_id)
        new_score.save()
        context = {
            "student_inform_reg": student_inform_reg
        }
        return render(request, 'login/reg_score.html', context=context)


def stu_to_tea(request):
    global course_score_inform, course_score_id

    if request.method == "GET":
        context = {
            "course_score_inform": course_score_inform
        }
        return render(request, 'login/stu_to_tea.html', context=context)
    else:
        score = request.POST.get("score")
        student_id = request.session['user_id']
        # course_id=request.POST.get("course_id")

        new_score = Score.objects.get(scoreCourseID=course_score_id, scoreStudent=student_id)
        new_score.teacherScore = score
        new_score.save()
        context = {
            "course_score_inform": course_score_inform
        }
        return render(request, 'login/stu_to_tea.html', context=context)


# @ratelimit(key='ip', rate='2/10s', block=True)
@web_tracking
def stu1(request):
    # 先把所有课程给获取了
    studentID = request.session['user_id']
    # page = int(request.GET.get('p', 1))
    # posts = Course.objects.all().order_by('courseID')
    # paginator = Paginator(posts, settings.ONE_PAGE_NEWS_COUNT)
    # page_obj = paginator.page(page)
    course_inform = cache.get("course_inform")
    if not course_inform:
        course_inform = list(Course.objects.all())
        cache.set("course_inform", course_inform, 60)

    context = {
        "course_inform": course_inform,
    }

    if request.method == "GET":
        return render(request, 'login/stu1.html', context=context)

    else:
        course_add_id = request.POST.get("course_add_id")
        student_obj = Student.objects.get(id=studentID)
        course_obj = Course.objects.get(id=course_add_id)
        course_obj.courseStudent.add(student_obj)

        return render(request, 'login/stu1.html', context=context)


def course_search(request):
    courseName = request.GET.get("course_search")
    course_search = Course.objects.filter(courseName__contains=courseName)

    context = {
        "course_inform": course_search,
    }
    if request.method == "GET":
        return render(request, 'login/stu1.html', context=context)


def stu2(request):
    global course_inform_check, course_score_id, course_score_inform, tea_score_inform
    course_inform_check = []
    tea_score_inform = []
    course_score_id = 0
    inform2 = []
    student = request.session['user_id']
    if request.method == "GET":
        inform = Course.objects.filter(courseStudent__id=student)
        for c in inform:
            cid = c.id
            inform2.append(cid)
        for c in inform2:
            obj = Course.objects.get(id=c)
            course_inform_check.append(obj)
        score_inform = Score.objects.filter(scoreStudent__id=student)
        context = {
            "course_inform_check": course_inform_check,
            "score_inform": score_inform
        }
        return render(request, 'login/stu2.html', context=context)
    else:
        course_score_id = request.POST.get("course_id")
        course_score_inform = Score.objects.filter(scoreCourseID=course_score_id, scoreStudent_id=student)

        context = {
            "course_score_inform": course_score_inform
        }
        return render(request, 'login/stu_to_tea.html', context=context)


def stu3(request):
    credit = 0
    student = request.session['user_id']
    scores = Score.objects.filter(scoreStudent=student)

    for s in scores:
        score_check = s.score_date
        try:
            if score_check >= 60:
                credit += s.scoreCredit
            else:
                continue
        except AttributeError:
            credit += 0
    Student.objects.filter(id_id=student).update(studentCredit=credit)
    student_inform = Student.objects.filter(id_id=student)
    context = {
        "student_inform": student_inform,
        "student_credit": credit
    }
    return render(request, 'login/stu3.html', context=context)


def stu4(request):
    global course_inform_check
    studentID = request.session['user_id']
    course_inform_check = []
    inform2 = []
    student = request.session['user_id']
    inform = Course.objects.filter(courseStudent__id=student)
    for c in inform:
        cid = c.id
        inform2.append(cid)
    for c in inform2:
        obj = Course.objects.get(id=c)
        course_inform_check.append(obj)
    score_inform = Score.objects.filter(scoreStudent_id=student)
    context = {
        "course_inform_check": course_inform_check,
        "score_inform": score_inform
    }
    if request.method == "GET":
        return render(request, 'login/stu4.html', context=context)
    else:
        course_remove_id = request.POST.get("course_remove_id")
        student_obj = Student.objects.get(id=studentID)
        course_obj = Course.objects.get(id=course_remove_id)
        course_obj.courseStudent.remove(student_obj)
        return redirect('/stu4')


def adm1(request):
    if request.method == "GET":
        student_inform = Student.objects.all()
        context = {
            "student_inform": student_inform,
        }
        return render(request, 'login/adm1.html', context=context)
    else:
        address = request.POST.get("address")
        student_id = request.POST.get("student_id")
        print(address)
        Student.objects.filter(studentID=student_id).update(studentAddress=address)
        return render(request, 'login/adm1.html')


def adm2(request):
    student_inform = Student.objects.all()
    context = {
        "student_inform": student_inform,
    }
    return render(request, 'login/adm2.html', context=context)


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            real_name = register_form.cleaned_data['real_name']
            id = register_form.cleaned_data['id']
            kind = register_form.cleaned_data['kind']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                # 当一切都OK的情况下，创建新用户
                new_user = User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.kind = kind
                new_user.save()
                if kind == '教师':
                    new_tea = Teacher.objects.create(id_id=new_user.id)
                    new_tea.teacherName = real_name
                    new_tea.teacherID = id
                    new_tea.save()
                elif kind == '学生':
                    new_stu = Student.objects.create(id_id=new_user.id)
                    new_stu.id_id = new_user.id
                    new_stu.studentName = real_name
                    new_stu.studentID = id
                    new_stu.save()
                else:
                    new_su = Admin.objects.create(id_id=new_user.id)
                    new_su.id_id = new_user.id
                    new_su.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


# @ratelimit(key='ip', rate='2/10s', block=True)
@web_tracking
def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        # 检查表单
        message = ""
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_kind'] = user.kind
                    return redirect('user:index_s')
                else:
                    message = "密码不正确！"
            except Exception as e:
                print(e)
                message = "用户不存在！"
            return render(request, 'login/login.html', locals())
        message = "验证码错误"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def form(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        user_obj = User.objects.get(id=user_id)
        user_password = request.POST.get("user_password")
        user_obj.password = user_password
        user_obj.save()
        return render(request, 'login/form.html', locals())
    else:
        student_obj = Student.objects.get(id=request.session.get('user_id'))
        context = {
            'student': student_obj,
        }
        print(student_obj.department.departmentName)
        return render(request, 'login/form.html', context=context)


def update(request):
    import pandas as pd
    filepath = "course1.xlsx"
    data = pd.read_excel(filepath)
    dataDict = data.values
    for row in dataDict:
        courseID, courseSeriesNumber, courseName, courseCredit, department, courseTeacher = row[0], row[1], row[2], row[
            3], row[5], row[13]
        user_obj = User.objects.update_or_create(name=courseTeacher, password='12345678', kind='教师')
        teacher_obj = Teacher.objects.update_or_create(id_id=user_obj[0].id, teacherName=courseTeacher,
                                                       teacherID=user_obj[0].id)
        course_obj = Course.objects.update_or_create(courseID=courseID, courseSeriesNumber=courseSeriesNumber,
                                                     courseName=courseName,
                                                     courseCredit=courseCredit, courseTeacher=teacher_obj[0])

        department_obj = Department.objects.update_or_create(departmentName=department)

        department_obj[0].teacher_set.add(teacher_obj[0])  # 老师增加学院
        department_obj[0].course_set.add(course_obj[0])  # 课程增加学院
