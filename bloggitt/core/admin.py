from django.contrib import admin
from .models import Post, FavouritePost,Comment
# Register your models here.


admin.site.register(Post)
admin.site.register(FavouritePost)
admin.site.register(Comment)