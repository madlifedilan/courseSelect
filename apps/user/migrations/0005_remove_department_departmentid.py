# Generated by Django 4.0.4 on 2022-05-21 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_department_course_department_score_teacherscore_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='departmentID',
        ),
    ]
