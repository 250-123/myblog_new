from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_time']
    fields = ['user', 'text', 'post']


admin.site.register(Comment, CommentAdmin)
# Register your models here.
