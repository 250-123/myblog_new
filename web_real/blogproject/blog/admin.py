from django.contrib import admin
from django.contrib import admin
from .models import Post, Category, Tag
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body',  'category', 'tags','author']
    filter_horizontal = ('tags',)
  #  def save_model(self, request, obj, form, change):
       # obj.author = request.user
       # super().save_model(request, obj, form, change)
# 把新增的 Postadmin 也注册进来
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'email_to')}),
    )
    filter_horizontal = ('email_to',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
# Register your models here.
