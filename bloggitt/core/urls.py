from . import views
from django.urls import path
from .views import PostLikeToggle , PostLikeAPIToggle

urlpatterns = [
    path('login', views.loginUser, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logoutUser, name='logout'),
    path('favourites', views.favourites, name='favourites'),
    path('', views.postlist, name='home'),
    path('post/detail/<slug:slug>/', views.postdetail, name='post_detail'),
    path('post/detail/<slug:slug>/Favourites', views.Favorites, name='Favorites'),
    path('about',views.aboutdetail,name='about'),
    path('post/like/<slug:slug>/', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/like/<slug:slug>/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 