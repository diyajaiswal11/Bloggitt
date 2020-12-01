from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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

    object_list=Post.objects.all().order_by('-created_on')
    paginator=Paginator(object_list, 3)     # 3 posts in each page
    page=request.GET.get('page')
    try:
        post_list=paginator.page(page)
    except PageNotAnInteger:
          # if Page is not an integer deliver the first page  
        post_list=paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        post_list=paginator.page(paginator.num_pages)

    return render(request,'index.html',{'page':page,'post_list':post_list})

def postdetail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'detail.html', {'post': post})
    
def aboutdetail(request):
    context={}
    return render(request,'about.html',context=context)