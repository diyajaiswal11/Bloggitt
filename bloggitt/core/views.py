from django.shortcuts import render, redirect
from django.views import generic
from .models import Post, FavouritePost
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib import messages

from django.db import IntegrityError

def loginUser(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
        return render(request, "login2.html")
    return redirect("home")


def logoutUser(request):
    logout(request)
    messages.info(request, "Logged out of Bloggit")
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_c = request.POST.get("password-c")
        if (password == password_c):
            try:
                user = User.objects.create_user(username, email, password);
                user.save()
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect("home")
            except IntegrityError:
                messages.info(request, "Try different Username")
                return render(request, "signup2.html")
        messages.error(request, "Password doesn't match Confirm Password")
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "signup2.html")


def postlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    post_list= Paginator(Post.objects.all().order_by('-created_on'),2)
    page= request.GET.get('page')

    try:
        posts = post_list.page(page)
    except PageNotAnInteger:
        posts = post_list.page(1)
    except EmptyPage:
        posts = post_list.page(post_list.num_pages)

    return render(request,'index2.html', {"post_list": posts})
    # return render(request, "index2.html")

def postdetail(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
        
    post = Post.objects.get(slug=slug)

    post.read_count += 1
    post.save()

    Favourites,_ = FavouritePost.objects.get_or_create(user=request.user)
    post_in_favorites = None
    if post in Favourites.posts.all():
        post_in_favorites = True
    else:
        post_in_favorites = False

    return render(request, 'detail2.html', {'post': post, 'post_in_favorites': post_in_favorites})


def Favorites(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    Favourites,_ = FavouritePost.objects.get_or_create(user=user)

    post = Post.objects.get(slug=slug)

    if post not in Favourites.posts.all():
        Favourites.posts.add(post)
    else:
        Favourites.posts.remove(post)
    
    Favourites.save()
    
    return HttpResponse('Success')


def favorites(request):
    user = request.user
    FavPosts,_ = FavouritePost.objects.get_or_create(user=user)

    return render(request, 'index2.html', { 'post_list': FavPosts.posts.all(), 'favorites': True})

    
def about(request):
    context={}
    return render(request,'about.html',context=context)

def dummy(request):
    return render(request, "detail2.html")