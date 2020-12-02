from django.contrib import admin
from .models import Post, FavouritePost, Category
# Register your models here.


admin.site.register(Post)
admin.site.register(FavouritePost)
admin.site.register(Category)
