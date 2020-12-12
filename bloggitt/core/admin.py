from django.contrib import admin
from .models import Post, FavouritePost,Profile, Comment
from .models import Post, FavouritePost,Comment
# Register your models here.


admin.site.register(Post)
admin.site.register(FavouritePost)
admin.site.register(Profile)
admin.site.register(Comment)
