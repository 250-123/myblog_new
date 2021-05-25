
from django.shortcuts import render, redirect
from .forms import RegisterForm,ChangeForm,ChangeForm1,Changepost,add_tags,Submit_postform
from django.contrib import messages
from blog.models import Post,Tag
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})

#个人主页页面视窗函数
def home(request,id):


    post_list=Post.objects.filter(author_id=id).order_by('-created_time')
    home_user=User.objects.get(id=id)
    page = Paginator(post_list, 4)  # 每页显示 4 个文章
    page_id = request.GET.get('page')
    print(request)
    try:
        post_list = page.page(page_id)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = page.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = page.page(page.num_pages)
    print(home_user.nickname)
    print("111")
    return render(request, 'users/user_home.html', context={'post_list':post_list,'home_user':home_user})
#修改昵称和头像
def Change(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        print(request.POST)
        if 'nickname' in request.POST:
            form = ChangeForm(request.POST, request.FILES)
            form1 = ChangeForm1()
        else:
            form1 = ChangeForm1(request.POST, request.FILES)
            form = ChangeForm()


        # 验证数据的合法性
        if form.is_valid():
            print("1111111111111111")
            user_now = form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            request.user.nickname= user_now.nickname
            request.user.save()
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            # 注册成功，跳转回首页
            return redirect('/users/user_change/')
        if form1.is_valid():
            print("22222222222222222222222222222222")
            user_now = form1.save(commit=False)
            # 将评论和被评论的文章关联起来。
            request.user.img = user_now.img
            request.user.save()
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            # 注册成功，跳转回首页
            return redirect('/users/user_change/')

    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = ChangeForm()
        form1 = ChangeForm1()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'users/user_index.html', context={'form': form,'form1': form1})
#个人主页修改博客内容
def change_post(request,pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method != 'POST':
        form = Changepost(instance=post)
        form1 = add_tags()
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单

    else:
        print(request.POST)
        form = Changepost(instance=post, data=request.POST)
        form1 = add_tags(request.POST)
        if form.is_valid():

            form_now = form.save(commit=True)
            form_now.author_id=request.user.id
            form_now.save()
            return redirect('users:change_post',pk)
        if not form.is_valid():
            #print("非合法的吗？？？？")
            form = Changepost(instance=post,data=request.POST)
        if form1.is_valid():
            form_now = form1.save(commit=True)
            form_now.save()
            return redirect('users:change_post', pk)
    return render(request,'users/user_change_post.html' , context={'form': form,'post1':post,'form1': form1})

#写文章的视窗函数
def submit_post(request,pk):
    post=Post(author_id=pk)

    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = Submit_postform(instance=post, data=request.POST)
        form1 = add_tags(request.POST)
        # 验证数据的合法性
        if not form.is_valid():
            print("不合法！")
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form_now=form.save(commit=True)
            form_now.author_id=pk
            form_now.save()

            return redirect('users:submit_post',pk)
        if form1.is_valid():

            form_now = form1.save(commit=True)
            form_now.save()
            return redirect('users:submit_post', pk)
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = Submit_postform(instance=post)
        form1 = add_tags()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递

    return render(request,'users/user_submit_post.html' , context={'form': form,'form1': form1,'pk':pk})

def delete_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    title=post.title
    post.delete()

    return render(request,'users/user_delete_post.html' , context={"title":title})