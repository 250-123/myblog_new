

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    img = models.ImageField(upload_to='img',blank=True)
    email = models.EmailField(unique=True)

    def get_home_id_url(self):

        return '/users/user_home/'+str(self.id)+'/'
    def new_post(self):

        return '/users/user_home/new_post/'+str(self.id)+'/'


    class Meta(AbstractUser.Meta):
        pass
# Create your models here.
