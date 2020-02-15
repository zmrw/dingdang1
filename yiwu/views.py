from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
import os

from .models import User, Post, Image, Category

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def addgoods(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
        price = request.POST.get('price')
        category = request.POST.get('category')
        category = Category(name=category)
        category.save()
        img = request.FILES.getlist("img", None)  # 获取上传的文件，如果没有文件，则默认为None
        try:
            post = Post(title=title, body=body, price=price, author=user, category=category,
                        modified_time=timezone.now(),
                        created_time=timezone.now())
        except Exception as e:
            print(e)
        post.save()
        if not img:
            message1 = '文件上传失败，请重新上传文件'
            return render(request, 'yiwu/index.html', locals())
        usersimg = os.path.join(BASE_DIR, 'static', 'usersimg', str(user_id))
        if not os.path.exists(usersimg):
            os.mkdir(usersimg)
        else:
            pass
        for i in img:
            destination = open(os.path.join(usersimg, i.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in i.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            img = Image(name=i.name, post=post)
            img.save()

    return render(request, 'yiwu/index.html', locals())


def showgoods(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(author=user)
    imgs = Image.objects.filter(post__author=user)

    return render(request, 'yiwu/show-user-goods.html', locals())


def managegoods(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(author=user)

    return render(request, 'yiwu/manage-user-goods.html', locals())


def changegoods(request, id):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')

    if request.method == "POST":
        print('===========================')
        id = id
        post = Post.objects.get(id=id)
        title = request.POST.get('title')
        body = request.POST.get('body')
        price = request.POST.get('price')
        category = request.POST.get('category')
        img = request.FILES.get("img", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not img:
            message1 = '文件上传失败，请重新上传文件'
            return render(request, 'yiwu/index.html', locals())
        usersimg = os.path.join(BASE_DIR, 'static', 'usersimg', str(user_id))
        if not os.path.exists(usersimg):
            os.mkdir(usersimg)
        else:
            pass
        destination = open(os.path.join(usersimg, img.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in img.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        user = User.objects.get(id=user_id)
        category = Category(name=category)
        category.save()
        try:
            post.title = title
            post.body = body
            post.category = category
            post.price = price
        except Exception as e:
            print(e)
        post.save()
        img = Image(name=img.name, post=post)
        img.save()
    else:
        post = Post.objects.get(id=id)
        oldtitle = post.title
        oldprice = post.price
        oldbody = post.body
        oldcat = post.category
        return render(request, 'yiwu/changegoods.html', locals())

    return render(request, 'yiwu/changegoods.html', locals())


def delgoods(request, id):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    post = Post.objects.get(id=id)
    print(post)
    post.delete()
    posts = Post.objects.filter(author=user)
    return render(request, 'yiwu/manage-user-goods.html', locals())


def showallgoods(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    imgs = Image.objects.all()
    try:
        posts = Post.objects.all()
    except Exception as e:
        print(e)

    return render(request, 'yiwu/showallgoods.html', locals())
