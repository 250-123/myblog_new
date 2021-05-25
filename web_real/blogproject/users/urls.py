from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_change/', views.Change, name='user_change'),
    path('user_home/<int:id>/', views.home, name='user_home'),
    path('user_home/posts/<int:pk>/', views.change_post, name='change_post'),
    path('user_home/new_post/<int:pk>/', views.submit_post, name='submit_post'),
    path('user_home/posts/delete/<int:pk>/', views.delete_post, name='delete_post')
]