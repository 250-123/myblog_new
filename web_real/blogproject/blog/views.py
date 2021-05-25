
import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post, Category,Tag
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    page = Paginator(post_list, 5)  # 每页显示 4 个文章
    page_id = request.GET.get('page')
    try:
        post_list = page.page(page_id)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = page.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = page.page(page.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})

#页边距月份归档
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    page = Paginator(post_list, 5)  # 每页显示 4 个文章
    page_id = request.GET.get('page')
    try:
        post_list = page.page(page_id)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = page.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = page.page(page.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list,'year':year,'month':month})
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    #print("11111111111111111111")
   # print(post.body)
    #tag_list=Tag.objects.filter(pk=pk)
    #print("111111111111111111")
   # print(tag_list.name)
    #post.body = md.convert(post.body)
    post.toc = md.toc
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post,'tag_list':post.tags.all()})
#分类归档文章
def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    page = Paginator(post_list, 5)  # 每页显示 4 个文章
    page_id = request.GET.get('page')
    try:
        post_list = page.page(page_id)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = page.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = page.page(page.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list,'category':cate})
#标签归档文章
def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    page = Paginator(post_list, 5)  # 每页显示 4 个文章
    page_id = request.GET.get('page')
    try:
        post_list = page.page(page_id)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = page.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = page.page(page.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list,'tag':t})

def search(request):

    str_search = request.GET.get('search')

    search_context=str_search
    post_list = Post.objects.filter(Q(title__icontains=str_search) | Q(body__icontains=str_search)|Q(author__nickname=str_search))

    page = Paginator(post_list, 5)  # 每页显示 4 个文章
    page_id = request.GET.get('page')
    try:
        post_list = page.page(page_id)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = page.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = page.page(page.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list,'search_context' : search_context})