from captcha.fields import CaptchaField
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class RegisterForm(forms.Form):
    attribute = (
        ('教师', 'teacher'),
        ('学生', 'student'),
        ('管理员', 'admin')
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    real_name = forms.CharField(label="真实姓名", max_length=128,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    id = forms.CharField(label="学号/工号", max_length=128,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    kind = forms.ChoiceField(label='用户类型', choices=attribute, )
