from django import forms
from captcha.fields import CaptchaField
class RegisterForm(forms.Form):
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})