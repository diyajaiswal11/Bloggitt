from . import views
from django.urls import path

urlpatterns = [
    path('login', views.loginUser, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logoutUser, name='logout'),
    path('', views.postlist, name='home'),
    path('<slug:slug>/', views.postdetail, name='post_detail'),
]