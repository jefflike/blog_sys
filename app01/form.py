from django.forms import Form,widgets
from django.forms import fields
from django.core.exceptions import ValidationError
from app01 import models
class SignForm(Form):
    username = fields.CharField(max_length=32,
                              required=True,
                              widget=widgets.TextInput(attrs={'class':"form-control", "placeholder":'用户名'}))
    password = fields.CharField(max_length=64,
                                required=True,
                                widget=widgets.PasswordInput(attrs={'class':"form-control","placeholder":'密码'}))
    password2 = fields.CharField(max_length=64,
                                required=True,
                                widget=widgets.PasswordInput(attrs={'class':"form-control","placeholder":'再次输入密码'}))
    nickname=fields.CharField(
        max_length=32,
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control", "placeholder": '昵称'}))
    email=fields.EmailField(required=True,widget=widgets.TextInput(attrs={'class':"form-control","placeholder":'邮箱'}))
    avatar=fields.FileField(required=True,widget=widgets.FileInput(attrs={'id':"imgSelect",'class':"f1"}))
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    # def clean_code(self):
    #     input_code = self.cleaned_data['code']
    #     session_code = self.request.session.get('code')
    #     print(input_code)
    #     print(session_code)
    #     if input_code.upper() == session_code.upper():
    #         return input_code
    #     raise ValidationError('验证码错误')

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 == p2:
            # return self.cleaned_data
            input_code = self.request.POST.get('code')
            session_code = self.request.session.get('code')
            if input_code.upper() == session_code.upper():
                # return self.cleaned_data
                username = self.cleaned_data.get('username')
                if models.UserInfo.objects.filter(username=username).count():
                    # raise ValidationError('用户名已经存在')
                    self.add_error('username', '用户名已经存在')
                else:
                    return None
            raise ValidationError('验证码错误')
        # self.add_error(None,ValidationError('密码不一致'))
        self.add_error("password2",ValidationError('密码不一致'))

    # def cleaned_data(self):
    #     pass

class Loginform(Form):
    username = fields.CharField(max_length=32,
                                required=True,
                                widget=widgets.TextInput(attrs={'class': "form-control", "placeholder": '用户名'}))
    password = fields.CharField(max_length=64,
                                required=True,
                                error_messages={
                                    'invalid': '用户名不能为空',
                                    'required':'用户名不能为空'
                                },
                                widget=widgets.PasswordInput(attrs={'class': "form-control", "placeholder": '密码'}))
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean(self):
        # return self.cleaned_data
        input_code = self.request.POST.get('code')
        session_code = self.request.session.get('code')
        if input_code.upper() == session_code.upper():
            return None
        raise ValidationError('验证码错误')