from django.shortcuts import render, redirect
from django.views import generic
from .models import Post, FavouritePost
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.views.generic import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render,get_object_or_404
import json
from django.forms import model_to_dict

from django.contrib import messages

from django.db import IntegrityError

import datetime
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    return str(o)

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
        return render(request, "login.html")
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
                return render(request, "signup.html")
        messages.error(request, "Password doesn't match Confirm Password")
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "signup.html")


def postlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # post_list= Paginator(Post.objects.all().order_by('-created_on'),2)
    # page= request.GET.get('page')

    # try:
    #     posts = post_list.page(page)
    # except PageNotAnInteger:
    #     posts = post_list.page(1)
    # except EmptyPage:
    #     posts = post_list.page(post_list.num_pages)

    # return render(request,'index.html', {"post_list": posts})
    return render(request, "index.html")

def fetch(request):
    post_list= Paginator(Post.objects.all().order_by('-created_on'),2)
    page=request.POST.get("page")

    try:
        posts = post_list.page(page)
    except PageNotAnInteger:
        posts = post_list.page(1)
    except EmptyPage:
        posts = post_list.page(post_list.num_pages)

    post_dic = {
        "number": posts.number,
        "has_next": posts.has_next(),
        "has_previous": posts.has_previous(),
        "posts": []
    }

    for i in post_list.page(page):
        post_dic["posts"].append(i.__dict__)
    
    for i in post_dic["posts"]:
        i["author"]=User.objects.get(id = i.get("author_id")).username

    # for i in post_dic["posts"]:
    #     i["image"]=str(i["image"])
    
    return JsonResponse({"post_list": json.dumps(post_dic, default = default)})

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

    return render(request, 'detail.html', {'post': post, 'post_in_favorites': post_in_favorites})


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

    return render(request, 'favourites.html', { 'post_list': FavPosts.posts.all(), "favorites": True})

    
def about(request):
    context={}
    return render(request,'about.html',context=context)

class PostLikeToggle(RedirectView):
    def get_redirect_url(self,*args, **kwargs):
        id_ = self.kwargs.get("slug")
        obj = get_object_or_404(Post,slug=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                 obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None,format=None):
        obj = get_object_or_404(Post,slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        verb = None
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                verb = 'Like'
                obj.likes.remove(user)
                count = obj.likes.all().count()
            else:
                liked = True
                verb = 'Unlike'
                obj.likes.add(user)
                count = obj.likes.all().count()
            updated = True
        data = {
            "updated":updated,
            "liked":liked,
            "count":count,
            "verb":verb
        }
        return Response(data)
