from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from blog.models import Post,Tag
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email","nickname")

#修改昵称
class ChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname"]
#修改头像
class ChangeForm1(forms.ModelForm):
            class Meta:
                model = User
                fields = ["img"]
#修改文章内容表单
class Changepost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title","body","tags"]

#为文章增加标签
class add_tags(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
class Submit_postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","body",'category', 'tags']
