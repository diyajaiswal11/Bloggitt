from django.shortcuts import render
from django.views import generic
from .models import Post


def postlist(request):
    post_list=Post.objects.all().order_by('-created_on')
    return render(request,'index.html',{'post_list':post_list})

def postdetail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'detail.html', {'post': post})