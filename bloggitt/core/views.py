from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import SignupForm

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', { 'errorMsg': "Invalid credentials entered" })
    
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
            
        return render(request, 'signup.html', { 'errorMsg': "Please try different credentials" })
    
    return render(request, 'signup.html')


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

    return render(request,'index.html',{'post_list':posts})

def postdetail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'detail.html', {'post': post})
    
def aboutdetail(request):
    context={}
    return render(request,'about.html',context=context)