from . import views
from django.urls import path

urlpatterns = [
    path('', views.postlist, name='home'),
    path('<slug:slug>/', views.postdetail, name='post_detail'),
    path('/',views.aboutdetail,name='about'),
]