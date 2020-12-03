from django.contrib import admin
from .models import Post, FavouritePost
# Register your models here.


admin.site.register(Post)
admin.site.register(FavouritePost)
