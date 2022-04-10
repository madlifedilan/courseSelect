from django.db import models
from courseSelect import settings
from django.utils import timezone
import jwt


class User(models.Model):
    attribute = (
        ('teacher', '教师'),
        ('student', '学生'),
        ('admin', '管理员'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)  # 用户名（学号/工号）
    password = models.CharField(max_length=20)  # 用户密码
    kind = models.CharField(max_length=10, choices=attribute, default='学生')  # 用户属性 教师/学生
    c_time = models.DateTimeField(auto_now_add=True)
    exp_time = models.DateTimeField(verbose_name='Token过期时间', auto_now=False, blank=True,
                                    default=timezone.now() + timezone.timedelta(days=1))
    login_time = models.DateTimeField(verbose_name='登录时间', auto_now=True, blank=True)
    last_login_time = models.DateTimeField(verbose_name='上次登录时间', auto_now=False, blank=True,
                                           default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        exp = timezone.now() + timezone.timedelta(days=1)
        token = jwt.encode({
            'exp': exp,
            'iat': timezone.now(),
            'data': {
                'username': self.name
            }
        }, settings.SECRET_KEY, algorithm='HS256')
        lt = self.login_time
        nt = timezone.now()
        self.exp_time = exp
        self.last_login_time = lt
        self.login_time = nt
        self.save()
        print(type(token))
        return token

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Teacher(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # 教师类与用户类一对一
    teacherID = models.CharField(max_length=20)  # 教师工号
    teacherName = models.CharField(max_length=20, null=True)  # 教师姓名
    # 教师已开设课程，一对多，根据课程id寻找


class Student(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # 学生类与用户类一对一
    studentID = models.CharField(max_length=20)  # 学生学号
    studentName = models.CharField(max_length=20)  # 学生姓名
    studentAddress = models.CharField(max_length=128, null=True)  # 学生区块链地址
    studentCredit = models.IntegerField(null=True)  # 学生已获学分


class Admin(models.Model):
    id = models.OneToOneField(User, models.CASCADE, primary_key=True)  # 管理员类与用户类一对一


class Course(models.Model):
    courseID = models.CharField(max_length=20)  # 课程号
    courseSeriesNumber = models.CharField(max_length=20)  # 课序号
    courseName = models.CharField(max_length=255)  # 课程名
    courseCredit = models.PositiveIntegerField()  # 学分
    courseTeacher = models.ManyToManyField(Teacher)  # 授课教师 与教师类多对多
    courseStudent = models.ManyToManyField(Student)  # 课程学生 与学生类多对多

    class Meta:
        unique_together = (("courseID", "courseName", "courseSeriesNumber"),)
        verbose_name = '课程'
        verbose_name_plural = '课程'


class Score(models.Model):
    id = models.AutoField(primary_key=True)
    scoreStudent = models.ForeignKey(Student, on_delete=models.CASCADE)  # 成绩与学生一对多
    score_date = models.IntegerField(null=True)  # 成绩分数
    scoreCourse = models.CharField(max_length=20, null=True)  # 成绩课程名
    scoreCredit = models.PositiveIntegerField()

    class Meta:
        unique_together = ("scoreStudent", "scoreCourse")
        ordering = ['scoreCourse']
        verbose_name = '成绩'
        verbose_name_plural = '成绩'
