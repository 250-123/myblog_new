
from django.db import models
from django.utils import timezone


class Comment(models.Model):
   #name = models.OneToOneField('users.User',to_field='username',related_name='Comment_name',verbose_name='用户名',on_delete=models.CASCADE)
    #email = models.OneToOneField('users.User',to_field='email',related_name='Comment_email',verbose_name='邮箱',on_delete=models.CASCADE)
    user=models.ForeignKey('users.User',verbose_name='用户',on_delete=models.CASCADE)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.text[:20])
# Create your models here.
