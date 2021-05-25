from django import template
from ..forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }
@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    request=context['request']
    page = Paginator(comment_list, 6)  # 每页显示 10
    page_id = request.GET.get('page')
    try:
        comment_list = page.page(page_id)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        comment_list = page.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        comment_list = page.page(page.num_pages)


    return {

        'comment_count': comment_count,
        'comment_list': comment_list,

    }