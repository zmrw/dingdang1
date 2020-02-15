from django.shortcuts import render
from django.shortcuts import redirect

import hashlib
from . import models
from yiwu.models import Post

# Create your views here.

# 加密密码，使密码不是明文
def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = models.User.objects.get(id=user_id)
    postcount = Post.objects.filter(author=user).count()
    # name = user.name
    return render(request, 'login/index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        message = '请检查填写内容！'
        if email.strip() and password:
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(email=email)
            except:
                message = '用户名不存在！'
                return render(request, 'login/login.html', locals())
        if user.password == hash_code(password):
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('/index/')
        else:
            message = '密码不正确！'
            return render(request, 'login/login.html', locals())
    else:
        return render(request, 'login/login.html', locals())
    return render(request, 'login/login.html')


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password1 != password2:
            message = '两次输入的密码不同，请重新输入！'
            return render(request, 'login/register.html', locals())
        else:
            same_name_user = models.User.objects.filter(name=username)
            if same_name_user:
                message = '用户名已经存在'
                return render(request, 'login/register.html', locals())
            same_email_user = models.User.objects.filter(email=email)
            if same_email_user:
                message = '该邮箱已经注册！'
                return render(request, 'login/register.html', locals())

            new_user = models.User()
            new_user.name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.save()
            message = '注册成功，请登录！'
            return render(request, 'login/confirm.html', locals())
    else:
        return render(request, 'login/register.html', locals())
    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect("/login/")
