from . import views
from django.urls import path
from .views import PostLikeToggle , PostLikeAPIToggle

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('favorites/', views.favorites, name='favorites'),
    path('', views.postlist, name='home'),
    # path('post/detail/<slug:slug>/', views.postdetail, name='post_detail'),
    # path('post/detail/<slug:slug>/Favourites', views.Favorites, name='Favorites'),
    # path('about',views.aboutdetail,name='about'),
    path('post/like/<slug:slug>/', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/like/<slug:slug>/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('detail/<slug:slug>/', views.postdetail, name='post_detail'),
    path('detail/<slug:slug>/Favourites', views.Favorites, name='Favorites'),
    path('about/',views.about,name='about')
]