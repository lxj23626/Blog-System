from django.shortcuts import render, HttpResponse, redirect
from repository import models
from ..forms.registerform import RegisterForm
from ..forms.loginform import LoginForm
import json

from io import BytesIO
from utils.check_code import create_validate_code

def check_code(request):
    stream = BytesIO()  
    img, code = create_validate_code()   # 返回一张图片和随机字符串，只存在一次
    img.save(stream, 'PNG')              # 保存到内存里
    request.session['CheckCode'] = code  # 把随机字符串保存下来，用来等用户输入做验证
    return HttpResponse(stream.getvalue())

def register(request):
    if request.method == 'GET':
        # 如果已经登录，用户自己手动输入网页进入注册页面，则跳转到首页
        if_login = request.session.get('userinfo', None)
        if if_login:
            return redirect('/')
        return render(request, 'web/register.html')

    else:
        result = {'status': False, 'message': None, 'data': None}
        form = RegisterForm(request, request.POST)

        if form.is_valid():
            models.UserInfo.objects.create(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                email=request.POST.get('email'),
            )

            # 将新注册的用户的可能用到的信息从数据库取出放在session里，相当于已经登录
            userinfo = models.UserInfo.objects.filter(
                username = form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            ).values(
                'uid',
                'nickname',
                'username',
                'email',
                'avatar',
                'blog__bid',
                'blog__site'
            ).first()
            request.session['userinfo'] = userinfo
            result['status'] = True
        else:
            # print(111, form.errors)          # ErrorDict对象，字典
            '''form.errors = 
                <ul class="errorlist">
                    <li>username
                        <ul class="errorlist">
                            <li>用户名不能为空</li>
                        </ul>
                    </li>
                    
                    <li>email
                        <ul class="errorlist">
                            <li>邮箱不能为空</li>
                        </ul>
                    </li>
                    
                    <li>password
                        <ul class="errorlist">
                            <li>密码不能为空</li>
                        </ul>
                    </li>
                    
                    <li>second_password
                        <ul class="errorlist">
                            <li>确认密码不能为空</li>
                        </ul>
                    </li>
                    
                    <li>check_code
                        <ul class="errorlist">
                            <li>验证码不能为空</li>
                        </ul>
                    </li>
                </ul>
            '''

            error_name = list(form.errors)
            # print('222', error_name)                     # ['username', 'email', 'password', 'second_password', 'check_code']
            # print('333', form.errors[error_name[0]])     # <ul class="errorlist"><li>用户名不能为空</li></ul>
            # print('444', form.errors[error_name[0]][0])  # 用户名不能为空
            result['message'] = form.errors[error_name[0]][0]
        return HttpResponse(json.dumps(result))


def login(request):
    # print(1111111111111,request.session['userinfo'])
    # print(2222222222, request.session['CheckCode'])
    if request.method == 'GET':
        if_login = request.session.get('userinfo', None)
        if if_login:
            return redirect('/')
        return render(request, 'web/login.html')

    else:
        result = {'status': False, 'err_message': None}
        form = LoginForm(request, request.POST)

        if form.is_valid():
            result['status'] = True
            # print(form.userinfo)
            request.session['userinfo'] = form.userinfo
        else:
            error_name_list = list(form.errors)
            result['err_message'] = form.errors[error_name_list[0]][0]

        if form.rmb:
            request.session.set_expiry(60 * 60 * 24 * 7)
            
        return HttpResponse(json.dumps(result))


def logout(request):
    request.session.clear()
    return redirect('/')

