# Generated by Django 4.0.3 on 2022-05-23 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentName', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('kind', models.CharField(choices=[('teacher', '教师'), ('student', '学生'), ('admin', '管理员')], default='学生', max_length=10)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['c_time'],
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
                ('teacherID', models.CharField(max_length=20)),
                ('teacherName', models.CharField(max_length=20, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.department')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
                ('studentID', models.CharField(max_length=20)),
                ('studentName', models.CharField(max_length=20)),
                ('studentAddress', models.CharField(max_length=128, null=True)),
                ('studentCredit', models.IntegerField(null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.department')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score_date', models.IntegerField(null=True)),
                ('scoreCourse', models.CharField(max_length=20, null=True)),
                ('scoreCredit', models.PositiveIntegerField()),
                ('teacherScore', models.PositiveIntegerField(null=True)),
                ('scoreCourseID', models.CharField(max_length=20, null=True)),
                ('scoreStudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
                ('scoreTeacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.teacher')),
            ],
            options={
                'verbose_name': '成绩',
                'verbose_name_plural': '成绩',
                'ordering': ['scoreCourse'],
                'unique_together': {('scoreStudent', 'scoreCourse')},
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.CharField(max_length=20)),
                ('courseSeriesNumber', models.CharField(max_length=20)),
                ('courseName', models.CharField(max_length=255)),
                ('courseCredit', models.PositiveIntegerField()),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.department')),
                ('courseStudent', models.ManyToManyField(to='user.student')),
                ('courseTeacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.teacher')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
                'unique_together': {('courseID', 'courseName', 'courseSeriesNumber')},
            },
        ),
    ]
