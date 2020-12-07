from . import views
from django.urls import path

urlpatterns = [
    path('login', views.loginUser, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('favourites', views.favourites, name='favourites'),
    path('', views.postlist, name='home'),
    path('detail/<slug:slug>/', views.postdetail, name='post_detail'),
    path('detail/<slug:slug>/Favourites', views.Favorites, name='Favorites'),
    path('about',views.aboutdetail,name='about'),
]